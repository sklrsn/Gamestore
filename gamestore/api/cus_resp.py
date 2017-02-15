from django.http import JsonResponse


"""
@Method_Name: InternalError
@Param_in: Error (Default value "None")
@:returns: JSON response with status code "500"
"""


def InternalError(error=None):
    if error is None:
        error="We encountered an internal error. Please try again."
    data = {
        "error": error
    }
    return JsonResponse(status=500, data=data)

"""
@Method_Name: MethodNotAllowed
@Param_in: Error (Default value "None")
@:returns: JSON response with status code "405"
"""


def MethodNotAllowed(error=None):
    if error is None:
        error="The specified method is not allowed against this resource."
    data = {
        "error": error
    }
    return JsonResponse(status=405, data=data)

"""
@Method_Name: KeyNotFound
@Param_in: Error (Default value "None")
@:returns: JSON response with status code "404"
"""


def KeyNotFound(error=None):
    if error is None:
        error="The specified key does not exist or is invalid."
    data = {
        "error": error
    }
    return JsonResponse(status=404, data=data)

"""
@Method_Name: Error404
@Param_in: Error (Default value "None")
@:returns: JSON response with status code "404"
"""


def Error404(error=None):
    if error is None:
        error="The specified resource does not exist."
    data = {
        "error": error
    }
    return JsonResponse(status=404, data=data)


"""
@Method_Name: Error406
@Param_in: Error (Default value "None")
@:returns: JSON response with status code "406"
"""


def Error406(error=None):
    if error is None:
        error="Invalid input."
    data = {
        "error": error
    }
    return JsonResponse(status=406, data=data)
