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
    """
    Enhanced to support dynamic task assignments (text, quizzes, checkboxes).
    Includes an approval toggle to hide AI drafts until the admin vets them.
    """
    ASSIGNMENT_TYPES = [
        ('text', 'Manual Text Submission'),
        ('multiple_choice', 'Multiple Choice (Single Option)'),
        ('checkbox', 'Checkbox Selection (Multiple Options)'),
    ]

    track = models.ForeignKey(SkillTrack, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    title = models.CharField(max_length=200)
    learning_content = models.TextField(blank=True, null=True)  # Holds the AI-generated textbook/lesson text
    concept_summary = models.TextField(blank=True, null=True)   # Short 1-2 sentence breakdown
    local_example = models.TextField(blank=True, null=True)     # Regional/African business context case study
    
    # Structural changes for dynamic assessments
    assignment_type = models.CharField(max_length=20, choices=ASSIGNMENT_TYPES, default='text')
    description = models.TextField(help_text="Holds the practical assignment/assessment prompt question.") 
    
    # JSON arrays safely supported by SQLite/PostgreSQL
    options = models.JSONField(default=list, blank=True, help_text="List of choices for quizzes. Leave empty for text.")
    correct_options = models.JSONField(default=list, blank=True, help_text="Exact matching text choices that equal success.")
    
    points_value = models.IntegerField(default=25) 
    order = models.IntegerField(default=1)         
    is_approved = models.BooleanField(default=False)  # 🔥 Hidden from students until you click publish inside the admin workspace

    def __str__(self):
        status = "Live" if self.is_approved else "Draft Blueprint"
        if self.track:
            return f"[{self.track.title}] - {self.title} ({status} - {self.points_value} SP)"
        return f"[Standalone AI Task] - {self.title} ({status})"


class TaskCompletion(models.Model):  
    """
    Tracks answers, grades, and feedback notes. Updated to transition 
    from 'AI Review' definitions to a pure 'Admin Vetting' architecture.
    """
    GRADING_STATUS = [
        ('PENDING', 'Under Admin Review'),  # For manual text submissions awaiting your click
        ('FAILED', 'Needs Revision (Try Again)'),
        ('PASSED', 'Passed (100% Competency)'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='completed_tasks')
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    
    # Holds submitted string text, or string arrays for multiple choice selections
    submission_text = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=15, choices=GRADING_STATUS, default='PENDING')
    admin_feedback = models.TextField(blank=True, null=True)  # Personalized notes you leave for manual reviews
    
    date_completed = models.DateTimeField(auto_now=True) 

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