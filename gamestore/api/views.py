from django.core.urlresolvers import reverse, resolve
from django.http import JsonResponse


"""
@Method_Name:versions
@Param_in: request
@:returns: JSON Response in the case of request method not being get, else the URI of available versions
@Description:     Returns list of available versions, Supports only GET
"""


def versions(request):
    if request.method == "GET":
        return JsonResponse({
            'urls': {
                # 'v1':request.build_absolute_uri(reverse('v1')),
                'latest': request.build_absolute_uri()
            }
        })
    else:
        return JsonResponse(status=405, data=None)
