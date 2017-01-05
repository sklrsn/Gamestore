from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db import transaction
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse
from .forms import UserForm, UserProfileForm


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return render(request, 'profiles/success.html')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        profile_form = UserProfileForm()
    return render(request, 'profiles/update_profile.html', {
        'profile_form': profile_form
    })


def change_password(request):
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


def register_user(request):
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


def user_login(request):
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


@login_required
def user_logout(request):
    logout(request)
    return render(request, 'profiles/success.html')
