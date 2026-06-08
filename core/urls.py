from django.urls import path
from .views import SuccessMessageLoginView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', SuccessMessageLoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('enroll/<int:track_id>/', views.enroll_in_track, name='enroll_in_track'),
    
    # 🛒 Marketplace Vouchers
    path('marketplace/', views.all_rewards, name='all_marketplace'),
    path('marketplace/redeem/<int:reward_id>/', views.redeem_reward, name='redeem_reward'),
    
    # 📚 Course Catalog & Learning Workspace
    path('tracks/', views.all_tracks, name='all_tracks'),
    path('workspace/<int:enrollment_id>/', views.track_workspace, name='track_workspace'),
    path('workspace/task/<int:task_id>/complete/', views.complete_workspace_task, name='complete_workspace_task'),
]