from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("add_tournament/", views.add_tournament, name="add_tournament"),
    path("tournaments/", views.get_tournaments, name="get_tournaments"),
    path("add_team/", views.add_team, name="get_team"),
    path("teams/", views.get_teams, name="get_teams"),
    path("players/", views.get_players, name="get_players"),
    path("add_player/", views.add_player, name="add_player")
]
