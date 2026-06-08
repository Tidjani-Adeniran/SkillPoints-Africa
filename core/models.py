from django.db import models
from django.contrib.auth.models import User

# ==========================================================================
# 1. SKILL TRACK & TASK ENGINE MODELS
# ==========================================================================
class SkillTrack(models.Model):
    CATEGORY_CHOICES = [
        ('tech', 'Tech'),
        ('business', 'Business'),
        ('career', 'Career'),
    ]
    
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    points_awarded = models.IntegerField(default=100) 
    difficulty = models.CharField(max_length=50)      

    def __str__(self):
        return self.title
    
    
class Task(models.Model):
    track = models.ForeignKey(SkillTrack, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    title = models.CharField(max_length=200)
    learning_content = models.TextField(blank=True, null=True)  # 🚀 ADDED: Holds the AI-generated study material/lesson
    description = models.TextField()                            # Holds the practical assignment/assessment prompt
    points_value = models.IntegerField(default=25) 
    order = models.IntegerField(default=1)         

    def __str__(self):
        if self.track:
            return f"[{self.track.title}] - {self.title} ({self.points_value} SP)"
        return f"[Standalone AI Task] - {self.title} ({self.points_value} SP)"


class TaskCompletion(models.Model):  
    """Tracks assignment answers, AI grades, and feedback notes for try-again logic."""
    GRADING_STATUS = [
        ('PENDING', 'Under AI Review'),
        ('FAILED', 'Needs Revision (Try Again)'),
        ('PASSED', 'Passed (100% Competency)'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='completed_tasks')
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    
    # Assessment implementation fields
    submission_text = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=15, choices=GRADING_STATUS, default='PENDING')
    ai_feedback = models.TextField(blank=True, null=True)
    
    date_completed = models.DateTimeField(auto_now=True) # Automatically updates on every resubmission retry

    class Meta:
        unique_together = ('user', 'task')

    def __str__(self):
        return f"{self.user.username} - {self.task.title} [{self.status}]"


# ==========================================================================
# 2. MARKETPLACE REWARD ITEM MODEL
# ==========================================================================
class RewardItem(models.Model):
    title = models.CharField(max_length=200)
    vendor = models.CharField(max_length=200) 
    points_cost = models.IntegerField()
    stock_status = models.CharField(max_length=100, default="Available")
    icon_class = models.CharField(max_length=50, default="fa-utensils") 

    def __str__(self):
        return self.title


# ==========================================================================
# 3. USER PROFILE WALLET SYSTEM
# ==========================================================================
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    points_balance = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s Profile — {self.points_balance} SP"


# ==========================================================================
# 4. ENROLLMENT ENGINE BRIDGE MODEL
# ==========================================================================
class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('DIAGNOSTIC', 'Taking AI Assessment'),
        ('ACTIVE', 'Active Learning Tasks'),
        ('COMPLETED', 'Track Fully Concluded'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    track = models.ForeignKey(SkillTrack, on_delete=models.CASCADE, related_name='enrollments')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DIAGNOSTIC')
    date_started = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(null=True, blank=True)
    ai_chat_history = models.JSONField(default=dict, blank=True)

    class Meta:
        unique_together = ('user', 'track')

    def __str__(self):
        return f"{self.user.username} - {self.track.title} ({self.get_status_display()})"


# ==========================================================================
# 5. REDEMPTION TRANSACTION LEDGER
# ==========================================================================
class Redemption(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='redemptions')
    reward = models.ForeignKey(RewardItem, on_delete=models.CASCADE)
    date_redeemed = models.DateTimeField(auto_now_add=True)
    voucher_code = models.CharField(max_length=100, unique=True, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} redeemed {self.reward.title}"