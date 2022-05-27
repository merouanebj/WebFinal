from django.shortcuts import get_object_or_404, redirect, render


def can_view_equipe(request):
    return 