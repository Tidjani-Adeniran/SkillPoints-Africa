from django.contrib import admin
from .models import SkillTrack, RewardItem, UserProfile, Enrollment, Redemption
from .models import SkillTrack, RewardItem, UserProfile, Enrollment, Redemption, Task, TaskCompletion

# Register your models here.
admin.site.register(SkillTrack)
admin.site.register(RewardItem)
admin.site.register(UserProfile)
admin.site.register(Enrollment)
admin.site.register(Redemption)
admin.site.register(Task)
admin.site.register(TaskCompletion)