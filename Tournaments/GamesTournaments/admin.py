from django.contrib import admin

from .models import Tournament, Team, Player

# Register your models here.


admin.site.register([
    Tournament,
    Team,
    Player
])
