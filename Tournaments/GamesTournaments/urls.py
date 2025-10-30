from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("add_tournament/", views.add_tournament, name="add_tournament"),
    path("tournaments/", views.get_tournaments, name="get_tournaments"),
    path("tournaments/paginated/", views.get_tournaments_paginated, name="get_tournaments_paginated"),
    path("tournaments/<int:tournament_id>/delete/", views.delete_tournament, name="delete_tournament"),
    path("add_team/", views.add_team, name="add_team"),
    path("teams/<int:team_id>/delete/", views.delete_team, name="delete_team"),
    path("teams/", views.get_teams, name="get_teams"),
    path("players/", views.get_players, name="get_players"),
    path("players/<int:player_id>/delete/", views.delete_player, name="delete_player"),
    path("add_player/", views.add_player, name="add_player")
]
