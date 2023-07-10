from django.core.exceptions import PermissionDenied


def is_client(user):
    return hasattr(user, 'client')


def is_freelancer(user):
    return hasattr(user, 'freelancer')


def client_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not is_client(request.user):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper


def freelancer_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not is_freelancer(request.user):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper
