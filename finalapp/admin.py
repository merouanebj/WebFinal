from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *

admin.site.register(Researcher), 
admin.site.register(Location),
admin.site.register(Etablisment),
admin.site.register(Division),
admin.site.register(Laboratoire),
admin.site.register(Equipe),
admin.site.register(Directions),