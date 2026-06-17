import uuid  # Used for generating dynamic reward voucher codes
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.utils import timezone
from .models import SkillTrack, RewardItem, Enrollment, Redemption
from .models import Task, TaskCompletion, UserProfile
from .ai_services import generate_skill_task, evaluate_student_submission

# ==========================================================================
# PUBLIC SITE VIEWS
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


def all_tracks(request):
    tracks = SkillTrack.objects.all()
    return render(request, 'tracks.html', {'tracks': tracks})


def all_rewards(request):
    rewards = RewardItem.objects.all()
    return render(request, 'marketplace.html', {'rewards': rewards})


def about_page(request):
    """Renders the SkillPoints Africa mission and vision overview page."""
    return render(request, 'about.html')


class SuccessMessageLoginView(LoginView):
    def form_valid(self, form):
        messages.success(self.request, f"Login successful! Welcome back, {form.get_user().username}.")
        return super().form_valid(form)


# ==========================================================================
# CORE STUDENT DASHBOARD
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
    
    passed_task_ids = set(
        TaskCompletion.objects.filter(user=user, status='PASSED').values_list('task_id', flat=True)
    )
    
    for enrollment in active_enrollments:
        total_tasks = enrollment.track.tasks.count()
        if total_tasks > 0:
            completed_tasks_count = enrollment.track.tasks.filter(id__in=passed_task_ids).count()
            enrollment.progress_percentage = int((completed_tasks_count / total_tasks) * 100)
        else:
            enrollment.progress_percentage = 0
            
    context = {
        'points_balance': points_balance,
        'enrolled_count': enrolled_count,
        'completed_count': completed_count,
        'active_enrollments': active_enrollments,
        'redeemed_rewards': redeemed_rewards,
    }
    return render(request, 'dashboard.html', context)


@login_required(login_url='login')
def enroll_in_track(request, track_id):
    track = get_object_or_404(SkillTrack, id=track_id)
    enrollment, created = Enrollment.objects.get_or_create(user=request.user, track=track)
    
    if created:
        messages.success(request, f"Successfully enrolled in {track.title}! Track has been added to your workspace.")
    else:
        messages.info(request, f"You are already actively enrolled in {track.title}.")
        
    return redirect('dashboard')


# ==========================================================================
# WORKSPACE LEARNING RUNTIME
# ==========================================================================
@login_required(login_url='login')
def track_workspace(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id, user=request.user)
    
    if enrollment.status == 'DIAGNOSTIC':
        enrollment.status = 'ACTIVE'
        enrollment.save()
        
    tasks = Task.objects.filter(track=enrollment.track).order_by('order')
    completions = TaskCompletion.objects.filter(user=request.user, task__track=enrollment.track)
    
    completed_tasks_list = list(completions.filter(status='PASSED').values_list('task_id', flat=True))
    
    # Builds a real-time completion dictionary state lookup mapping for templates
    completion_status_map = {c.task_id: c.status for c in completions}
    
    context = {
        'enrollment': enrollment,
        'tasks': tasks,
        'completed_tasks_list': completed_tasks_list,
        'completion_status_map': completion_status_map,
    }
    return render(request, 'workspace.html', context)


@login_required(login_url='login')
def complete_workspace_task(request, task_id):
    if request.method != 'POST':
        return redirect('dashboard')
        
    task = get_object_or_404(Task, id=task_id)
    enrollment = get_object_or_404(Enrollment, track=task.track, user=request.user)
    
    completion, created = TaskCompletion.objects.get_or_create(user=request.user, task=task)
    if completion.status == 'PASSED':
        messages.info(request, f"Milestone task points for {task.title} have already been successfully added.")
        return redirect('track_workspace', enrollment_id=enrollment.id)

    # 🎛️ DYNAMIC ASSIGNMENT EVALUATION ENGINE ROUTER
    if task.assignment_type in ['multiple_choice', 'checkbox']:
        selected_choices = request.POST.getlist('quiz_choices')
        correct_choices = task.correct_options if isinstance(task.correct_options, list) else []
        
        if sorted(selected_choices) == sorted(correct_choices):
            completion.status = 'PASSED'
            completion.submission_text = f"Selected Quiz Answers: {', '.join(selected_choices)}"
            completion.admin_feedback = "Quiz Verification Engine: Instantly verified correct option arrays."
            completion.save()
            
            # Award points instantly for successful quiz runs
            profile, _ = UserProfile.objects.get_or_create(user=request.user)
            profile.points_balance += task.points_value
            profile.save()
            
            messages.success(request, f"🎉 Quiz Correct! +{task.points_value} SP added directly to your wallet balance.")
        else:
            completion.status = 'FAILED'
            completion.admin_feedback = "Quiz Verification Engine: Submission failed verification due to incorrect selection options."
            completion.save()
            messages.error(request, "❌ Quiz selection answers were incorrect. Review the lesson materials and try again.")
            return redirect('track_workspace', enrollment_id=enrollment.id)

    else:
        # TEXT portfolio assignment queue tracking mechanics
        submission_text = request.POST.get('submission_text', '').strip()
        if not submission_text:
            messages.error(request, "Assignment text field submission cannot be left blank.")
            return redirect('track_workspace', enrollment_id=enrollment.id)
            
        completion.submission_text = submission_text
        completion.status = 'PENDING'  # Routed to human Operations Cockpit queue
        
        # 🎯 Fix Applied: Clear old records on re-submission so placeholder texts don't linger
        completion.admin_feedback = "Pending evaluation review from operations staff."
        completion.save()
        messages.warning(request, "🚀 Solution uploaded successfully! Portfolio has been routed to the review queue desk.")

    # Auto graduation tracking routine
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
# CENTRAL PRODUCTION OPERATIONS COCKPIT
# ==========================================================================
@staff_member_required
def admin_dashboard(request):
    """Central production command deck for operations managing track fields and manual portfolio queues."""
    context = {
        'tracks': SkillTrack.objects.all(),
        'pending_submissions': TaskCompletion.objects.filter(status='PENDING').order_by('-id'),
    }
    return render(request, 'admin_dashboard.html', context)


@staff_member_required
def generate_track_content(request, track_id):
    """Triggered by the AI Generate button in the Operations Cockpit."""
    if request.method == 'POST':
        track = get_object_or_404(SkillTrack, id=track_id)
        batch_data = generate_skill_task(track.title, track.difficulty)
        
        if batch_data and batch_data.tasks:
            total_tasks_count = len(batch_data.tasks)
            track_total_points = track.points_awarded
            
            # Proportional allocation logic to cleanly handle any non-divisible remainders
            base_points = track_total_points // total_tasks_count
            remainder_points = track_total_points % total_tasks_count
            
            for idx, t in enumerate(batch_data.tasks, start=1):
                # Assign baseline points or capture leftover balance into the ultimate milestone task
                if idx == total_tasks_count:
                    task_assigned_points = base_points + remainder_points
                else:
                    task_assigned_points = base_points
                    
                Task.objects.create(
                    track=track,
                    order=idx,
                    title=t.title,
                    concept_summary=getattr(t, 'concept_summary', ''), # Synced to capture model summary field data
                    description=t.assignment_instruction,
                    learning_content=t.core_lessons,
                    local_example=t.local_example,
                    assignment_type=t.assignment_type,
                    options=t.options if t.options is not None else [],
                    correct_options=t.correct_options if t.correct_options is not None else [],
                    points_value=task_assigned_points,
                    is_approved=False # Defaults safely to Draft Blueprint for operations control reviews
                )
            messages.success(request, f"🎉 Generated course curriculum content for '{track.title}' successfully! Allocation balanced exactly to {track_total_points} SP.")
        else:
            messages.error(request, "Failed to connect to the Gemini API infrastructure.")
            
    return redirect('admin_dashboard')


@staff_member_required
def approve_submission(request, submission_id):
    """Processes portfolio submission choices from the admin interface queue."""
    if request.method == 'POST':
        completion = get_object_or_404(TaskCompletion, id=submission_id)
        action = request.POST.get('action')
        feedback = request.POST.get('admin_feedback', '').strip()
        
        if action == 'APPROVE':
            # Assign typed feedback or use standard approval text
            completion.admin_feedback = feedback if feedback else "Reviewed by Admin Panel Operations Staff."
            completion.status = 'PASSED'
            completion.save()
            
            # Process points addition ledger entry safely upon approval action
            profile, _ = UserProfile.objects.get_or_create(user=completion.user)
            profile.points_balance += completion.task.points_value
            profile.save()
            
            messages.success(request, f"Approved submission from {completion.user.username}. Points awarded!")
            
        elif action == 'REJECT':
            # 🎯 FIXED: Removed the constraint forcing text feedback entry. 
            # If blank, it now applies a helpful, standardized rejection default message.
            completion.admin_feedback = feedback if feedback else "Task rejected. Please review your implementation notes, check the lesson specifications, and re-submit for evaluation review."
            completion.status = 'REJECTED'
            completion.save()
            
            messages.warning(request, f"Submission from {completion.user.username} rejected back to revision loops.")
            
    return redirect('admin_dashboard')


# ==========================================================================
# MARKETPLACE REWARD SPEND ENGINE
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


# ==========================================================================
# SANDBOX PLAYGROUND SIMULATOR (OPTIONAL RUNTIME DEMO KEEP-ALIVE)
# ==========================================================================
def ai_demo_page(request):
    """Isolated sandbox route playground allowing playground checks outside the production models framework."""
    if 'generate_task' in request.POST:
        topic = request.POST.get('topic', 'Digital Marketing')
        level = request.POST.get('level', 'Beginner')
        
        batch_data = generate_skill_task(topic, level)
        if batch_data:
            tasks_list = []
            for t in batch_data.tasks:
                tasks_list.append({
                    'title': t.title,
                    'concept_summary': t.concept_summary,
                    'core_lessons': t.core_lessons,
                    'local_example': t.local_example,
                    'assignment_type': t.assignment_type,
                    'assignment_instruction': t.assignment_instruction,
                    'options': t.options,
                    'correct_options': t.correct_options,
                    'points': t.points_value
                })
            
            request.session['demo_batch'] = {
                'track_title': batch_data.track_title,
                'tasks': tasks_list
            }
            request.session['demo_evaluation'] = None
            messages.success(request, f"🎉 Loaded 3 runtime demo tasks for '{batch_data.track_title}'!")
        else:
            messages.error(request, "Failed to connect to the Gemini API engine.")

    elif 'submit_answer' in request.POST:
        task_type = request.POST.get('task_type')
        task_title = request.POST.get('task_title')
        
        if task_type == 'text':
            assignment_prompt = request.POST.get('assignment_prompt')
            student_answer = request.POST.get('student_answer', '').strip()
            
            if not student_answer:
                messages.error(request, "Please type a response before submitting.")
            else:
                ai_eval = evaluate_student_submission(assignment_prompt, student_answer)
                if ai_eval:
                    request.session['demo_evaluation'] = {
                        'task_title': task_title,
                        'is_correct': ai_eval.is_correct,
                        'feedback': ai_eval.feedback
                    }
                else:
                    messages.error(request, "The grading engine is unavailable.")
        else:
            selected_answers = request.POST.getlist('quiz_choices')
            correct_answers = request.POST.getlist('correct_choices')
            
            passed = sorted(selected_answers) == sorted(correct_answers)
            feedback_msg = "Excellent work! Accurate quiz arrays matching." if passed else f"Incorrect. Correct answer was: {', '.join(correct_answers)}."
            
            request.session['demo_evaluation'] = {
                'task_title': task_title,
                'is_correct': passed,
                'feedback': feedback_msg
            }

    elif 'reset_demo' in request.POST:
        request.session['demo_batch'] = None
        request.session['demo_evaluation'] = None
        messages.info(request, "Sandbox playground reset.")

    context = {
        'demo_batch': request.session.get('demo_batch'),
        'demo_evaluation': request.session.get('demo_evaluation')
    }
    return render(request, 'ai_demo.html', context)