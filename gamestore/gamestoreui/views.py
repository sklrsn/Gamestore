from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db import transaction
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse
from .forms import UserForm, UserProfileForm, UserProfileUpdateForm
import cloudinary


# Handle profile updates

@login_required
@transaction.atomic
def update_profile(request):
    try:
        if request.method == 'POST':
            profile_form = UserProfileUpdateForm(request.POST, instance=request.user.userprofile)
            if profile_form.is_valid():
                profile_form = profile_form.save(commit=False)
                if 'picture' in request.FILES:
                    profile_form.picture = request.FILES['picture']
                profile_form.save()
                messages.success(request, 'Your profile was successfully updated!')
                return render(request, 'profiles/success.html')
            else:
                messages.error(request, 'Please correct the error below.')
        else:
            profile_form = UserProfileUpdateForm()
        return render(request, 'profiles/update_profile.html', {
            'profile_form': profile_form
        })
    except Exception as e:
        print(e)
        return render(request, 'profiles/system_failure.html')


# Handle Password Reset

@login_required
def change_password(request):
    try:
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                return render(request, 'profiles/success.html')
            else:
                messages.error(request, 'Please correct the error below.')
        else:
            form = PasswordChangeForm(request.user)
        return render(request, 'profiles/change_password.html', {
            'form': form
        })
    except Exception as e:
        print(e)
        return render(request, 'profiles/system_failure.html')


# Handle Dynamic User Registration

def register_user(request):
    try:
        context = RequestContext(request)
        registered = False
        if request.method == 'POST':
            user_form = UserForm(data=request.POST)
            profile_form = UserProfileForm(data=request.POST)
            if user_form.is_valid() and profile_form.is_valid():
                user = user_form.save()
                user.set_password(user.password)
                user.save()
                profile = profile_form.save(commit=False)
                profile.user = user
                if 'picture' in request.FILES:
                    profile.picture = request.FILES['picture']
                else:
                    profile.picture = cloudinary.CloudinaryImage("sample", format="png")
                profile.save()
                registered = True
            else:
                print(user_form.errors, profile_form.errors)
        else:
            user_form = UserForm()
            profile_form = UserProfileForm()
        return render(request, 'profiles/register.html', {
            'user_form': user_form, 'profile_form': profile_form, 'registered': registered
        }, context)
    except Exception as e:
        print(e)
        return render(request, 'profiles/system_failure.html')


# Handle User Authentication

def user_login(request):
    try:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return render(request, 'profiles/success.html')
                else:
                    return HttpResponse("Your Game store account is disabled.")
            else:
                print(
                    "Invalid login details: {0}, {1}".format(username, password));
                return HttpResponse("Invalid login details")
        else:
            return render(request, 'profiles/login.html')
    except Exception as e:
        print(e)
        return render(request, 'profiles/system_failure.html')


# Handle Session Invalidation

@login_required
def user_logout(request):
    try:
        logout(request)
        return render(request, 'profiles/success.html')
    except Exception as e:
        print(e)
        return render(request, 'profiles/system_failure.html')
