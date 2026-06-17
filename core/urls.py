from django.urls import path
from .views import SuccessMessageLoginView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('about/', views.about_page, name='about'),
    path('login/', SuccessMessageLoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('enroll/<int:track_id>/', views.enroll_in_track, name='enroll_in_track'),
    
    # 🛒 Marketplace Vouchers
    path('marketplace/', views.all_rewards, name='all_marketplace'),
    path('marketplace/redeem/<int:reward_id>/', views.redeem_reward, name='redeem_reward'),
    
    # 📚 Course Catalog & Learning Workspace
    path('tracks/', views.all_tracks, name='all_tracks'),
    path('workspace/<int:enrollment_id>/', views.track_workspace, name='track_workspace'),
    path('workspace/task/<int:task_id>/complete/', views.complete_workspace_task, name='complete_workspace_task'),
    
    # 🧑‍💼 Exclusive Admin Panel Operations (Hidden from Students)
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/generate/<int:track_id>/', views.generate_track_content, name='generate_track_content'),
    # Fixed: changed <int:completion_id> to <int:submission_id> to match views.py parameter perfectly
    path('admin-dashboard/review/<int:submission_id>/', views.approve_submission, name='approve_submission'),
]