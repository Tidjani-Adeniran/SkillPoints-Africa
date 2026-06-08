from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
# Import your Core Point wallet model across app boundaries
from core.models import UserProfile 

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Instantly inject their custom point balance container profile 
            UserProfile.objects.create(user=user, points_balance=0)
            
            messages.success(request, "Sign up successful! Welcome to SkillPoints Africa.")
            return redirect('dashboard') 
    else:
        form = UserCreationForm()
        
    # FIX: Added 'accounts/' so Django looks inside accounts/templates/accounts/
    return render(request, 'accounts/signup.html', {'form': form})