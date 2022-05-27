from django.http import HttpResponse


def try_view(request):
    return HttpResponse("ok")
