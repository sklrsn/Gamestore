from django.http import HttpRequest, HttpResponse, Http404
import json


def store_game_score(request):
    data = "Yet to Implement the service"

    callback = request.GET.get('callback')
    if callback is not None:
        data = '%s(%s);' % (callback, json.dumps(data))

    return HttpResponse(json.dumps(data), content_type='application/json')


def load_game_score(request):
    data = "Yet to Implement the service"

    if request.is_ajax():
        data = "Ajax call has been Made here"

    return HttpResponse(json.dumps(data), content_type='application/json')


def store_game_state(request):
    data = "Yet to Implement the service"
    return HttpResponse(json.dumps(data), content_type='application/json')


def load_game_state(request):
    data = "Yet to Implement the service"
    return HttpResponse(json.dumps(data), content_type='application/json')


def store_system_configs(request):
    data = "Yet to Implement the service"
    return HttpResponse(json.dumps(data), content_type='application/json')


def load_system_configs(request):
    data = "Yet to Implement the service"
    return HttpResponse(json.dumps(data), content_type='application/json')
