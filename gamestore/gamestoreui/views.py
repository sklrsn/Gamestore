from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db import transaction
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import UserForm, UserProfileForm, UserProfileUpdateForm, GameUploadForm
import cloudinary
from gamestoredata.models import UserProfile, Game, Score, GameState
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
import datetime


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
                        return HttpResponseRedirect(redirect_to=reverse('home'))
                    else:
                        return HttpResponse("Your Game store account is disabled.")
                else:
                    print(
                        "Invalid login details: {0}, {1}".format(username, password))
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

        upload_game_form = GameUploadForm(data=request.POST)
        if upload_game_form.is_valid():
            game = Game(id=None, name=upload_game_form.cleaned_data['name'],
                        description=upload_game_form.cleaned_data['description'],
                        logo=upload_game_form.cleaned_data['logo'],
                        resource_info=upload_game_form.cleaned_data['resource_info'],
                        cost=upload_game_form.cleaned_data['cost'],
                        modified_date=datetime.datetime.now(), developer_info=user)
            game.save()
            return HttpResponseRedirect(redirect_to=reverse('home'))


@login_required
def play_game(request, game_id):
    user = User.objects.get(username=request.user)
    current_user = UserProfile.objects.get(user=user)
    print('gameid = ' + game_id)
    game = get_object_or_404(Game, id=game_id)
    if request.method == 'GET':
        leaders = Score.objects.filter(game_info=game).order_by("-score")[:5]
        leaderjson = {}
        leaderjson = [ob.as_json_leader() for ob in leaders]
        print(game.to_json_dict())
        return render(request, "player.html", {'game': game.to_json_dict(),
                                               'game_server': game.resource_info, 'leaders': leaderjson})
    elif request.method == 'POST':
        response = {
            "error": None,
            "result": None
        }
        messageType = request.POST.get('messageType')
        # Do validations
        if messageType == 'SCORE':
            latestscore = request.POST.get('score')
            scoreobj = Score(id=None, score=latestscore, player_info=user, game_info=game)
            scoreobj.save()
            response['result'] = "Score saved successfully"
            return JsonResponse(status=201, data=response)
        elif messageType == 'SAVE':
            gamestate = request.POST.get('gameState');
            gameStateObj, created = GameState.objects.update_or_create(game=game, player=user,
                                                                       defaults={'app_state': gamestate}, )
            # gameStateObj = GameState(id=None, game = game, player = user, app_state = gamestate)
            gameStateObj.save()
            response['result'] = None
            return JsonResponse(status=201, data=response)
        elif messageType == "LOAD_REQUEST":
            savedGame = GameState.objects.filter(player=user, game=game).order_by("last_modified")
            if savedGame.exists():
                response['result'] = savedGame[0].app_state
                return JsonResponse(status=200, data=response)
            else:
                response['result'] = None
                response['error'] = "There are no saved games."
                return JsonResponse(status=200, data=response)
        return HttpResponse(status=405, content="Invalid method specified.")


@login_required
def edit_game(request, game_id):
    if request.method == 'GET':
        game = get_object_or_404(Game, id=game_id, developer_info=request.user)
        form = GameUploadForm(instance=game)
        return render(request, 'edit_game.html', {'form': form, 'user': request.user})

    if request.method == 'POST':
        game_form = GameUploadForm(data=request.POST)
        user = User.objects.get(username=request.user)

        if game_form.is_valid() and request.POST['action'].lower() == 'save':
            game = Game(id=game_id, name=game_form.cleaned_data['name'],
                        description=game_form.cleaned_data['description'],
                        logo=game_form.cleaned_data['logo'],
                        resource_info=game_form.cleaned_data['resource_info'],
                        cost=game_form.cleaned_data['cost'],
                        modified_date=datetime.datetime.now(), developer_info=user)
            game.save()
            messages.success(request=request, message='Game updated successfully.')
            return HttpResponseRedirect(redirect_to=reverse('home'))

        elif game_form.is_valid() and request.POST['action'].lower() == 'delete':
            Game.objects.filter(id=game_id, developer_info=user).delete()
            messages.success(request=request, message='Game removed successfully.')
            return HttpResponseRedirect(redirect_to=reverse('home'))

        else:
            print('Invalid Request')
            return HttpResponseRedirect(redirect_to=reverse('home'))
    else:
        return HttpResponseRedirect(redirect_to=reverse('home'))


# Handle user profile and password updates
@login_required
@transaction.atomic
def manage_profile(request):
    try:
        if request.method == 'POST':
            password_reset_form = PasswordChangeForm(request.user, request.POST)
            update_profile_form = UserProfileUpdateForm(request.POST, instance=request.user.userprofile)
            if password_reset_form.is_valid() and update_profile_form.is_valid():
                user = password_reset_form.save()
                update_session_auth_hash(request, user)
                update_profile_form = update_profile_form.save(commit=False)
                if 'picture' in request.FILES:
                    update_profile_form.picture = request.FILES['picture']
                    update_profile_form.save()
                messages.success(request, 'Your Profile updated successfully !')
                return HttpResponseRedirect(redirect_to=reverse('home'))
            else:
                messages.error(request, 'Please correct the error below.')
        else:
            password_reset_form = PasswordChangeForm(request.user)
            update_profile_form = UserProfileUpdateForm()
        return render(request, 'profiles/manage_profile.html', {
            'password_reset_form': password_reset_form, 'update_profile_form': update_profile_form
        })
    except Exception as e:
        print(e)
        return HttpResponseRedirect(redirect_to=reverse('home'))

    return HttpResponseRedirect(redirect_to=reverse('home'))
