from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import cloudinary
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
import datetime
import uuid
from django.core.exceptions import ObjectDoesNotExist
from .models import UserProfile
from GameArena.models import Game, Category
from .forms import UserProfileUpdateForm, RegistrationForm
from GameArena.forms import GameUploadForm
from Store.models import Purchase
import json
import itertools
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

'''
This view performs user authentication and creates a session between user and application

TODO: Even after we login to the home screen after login, it shows the login screen. If logged in it should take to
dashboard
'''

"""
@Method_Name: user_login
@Param_in: request
@:returns: renders index.html
"""


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
                        messages.error(request=request, message='Your Game store account is disabled.')
                        return HttpResponse("Your Game store account is disabled.")
                else:
                    messages.error(request=request, message='Invalid username or Password.')
                    return HttpResponseRedirect(redirect_to=reverse("index"))
            else:
                return HttpResponseRedirect(redirect_to=reverse("index"))
        except Exception as e:
            print(e)
            return HttpResponseRedirect(redirect_to=reverse("index"))


"""
@Method_Name: user_logout
@Param_in: request
@:returns: renders index.html
@Description: This view invalidates the user session
"""


@login_required
def user_logout(request):
    try:
        if request.user.is_authenticated():
            logout(request)
        return HttpResponseRedirect(redirect_to=reverse("index"))
    except Exception as e:
        print(e)
        return HttpResponseRedirect(redirect_to=reverse("index"))


"""
@Method_Name: index
@Param_in: request
@:returns: renders "Home" if user is authenticated, else "index.html"
@Description: This view renders Game store landing page
"""


def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("home")
    try:
        return render(request, 'users/index.html')
    except Exception as e:
        print(e)
        return render(request, 'errors/400.html')


"""
@Method_Name: home
@Param_in: request
@:returns: renders "dashboard"
@Description: This view renders the dashboard depends on the user type
"""


@login_required
def home(request):
    if request.user.userprofile.user_type == 'D':
        games_list = Game.objects.filter(developer_info=request.user)
    else:
        games_list = Purchase.objects.filter(player_details=request.user)
    upload_form = GameUploadForm()
    page_size = getattr(settings, "PAGE_SIZE", None)
    paginator = Paginator(games_list, int(page_size[0]))
    page = request.GET.get('page', int(page_size[0]))
    try:
        games = paginator.page(page)
    except PageNotAnInteger:
        games = paginator.page(int(page_size[0]))
    except EmptyPage:
        games = paginator.page(paginator.num_pages)

    return render(request, 'users/dashboard.html',
                  {'user_type': request.user.userprofile.user_type, 'games_list': games,
                   'upload_form': upload_form,
                   'current_user': request.user.userprofile})


"""
@Method_Name: home
@Param_in: request
@:returns: renders
@Description: This view allows the user change their password, upload a profile picture and share personal website/blog
information
"""


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
        return render(request, 'users/manage_profile.html', {
            'password_reset_form': password_reset_form, 'update_profile_form': update_profile_form,
            'user_type': request.user.userprofile.user_type, 'current_user': request.user.userprofile
        })
    except Exception as e:
        print(e)
        return HttpResponseRedirect(redirect_to=reverse('home'))


"""
@Method_Name: about_us
@Param_in: request
@:returns: renders  "about_us"
@Description: This method renders the information about the website and contributors
"""


def about_us(request):
    if request.user.is_authenticated():
        return render(request, 'users/about_us.html', {'user_type': request.user.userprofile.user_type})
    return render(request, 'users/about_us.html')


"""
@Method_Name: contact_us
@Param_in: request
@:returns: renders  "contact_us"
@Description: This method will render the contact us page information to users
"""


def contact_us(request):
    if request.user.is_authenticated():
        return render(request, 'users/contact_us.html', {'user_type': request.user.userprofile.user_type})
    return render(request, 'users/contact_us.html')


"""
@Method_Name: terms_conditions
@Param_in: request
@:returns: renders  "terms"
@Description: This method will render the terms page information to users
"""


def terms_conditions(request):
    return render(request, 'users/terms.html', {'time': datetime.datetime.now()})


"""
@Method_Name: register
@Param_in: request
@:returns: HTTP response based on the success or failure of the registration
@Description: Registration of the user
"""


@transaction.atomic
def register(request):
    if request.user.is_authenticated():
        messages.warning(request, "You are already logged in.")
        return HttpResponseRedirect(reverse('home'))

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if not form.is_valid():
            return render(request, "users/register.html", {'form': form})
        else:
            form.instance.is_active = False
            new_user = form.save()

            activation_token = uuid.uuid4()
            user_category = form.cleaned_data["user_type"]
            p = UserProfile(id=None, user=new_user,
                            picture=cloudinary.CloudinaryImage("sample", format="png"), user_type=user_category,
                            activation_token=activation_token)
            p.save()

            if form.cleaned_data["user_type"] == "D":
                developers = Group.objects.get(name='developers')
                developers.user_set.add(p.user)
            else:
                players = Group.objects.get(name='players')
                players.user_set.add(p.user)

        mail_title = 'Confirm your subscription!'
        message = 'Please visit the following link to complete your subscription: .... %s' % \
                  request.build_absolute_uri(reverse(viewname='activate', args=(activation_token,)))

        new_user.email_user(mail_title, message)

        messages.success(request=request, message='You have correctly registered to our portal. '
                                                  'An activation mail has been sent to your email account. '
                                                  'To log in, you will need to activate yourself by clicking '
                                                  'the activation link provided into that email.')
        return HttpResponseRedirect(reverse("index"))

    if request.method == 'GET':
        form = RegistrationForm()
        return render(request, "users/register.html", {
            'form': form,
        })


"""
@Method_Name: activate
@Param_in: request, activation_code (Default value "none")
@:returns: HTTP response based on the success or failure of the activation
@Description: Activation of the user
"""


def activate(request, activation_code=None):
    if request.method == 'GET':
        if not is_uuid_valid(activation_code):
            messages.error(request=request, message='The activation id provided is invalid.')
        else:
            p = None
            try:
                with transaction.atomic():
                    p = UserProfile.objects.get(activation_token=activation_code)
                    if p.user.is_active:
                        messages.error(request=request, message='Your account has already been activated.')
                    else:
                        p.user.is_active = True
                        p.user.save()
                        messages.success(request=request, message='You have correctly activated your account!')

            except ObjectDoesNotExist:
                messages.error(request=request, message='There was a problem during activation. Please try again.')

        return HttpResponseRedirect(redirect_to=reverse("home"))


"""
@Method_Name: is_uuid_valid
@Param_in: uuid String
@:returns: Boolean value 'True' if success else  'False'
@Description: validates the uuid string
"""


def is_uuid_valid(uuid_str):
    try:
        uuid.UUID(uuid_str, version=4)
        return True
    except:
        return False


"""
@Method_Name: forgot_password
@Param_in: request
@:returns: HTTP response
@Description: handles the forgot password scenario
"""


def forgot_password(request):
    if request.method == 'POST':
        try:
            app_user = User.objects.get(email=request.POST['email_address'])
            new_password = User.objects.make_random_password(length=12)
            app_user.set_password(new_password)
            app_user.save()
            mail_title = 'OnlineGameStore portal Password Reset'
            message = 'Your Password has been reset to the following..' + '\n Password:' + new_password

            app_user.email_user(mail_title, message)
            messages.success(request=request, message='We have sent your credentials to the registered email address '
                                                      'If you cannot find in your inbox, Please check your spam folder')
            return HttpResponseRedirect(redirect_to=reverse("index"))
        except ObjectDoesNotExist:
            messages.error(request=request, message='Please enter the registered  email address ')
    else:
        return HttpResponseRedirect(redirect_to=reverse("index"))


"""
@Method_Name: upload_game
@Param_in: request
@:returns: HTTP response - redirected to "home"
@Description: handles the uploading of a game scenario
"""


@login_required
def upload_game(request):
    if request.method == 'GET':
        upload_form = GameUploadForm()
        return render(request, 'users/game_upload_form.html', {
            'upload_form': upload_form})
    else:
        user = User.objects.get(username=request.user)
        upload_game_form = GameUploadForm(data=request.POST)
        if upload_game_form.is_valid():
            category = Category.objects.get(name=upload_game_form.cleaned_data['game_category'])
            game = Game(id=None, name=upload_game_form.cleaned_data['name'],
                        description=upload_game_form.cleaned_data['description'],
                        logo=upload_game_form.cleaned_data['logo'],
                        resource_info=upload_game_form.cleaned_data['resource_info'],
                        cost=upload_game_form.cleaned_data['cost'],
                        modified_date=datetime.datetime.now(), developer_info=user, game_category=category)
            game.save()
            return HttpResponseRedirect(redirect_to=reverse('home'))


"""
@Method_Name: edit_game
@Param_in: request,game_id
@:returns: renders edit_game
@Description: handles the editing of existing game scenario
"""


@login_required
def edit_game(request, game_id):
    if request.method == 'GET':
        game = get_object_or_404(Game, id=game_id, developer_info=request.user)
        form = GameUploadForm(instance=game)
        return render(request, 'users/edit_game.html',
                      {'form': form, 'user': request.user, 'user_type': request.user.userprofile.user_type})

    if request.method == 'POST':
        game_form = GameUploadForm(data=request.POST)

        if game_form.is_valid() and request.POST['action'].lower() == 'update':
            category = Category.objects.get(name=game_form.cleaned_data['game_category'])
            game = Game(id=game_id, game_category=category,
                        name=game_form.cleaned_data['name'],
                        description=game_form.cleaned_data['description'],
                        logo=game_form.cleaned_data['logo'],
                        resource_info=game_form.cleaned_data['resource_info'],
                        cost=game_form.cleaned_data['cost'],
                        modified_date=datetime.datetime.now(), developer_info=request.user)
            game.save()
            messages.success(request=request, message='Game updated successfully.')
            return HttpResponseRedirect(redirect_to=reverse('home'))

        elif game_form.is_valid() and request.POST['action'].lower() == 'delete':
            Game.objects.filter(id=game_id, developer_info=request.user).delete()
            messages.success(request=request, message='Game removed successfully.')
            return HttpResponseRedirect(redirect_to=reverse('home'))

        else:
            return HttpResponseRedirect(redirect_to=reverse('home'))
    else:
        return HttpResponseRedirect(redirect_to=reverse('home'))


"""
@Method_Name: download_statistics
@Param_in: request
@:returns: returns JSON response
@Description: statistics related to the games are handled
"""


def download_statistics(request):
    if request.is_ajax():
        if request.GET['type'] == 'pie-overall':
            games_list = Game.objects.filter(developer_info=request.user)
            stats = dict()

            for game in games_list:
                stats[game.id] = (game.name, len(Purchase.objects.filter(game_details=game)))
            return JsonResponse(stats)

        elif request.GET['type'] == 'pie-range':
            from_date = request.GET['from_date']
            to_date = request.GET['to_date']
            start = None
            end = None
            try:
                start = datetime.datetime.strptime(from_date, "%m/%d/%Y")
            except ValueError:
                return HttpResponse(status=400, content=json.dumps({'error', 'Invalid parameter from_date'}),
                                    content_type="text/json")

            try:
                end = datetime.datetime.strptime(to_date, "%m/%d/%Y")
            except ValueError:
                return HttpResponse(status=400, content=json.dumps({'error', 'Invalid parameter to_date'}),
                                    content_type="text/json")

            if start > end:
                return HttpResponse(status=400,
                                    content=json.dumps({'error', 'from_date cannot be greater than to_date'}),
                                    content_type="text/json")
            end = datetime.datetime.date(end) + datetime.timedelta(days=1)
            stats = dict()
            games_list = Game.objects.filter(developer_info=request.user)
            for game in games_list:
                stats[game.id] = (
                    game.name,
                    len(Purchase.objects.filter(game_details=game, purchase_date__lte=end, purchase_date__gte=start)))
            return JsonResponse(stats)
        elif request.GET['type'] == 'line-overall':
            stats = dict()
            stats['labels'] = []
            stats['dataset'] = []

            jobs = Purchase.objects.filter()
            data = itertools.groupby(jobs, lambda record: record.purchase_date.strftime("%Y-%m-%d"))
            purchase_by_day = [(day, len(list(purchase_this_day))) for day, purchase_this_day in data]

            for d in purchase_by_day:
                stats['labels'].append(d[0])
                stats['dataset'].append(d[1])
            return JsonResponse(stats)

    return render(request, 'users/statistics.html', {'user_type': request.user.userprofile.user_type})


"""
@Method_Name: generate_developer_key
@Param_in: request
@:returns: returns HTTP response - redirected to home
@Description: generates a new developer key
"""


def generate_developer_key(request):
    user_profile = request.user.userprofile
    user_profile.apikey = uuid.uuid4()
    user_profile.save()
    return HttpResponseRedirect(reverse("manage_profile"))


@transaction.atomic
def register_social_profile(backend, user, response, *args, **kwargs):
    try:
        if backend.name == 'facebook':
            if not UserProfile.objects.filter(user=user).exists():
                print('creating profile')
                # Create user profile
                activation_token = uuid.uuid4()
                p = UserProfile(id=None, user=user,
                                picture=cloudinary.CloudinaryImage("sample", format="png"), user_type='P',
                                activation_token=activation_token)
                p.save()
    except Exception as e:
        print(e)
