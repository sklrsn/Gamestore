from django.http import JsonResponse

def InternalError(error=None):
    if error is None:
        error="We encountered an internal error. Please try again."
    data = {
        "error": error
    }
    return JsonResponse(status=500, data=data)

def MethodNotAllowed(error=None):
    if error is None:
        error="The specified method is not allowed against this resource."
    data = {
        "error": error
    }
    return JsonResponse(status=405, data=data)

def KeyNotFound(error=None):
    if error is None:
        error="The specified key does not exist or is invalid."
    data = {
        "error": error
    }
    return JsonResponse(status=404, data=data)

def Error404(error=None):
    if error is None:
        error="The specified resource does not exist."
    data = {
        "error": error
    }
    return JsonResponse(status=404, data=data)

def Error406(error=None):
    if error is None:
        error="Invalid input."
    data = {
        "error": error
    }
    return JsonResponse(status=406, data=data)
