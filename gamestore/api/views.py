from django.core.urlresolvers import reverse, resolve
from django.http import JsonResponse

'''
    Returns list of available versions
    Supports only GET
'''
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
