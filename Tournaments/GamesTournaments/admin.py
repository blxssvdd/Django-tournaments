from django.contrib import admin

from .models import Tournament, Team, Player, Registration


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ("user", "tournament", "count")
    search_fields = ("user__username", "tournament__name")


admin.site.register([
    Tournament,
    Team,
    Player
])
