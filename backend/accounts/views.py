from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ProfileUpdateForm
from pathlib import Path
from django.conf import settings


PRESET_IMAGES = {
    'profile1': 'profile1.png',
    'profile2': 'profile2.png',
    'profile3': 'profile3.png',
    'profile4': 'profile4.png',
    'profile5': 'profile5.png',
    'profile6': 'profile6.png',
    'profile7': 'profile7.png',
    'profile8': 'profile8.png',
    'profile9': 'profile9.png',
}


def signup(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')

    else:
        form = UserRegisterForm()

    return render(request, 'accounts/signup.html', {'form': form})


@login_required
def profile(request):

    if request.method == 'POST':

        # Check if the user selected one of the preset images.
        preset_image = request.POST.get('preset_image')

        # If a preset was selected, handle the preset image.
        if preset_image in PRESET_IMAGES:

            # Set the user's profile image to the selected preset and save it.
            request.user.profile.preset_image = preset_image
            request.user.profile.save()

            messages.success(request, 'Profile picture updated successfully!')
            return redirect('profile')

        # If no preset was selected, handle a normal custom upload.
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if form.is_valid():
            profile = form.save(commit=False)
            profile.preset_image = ""
            profile.save()
            
            messages.success(request, 'Profile picture updated successfully!')
            return redirect('profile')

    else:
        # Display the current profile image when the page loads.
        form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'accounts/profile.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'You have been logged in successfully!')
            return redirect('profile')

        else:
            messages.error(request, 'Invalid username or password. Please correct the details below.')

    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('home')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Your password has been changed successfully!')
            return redirect('profile')

        else:
            messages.error(request, 'Please correct the details below.')

    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'accounts/change_password.html', {'form': form})