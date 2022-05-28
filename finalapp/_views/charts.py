from django.http import HttpResponse
from django.shortcuts import render


def try_view(request):
    return render(request, 'try.html')
