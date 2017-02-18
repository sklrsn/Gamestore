from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
import datetime
from Users.models import UserProfile
from GameArena.models import Game, Score, GameState, Plays
from Store.models import Purchase
from GameArena.forms import GameUploadForm

"""
@Method_Name: play_game
@Param_in: Request , Game ID
@:returns: renders player page
Description: This view is for the player. GET request is used for loading the game and all other commmunication between the game and the backend is using POST ajax call

"""


# TODO - Commented code can be removed

@login_required
def play_game(request, game_id):
    user = User.objects.get(username=request.user)
    current_user = UserProfile.objects.get(user=user)
    game = get_object_or_404(Game, id=game_id)
    print(request.is_ajax)
    print(request.method)
    if request.method == 'GET':
        # Check if the user has purchased the game

        # TODO: Uncomment the below
        if not Purchase.objects.filter(game_details=game_id, player_details=user):
            messages.error(request, "You do not own this game. Why don't you buy it?")
            return HttpResponseRedirect(reverse("listgames"))
        plays = Plays(game=game, player=user)
        plays.save()

        leaders = Score.objects.filter(game_info=game).order_by("-score")[:5]
        leaderjson = {}
        leaderjson = [ob.as_json_leader() for ob in leaders]
        # print(game.to_json_dict())
        # if request.is_ajax():
        #     return render(request, "leaderboard.html", {'leaders': leaderjson})
        #     print('load request')
        return render(request, "users/player.html", {'game': game.to_json_dict(),
                                                     'game_server': game.resource_info, 'leaders': leaderjson,
                                                     'user_type': current_user.user_type})
    # for all ajax calls
    elif request.method == 'POST' and request.is_ajax():
        response = {
            "error": None,
            "result": None
        }
        messageType = request.POST.get('messageType')
        print('messageType:', request.POST.get('messageType'))

        # Saving score
        if messageType == 'SCORE':
            try:
                try:
                    latestscore = float(request.POST.get('score'))
                except:
                    response['error'] = "Invalid score. Try again."
                    return JsonResponse(status=200, data=response)
                scoreobj = Score(id=None, score=latestscore, player_info=user, game_info=game)
                scoreobj.save()
                response['result'] = None
                return JsonResponse(status=201, data=response)
            except Exception as e:
                response['error'] = "Error saving score. Try again."
                print(e)
                return JsonResponse(status=200, data=response)
        # Saving game state
        elif messageType == 'SAVE':
            gamestate = request.POST.get('gameState');
            try:
                gameStateObj, created = GameState.objects.update_or_create(game=game, player=user,
                                                                           defaults={'app_state': gamestate}, )
                # gameStateObj = GameState(id=None, game = game, player = user, app_state = gamestate)
                gameStateObj.save()
            except:
                response['error'] = "Error saving state. Try again."
                return JsonResponse(status=200, data=response)
            response['result'] = None
            return JsonResponse(status=201, data=response)
        # Loading game state
        elif messageType == "LOAD_REQUEST":
            try:
                savedGame = GameState.objects.filter(player=user, game=game).order_by("last_modified")
            except:
                response['error'] = "Error fetchin game. Try again."
                return JsonResponse(status=200, data=response)
            if savedGame.exists():
                response['result'] = savedGame[0].app_state
                return JsonResponse(status=200, data=response)
            else:
                response['result'] = None
                response['error'] = "There are no saved games."
                return JsonResponse(status=200, data=response)
        return HttpResponse(status=405, content="Invalid method specified.")


"""
@Method_name: listgames
@Param_in: Request
@returns: Renders game list
"""


def listgames(request):
    games_list = Game.objects.all()
    return render(request, 'gamearena/listgames.html',
                  {'games_list': games_list})


"""
@Method_Name: fb_redirect
@Param_in: Request
@returns: renders the FB redirect page
"""


def fb_redirect(request):
    # Simply closes the window
    return render(request, "gamearena/fb_redirect.html")


"""
@Method_Name: get_leaderboard
@Param_in: Request and game ID
@returns: renders leader board, in case of error HTTP error response
Description: This method returns the leaderboard table. It is used only to refresh the leaderboard table
"""


@login_required
def get_leaderboard(request, game_id):
    try:
        user = User.objects.get(username=request.user)
        if request.is_ajax():
            if not Purchase.objects.filter(game_details=game_id, player_details=user):
                return HttpResponse('You do not own the game')
            game = Game.objects.get(id=game_id)
            leaders = Score.objects.filter(game_info=game).order_by("-score")[:5]
            leaderjson = {}
            leaderjson = [ob.as_json_leader() for ob in leaders]
            return render(request, "gamearena/leaderboard.html", {'leaders': leaderjson})
    except:
        return HttpResponse('error handling request')
    return HttpResponse('error...')
