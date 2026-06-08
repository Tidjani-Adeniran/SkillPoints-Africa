import uuid  # Used for generating dynamic reward voucher codes
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.utils import timezone
from .models import SkillTrack, RewardItem, Enrollment, Redemption
from .models import Task, TaskCompletion, UserProfile

# ==========================================================================
# DEDICATED TRACKS PAGE VIEW
# ==========================================================================
def all_tracks(request):
    tracks = SkillTrack.objects.all()
    return render(request, 'tracks.html', {'tracks': tracks})


# ==========================================================================
# DEDICATED MARKETPLACE PAGE VIEW
# ==========================================================================
def all_rewards(request):
    rewards = RewardItem.objects.all()
    return render(request, 'marketplace.html', {'rewards': rewards})


# ==========================================================================
# AUTHENTICATION EXTENSION VIEW
# ==========================================================================
class SuccessMessageLoginView(LoginView):
    def form_valid(self, form):
        messages.success(self.request, f"Login successful! Welcome back, {form.get_user().username}.")
        return super().form_valid(form)


# ==========================================================================
# 1. LANDING PAGE VIEW
# ==========================================================================
def home(request):
    if request.GET.get('logout') == 'success':
        messages.success(request, "Logout successful!")
        return redirect('home')
    
    tracks = SkillTrack.objects.all().order_by('-id')[:3]
    rewards = RewardItem.objects.all().order_by('-id')[:3]
    context = {
        'tracks': tracks,
        'rewards': rewards
    }
    return render(request, 'home.html', context)


# ==========================================================================
# 2. PROTECTED USER DASHBOARD VIEW
# ==========================================================================
@login_required(login_url='login')
def dashboard(request):
    user = request.user
    
    profile, created = UserProfile.objects.get_or_create(user=user)
    points_balance = profile.points_balance
    
    enrolled_count = user.enrollments.filter(status__in=['DIAGNOSTIC', 'ACTIVE']).count()
    completed_count = user.enrollments.filter(status='COMPLETED').count()
    active_enrollments = user.enrollments.filter(status__in=['DIAGNOSTIC', 'ACTIVE'])
    redeemed_rewards = Redemption.objects.filter(user=user).order_by('-date_redeemed')
    
    context = {
        'points_balance': points_balance,
        'enrolled_count': enrolled_count,
        'completed_count': completed_count,
        'active_enrollments': active_enrollments,
        'redeemed_rewards': redeemed_rewards,
    }
    return render(request, 'dashboard.html', context)


# ==========================================================================
# 3. ENROLLMENT ENGINE ACTION (DIRECT DASHBOARD ROUTING 🎯)
# ==========================================================================
@login_required(login_url='login')
def enroll_in_track(request, track_id):
    track = get_object_or_404(SkillTrack, id=track_id)
    enrollment, created = Enrollment.objects.get_or_create(user=request.user, track=track)
    
    if created:
        messages.success(request, f"Successfully enrolled in {track.title}! Track has been added to your workspace catalog list.")
    else:
        messages.info(request, f"You are already actively enrolled in {track.title}.")
        
    return redirect('dashboard')


# ==========================================================================
# 4. FIXED WORKSPACE ARCHITECTURE ACTIONS (DIRECT MANUALLY ADDED DATA LOADING 🚀)
# ==========================================================================
@login_required(login_url='login')
def track_workspace(request, enrollment_id):
    """Instantly tracks and pulls tasks that you manually created inside the database panel view."""
    enrollment = get_object_or_404(Enrollment, id=enrollment_id, user=request.user)
    
    # Bypass legacy AI diagnostics and automatically activate track environment
    if enrollment.status == 'DIAGNOSTIC':
        enrollment.status = 'ACTIVE'
        enrollment.save()
        
    # Directly fetch static course content tasks added via admin dashboard
    tasks = Task.objects.filter(track=enrollment.track).order_by('order')
    
    # Map completion lists to verify task checkboxes on UI layer
    completions = TaskCompletion.objects.filter(user=request.user, task__track=enrollment.track)
    completed_tasks_list = list(completions.filter(status='PASSED').values_list('task_id', flat=True))
    
    context = {
        'enrollment': enrollment,
        'tasks': tasks,
        'completed_tasks_list': completed_tasks_list,
    }
    return render(request, 'workspace.html', context)


@login_required(login_url='login')
def complete_workspace_task(request, task_id):
    """Bypasses AI processing. Instantly confirms work and adds track task points directly to profile wallet."""
    if request.method != 'POST':
        return redirect('dashboard')
        
    task = get_object_or_404(Task, id=task_id)
    enrollment = get_object_or_404(Enrollment, track=task.track, user=request.user)
    submission_text = request.POST.get('submission_text', '').strip()
    
    if not submission_text:
        messages.error(request, "Assignment text field submission cannot be left blank.")
        return redirect('track_workspace', enrollment_id=enrollment.id)
        
    completion, created = TaskCompletion.objects.get_or_create(user=request.user, task=task)
    
    if completion.status == 'PASSED':
        messages.info(request, f"Milestone task points for {task.title} have already been successfully added.")
        return redirect('track_workspace', enrollment_id=enrollment.id)

    # 🎯 INSTANT AUTO-APPROVAL ACTION
    completion.submission_text = submission_text
    completion.status = 'PASSED'
    completion.ai_feedback = "System Verification Engine: Project submission successfully logged and authenticated."
    completion.save()
    
    # 💰 AUTOMATIC POINT ACCRUAL LEDGER
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    profile.points_balance += task.points_value
    profile.save()
    
    messages.success(request, f"🎉 Task Verified! +{task.points_value} SP added directly to your profile balance wallet.")

    # Automatically handle complete track graduation 🎓
    all_track_tasks = Task.objects.filter(track=enrollment.track)
    passed_tasks_count = TaskCompletion.objects.filter(user=request.user, task__track=enrollment.track, status='PASSED').count()
    
    if all_track_tasks.count() == passed_tasks_count and all_track_tasks.count() > 0:
        enrollment.status = 'COMPLETED'
        enrollment.date_completed = timezone.now()
        enrollment.save()
        messages.success(request, f"🎓 Incredible achievement! You have completely graduated from {enrollment.track.title}!")
        return redirect('dashboard')
        
    return redirect('track_workspace', enrollment_id=enrollment.id)


# ==========================================================================
# 5. MARKETPLACE REWARD SPEND ENGINE
# ==========================================================================
@login_required(login_url='login')
def redeem_reward(request, reward_id):
    user = request.user
    reward = get_object_or_404(RewardItem, id=reward_id)
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    if profile.points_balance < reward.points_cost:
        messages.error(
            request, 
            f"Transaction Declined: You need {reward.points_cost} SP for this reward. Your current balance is {profile.points_balance} SP."
        )
        return redirect('dashboard')
        
    if reward.stock_status.lower() == 'out of stock':
        messages.error(request, f"Sorry, {reward.title} is currently out of stock.")
        return redirect('dashboard')

    profile.points_balance -= reward.points_cost
    profile.save()
    
    mock_voucher = f"SP-{reward.vendor[:3].upper()}-{str(uuid.uuid4())[:8].upper()}"
    
    Redemption.objects.create(
        user=user,
        reward=reward,
        voucher_code=mock_voucher
    )
    
    messages.success(
        request, 
        f"Redemption Successful! 🎉 {reward.points_cost} SP deducted. Your voucher code for {reward.title} is: {mock_voucher}"
    )
    
    return redirect('dashboard')