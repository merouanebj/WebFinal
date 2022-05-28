from atexit import register
from django import template
from finalapp.models import *
register = template.Library()


@register.filter
def user_role(user):
    if Etablisment.objects.filter(chef_etablisement__id=user.id):
        return "chef_eta"
    if Division.objects.filter(chef_div__id=user.id):
        return "chef_div"
    if Equipe.objects.filter(chef_equipe__id=user.id):
        return "chef_equipe"
    return "simple_membre"
