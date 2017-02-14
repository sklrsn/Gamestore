from django.shortcuts import render
from GameArena.models import Game, Score, GameState
from Users.models import UserProfile,User
from Store.models import Purchase
from api.cus_resp import *
from django.http import JsonResponse
import json


# Create your views here.
'''
    Gets the details of the game
'''
def get_game(request, game_id):
    if request.method == "GET":
            try:
                secretkey = request.GET.get('secretkey')
                try:
                    userprof = UserProfile.objects.filter(apikey=secretkey).first()
                except:
                    return KeyNotFound()
                game = Game.objects.filter(id=game_id,developer_info=userprof.user).first()
                if game is None:
                    return Error404("Either the game does not exit or you do not own the game")
            except Exception as ex:
                return InternalError()
            return JsonResponse(data=game.to_json_dict())

    else:
        return MethodNotAllowed()

'''
    Gets all the games
'''
def get_allgames(request):
    data={}
    if request.method == "GET":
        try:
            secretkey = request.GET.get('secretkey')
            try:
                userprof = UserProfile.objects.filter(apikey=secretkey).first()
            except:
                return KeyNotFound()
            games = userprof.user.uploaded_games.all()

            for game in games:
                data["id"] = game.id
                data["name"] = game.name
                data["cost"] = game.cost
        except Exception as ex:
            return InternalError()
        return JsonResponse(data=data)
    else:
        return MethodNotAllowed()

'''
    Gets all the leaders of a game
    Path : /api/v1/GetLeaders/<<game_id>>/?secretkey=<<secretkey>>&count=<<count>>
'''
def get_leaders(request,game_id):
    data={}
    if request.method == "GET":
        try:
            secretkey = request.GET.get('secretkey')
            count = request.GET.get('count',10)
            try:
                iCount = int(count)
            except:
                return Error406("Invalid count value.")
            try:
                userprof = UserProfile.objects.filter(apikey=secretkey).first()
            except:
                return KeyNotFound()
            game = Game.objects.filter(id=game_id,developer_info=userprof.user).first()
            if game is None:
                return Error404("Either the game does not exit or you do not own the game")

            leaders = Score.objects.filter(game_info=game).order_by("-score")[:iCount]
            leaderjson = {}
            leaderjson = [ob.as_json_leader() for ob in leaders]
        except Exception as ex:
            return InternalError(ex)
        return JsonResponse({'leaders': leaderjson})

    else:
        return MethodNotAllowed()
'''
    Gets all the purchases of a game
    /api/v1/GetPurchases/1/?secretkey=91969cd7e1e14e449bbaa8e388c01c39&count=10
'''
def get_purchases(request,game_id):
    data={}
    if request.method == "GET":
        try:
            secretkey = request.GET.get('secretkey')
            count = request.GET.get('count',10)
            try:
                iCount = int(count)
            except:
                return Error406("Invalid count value.")
            try:
                userprof = UserProfile.objects.filter(apikey=secretkey).first()
            except:
                return KeyNotFound()
            game = Game.objects.filter(id=game_id,developer_info=userprof.user).first()
            if game is None:
                return Error404("Either the game does not exit or you do not own the game")

            purchases = Purchase.objects.filter(game_details=game).order_by("-purchase_date")[:iCount]
            purchasejson = {}
            purchasejson = [ob.as_json_dict() for ob in purchases]
        except Exception as ex:
            return InternalError(ex)
        return JsonResponse({'purchases': purchasejson})

    else:
        return MethodNotAllowed()
