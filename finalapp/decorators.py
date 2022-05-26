from django.http import Http404


def check_user_ability(*groups):
    def decorators(function):
        def wrapper(request, *args, **kwargs):
            if request.user.groups.filter(name__in=groups).exists():
                return function(request)
            raise Http404
        return wrapper
    return decorators
