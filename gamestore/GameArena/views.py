from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
import datetime
from Users.models import UserProfile
from GameArena.models import Game, Score, GameState
from Store.models import Purchase
from GameArena.forms import GameUploadForm

'''
    This view is for the player.
    GET request is used for loading the game and all other commmunication between the game and the backend is using POST ajax call
'''


@login_required
def play_game(request, game_id):
    user = User.objects.get(username=request.user)
    current_user = UserProfile.objects.get(user=user)
    print('gameid = ' + game_id)
    game = get_object_or_404(Game, id=game_id)
    if request.method == 'GET':

        # Check if the user has purchased the game
        perm = Purchase.objects.filter(game_details=game_id, player_details=user)
        # TODO: Uncomment the below if
        # if not Purchase.objects.filter(game_details=game_id, player_details= user):
        #     messages.error(request, "You do not own this game. Why don't you buy it?")
        #     return HttpResponseRedirect(reverse("listgames"))
        leaders = Score.objects.filter(game_info=game).order_by("-score")[:5]
        leaderjson = {}

        leaderjson = [ob.as_json_leader() for ob in leaders]
        print(game.to_json_dict())
        return render(request, "player.html", {'game': game.to_json_dict(),
                                               'game_server': game.resource_info, 'leaders': leaderjson})
    # for all ajax calls
    elif request.method == 'POST' and request.is_ajax():
        response = {
            "error": None,
            "result": None
        }
        messageType = request.POST.get('messageType')
        print('messageType:',request.POST.get('messageType'))

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


def listgames(request):
    games_list = Game.objects.all()
    return render(request, 'listgames.html',
                  {'games_list': games_list})


def fb_redirect(request):
    # Simply closes the window
    return render(request, "fb_redirect.html")
