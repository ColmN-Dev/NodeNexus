from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth import login, logout

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
            return redirect('home')  # Redirect to the home page after successful login
        
        else:
            messages.error(request, 'Invalid username or password. Please correct the details below.')
            
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('home')  # Redirect to the home page after logout
