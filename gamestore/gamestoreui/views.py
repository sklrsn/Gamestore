from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db import transaction
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.http.response import HttpResponseRedirect, HttpResponse, JsonResponse
from .forms import UserForm, UserProfileForm, UserProfileUpdateForm, GameUploadForm
import cloudinary
from django.core.mail import send_mail
from gamestoredata.models import UserProfile, Game, Score, GameState
from django.contrib.auth.models import User


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
                return render(request, 'dashboard.html')
            else:
                messages.error(request, 'Please correct the error below.')
        else:
            profile_form = UserProfileUpdateForm()
        return render(request, 'profiles/update_profile.html', {
            'profile_form': profile_form
        })
    except Exception as e:
        print(e)
        return render(request, 'index.html')


# Handle Password Reset

def change_password(request):
    if request.user.is_authenticated():
        try:
            if request.method == 'POST':
                form = PasswordChangeForm(request.user, request.POST)
                if form.is_valid():
                    user = form.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, 'Your password was successfully updated!')
                    return render(request, 'dashboard.html')
                else:
                    messages.error(request, 'Please correct the error below.')
            else:
                form = PasswordChangeForm(request.user)
            return render(request, 'profiles/change_password.html', {
                'form': form
            })
        except Exception as e:
            print(e)
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')


# Handle Dynamic User Registration

def register_user(request):
    try:
        context = RequestContext(request)
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

                # Trigger an email
                user_email = request.POST.get('email', None)
                send_mail('Registration Successful', 'Welcome to Online Game store !!!!!!!!!!!!\n Regards,\n Admin',
                          "onlinegamestore999@gmail.com",
                          [user_email])
                return render(request, 'index.html')
            else:
                print(user_form.errors, profile_form.errors)
        else:
            user_form = UserForm()
            profile_form = UserProfileForm()
        return render(request, 'profiles/register.html', {
            'user_form': user_form, 'profile_form': profile_form}, context)
    except Exception as e:
        print(e)
        return render(request, 'index.html')


# Handle User Authentication

def user_login(request):
    if request.user.is_authenticated():
        return redirect('/profile/home')
    else:
        try:
            if request.method == 'POST':
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(username=username, password=password)
                if user:
                    if user.is_active:
                        login(request, user)
                        return redirect('/profile/home')
                    else:
                        return HttpResponse("Your Game store account is disabled.")
                else:
                    print(
                        "Invalid login details: {0}, {1}".format(username, password));
                    return render(request, 'index.html')
            else:
                return render(request, 'index.html')
        except Exception as e:
            print(e)
            return render(request, 'index.html')


# Handle Session Invalidation


def user_logout(request):
    try:
        if request.user.is_authenticated():
            logout(request)
        return render(request, 'index.html')
    except Exception as e:
        print(e)
        return render(request, 'index.html')


def index(request):
    try:
        return render(request, 'index.html')
    except Exception as e:
        print(e)
        return render(request, '400.html')


@login_required
def home(request):
    user = User.objects.get(username=request.user)
    current_user = UserProfile.objects.get(user=user)

    games_list = Game.objects.filter(developer_info=user)
    upload_form = GameUploadForm()
    return render(request, 'dashboard.html',
                  {'user_type': current_user.user_type, 'games_list': games_list, 'upload_form': upload_form})


# Allow the developer to upload a game to to the app store
@login_required
def upload_game(request):
    if request.method == 'GET':
        upload_form = GameUploadForm()
        return render(request, 'profiles/game_upload_form.html', {
            'upload_form': upload_form})
    else:
        user = User.objects.get(username=request.user)
        # check for the for logo attachment, if not available set the default logo
        if 'logo' in request.FILES:
            picture = request.FILES['logo']
        else:
            picture = cloudinary.CloudinaryImage("sample", format="png")
        upload_game_form = GameUploadForm(data=request.POST)
        if upload_game_form.is_valid():
            game = Game(id=None, name=upload_game_form.cleaned_data['name'],
                        description=upload_game_form.cleaned_data['description'],
                        logo=picture,
                        resource_info=upload_game_form.cleaned_data['resource_info'],
                        cost=upload_game_form.cleaned_data['cost'], developer_info=user)
            game.save()
        return redirect('/profile/home')
@login_required
def play_game(request,game_id):
    user = User.objects.get(username=request.user)
    current_user = UserProfile.objects.get(user=user)
    print('gameid = '+game_id)
    game = get_object_or_404(Game, id=game_id)
    if request.method == 'GET':
        leaders = Score.objects.filter(game_info=game).order_by("-score")[:5]
        leaderjson={}
        leaderjson=[ob.as_json_leader() for ob in leaders]
        print(game.to_json_dict())
        return render(request,"player.html",{'game': game.to_json_dict(),
                                                           'game_server': game.resource_info,'leaders': leaderjson})
    elif request.method == 'POST':
        response = {
            "error": None,
            "result": None
        }
        messageType = request.POST.get('messageType')
        #Do validations
        if messageType == 'SCORE':
            latestscore = request.POST.get('score');
            scoreobj = Score(id=None,score=latestscore,player_info=user,game_info=game);
            scoreobj.save()
            response['result'] = "Score saved successfully"
            return JsonResponse(status=201, data=response)
        elif messageType == 'SAVE':
            gamestate = request.POST.get('gameState');
            gameStateObj, created = GameState.objects.update_or_create(game = game, player = user, defaults={'app_state': gamestate},)
            #gameStateObj = GameState(id=None, game = game, player = user, app_state = gamestate)
            gameStateObj.save()
            response['result'] = None
            return JsonResponse(status=201, data=response)
        elif messageType == "LOAD_REQUEST":
            savedGame = GameState.objects.filter(player=user,game=game).order_by("last_modified")
            if savedGame.exists():
                response['result'] = savedGame[0].app_state
                return JsonResponse(status=200, data=response)
            else:
                response['result'] = None
                response['error'] = "There are no saved games."
                return JsonResponse(status=200, data=response)
        return HttpResponse(status=405, content="Invalid method specified.")
