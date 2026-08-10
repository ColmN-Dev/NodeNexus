from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm


def signup(request):
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created successfully! You can now log in.')
            return redirect('login')  # Redirect to the login page after successful signup
        
        else:
            messages.error(request, 'Please correct the details below.')
    else:
        form = UserRegisterForm()
    
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'You have been logged in successfully!')
            return redirect('profile')  # Redirect to the profile page after successful login
        
        else:
            messages.error(request, 'Invalid username or password. Please correct the details below.')
            
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('home')  # Redirect to the home page after logout

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

@login_required
def change_password(request):
    
    if request.method == 'POST':
        
        form = PasswordChangeForm(request.user, request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password has been changed successfully!')
            return redirect('profile')  # Redirect to the profile page after successful password change
        
        else:
            messages.error(request, 'Please correct the details below.')
    
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'accounts/change_password.html', {'form': form})