from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("api/tournaments/", views.tournaments_api, name="tournaments_api"),
    path("add_tournament/", views.add_tournament, name="add_tournament"),
    path("tournaments/<int:tournament_id>/edit/", views.edit_tournament, name="edit_tournament"),
    path("tournaments/", views.get_tournaments, name="get_tournaments"),
    path("tournaments/paginated/", views.get_tournaments_paginated, name="get_tournaments_paginated"),
    path("tournaments/<int:tournament_id>/delete/", views.delete_tournament, name="delete_tournament"),
    path("registrations/", views.my_registrations, name="my_registrations"),
    path("registrations/add/<int:tournament_id>/", views.add_to_registration, name="add_to_registration"),
    path("registrations/remove/<int:tournament_id>/", views.remove_registration, name="remove_registration"),
    path("add_team/", views.add_team, name="add_team"),
    path("teams/<int:team_id>/edit/", views.edit_team, name="edit_team"),
    path("teams/<int:team_id>/join/", views.join_team, name="join_team"),
    path("teams/<int:team_id>/leave/", views.leave_team, name="leave_team"),
    path("teams/<int:team_id>/delete/", views.delete_team, name="delete_team"),
    path("teams/", views.get_teams, name="get_teams"),
    path("players/", views.get_players, name="get_players"),
    path("players/<int:player_id>/delete/", views.delete_player, name="delete_player"),
    path("add_player/", views.add_player, name="add_player")
]
