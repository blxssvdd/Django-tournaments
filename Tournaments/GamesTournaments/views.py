from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .forms import TournamentForm, TeamForm, PlayerForm
from .models import Tournament, Team, Player

# Create your views here.


def index(request):
    featured_tournaments = [
        {
            "name": "Кубок Легенд",
            "count": 5,
            "date": "2023-10-01",
            "players": 20
        },
        {
            "name": "Masters Arena",
            "count": 3,
            "date": "2023-10-15",
            "players": 15
        },
        {
            "name": "Зимовий Челлендж",
            "count": 4,
            "date": "2023-11-01",
            "players": 25
        }
    ]
    tournaments = Tournament.objects.all().order_by("-date", "name")
    return render(
        request=request,
        template_name="index.html",
        context={
            "featured_tournaments": featured_tournaments,
            "all_tournaments": tournaments
        }
    )


@login_required(login_url="/users/sign_in/")
def add_tournament(request):
    form = TournamentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        name = form.cleaned_data["name"]
        location = form.cleaned_data["location"]
        description = form.cleaned_data["description"]
        date = form.cleaned_data["date"]
        tournament = Tournament(name=name, location=location, description=description, date=date)
        tournament.save()
        return redirect("get_tournaments")
    return render(request=request, template_name="add_tournament.html", context=dict(form=form))


def get_tournaments(request):
    tournaments = Tournament.objects.all().order_by("-date", "name")
    return render(request=request, template_name="tournaments.html", context=dict(tournaments=tournaments))


def get_tournaments_paginated(request):
    tournaments = Tournament.objects.all().order_by("-date", "name")
    paginator = Paginator(tournaments, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request=request,
        template_name="tournaments_paginated.html",
        context=dict(page_obj=page_obj)
    )


def get_players(request):
    return render(
        request=request,
        template_name="players.html",
        context=dict(players=Player.objects.select_related("team__tournament").all())
    )


@login_required(login_url="/users/sign_in/")
def add_player(request):
    form = PlayerForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        name = form.cleaned_data.get("name")
        description = form.cleaned_data.get("description")
        team = form.cleaned_data.get("team")
        player = Player(
            name=name,
            description=description,
            team=team
        )
        player.save()
        return redirect("get_players")

    return render(
        request=request,
        template_name="add_player.html",
        context=dict(form=form)
    )


def get_teams(request):
    return render(
        request=request,
        template_name="teams.html",
        context=dict(teams=Team.objects.select_related("tournament").all())
    )


@login_required(login_url="/users/sign_in/")
def add_team(request):
    form = TeamForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        name = form.cleaned_data.get("name")
        description = form.cleaned_data.get("description")
        tournament = form.cleaned_data.get("tournament")
        team = Team(
            name=name,
            description=description,
            tournament=tournament
        )
        team.save()
        return redirect("get_teams")

    return render(
        request=request,
        template_name="add_team.html",
        context=dict(form=form)
    )


@login_required(login_url="/users/sign_in/")
@require_POST
def delete_tournament(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    tournament.delete()
    messages.success(request, "Турнір видалено.")
    return redirect("get_tournaments")


@login_required(login_url="/users/sign_in/")
@require_POST
def delete_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    team.delete()
    messages.success(request, "Команду видалено.")
    return redirect("get_teams")


@login_required(login_url="/users/sign_in/")
@require_POST
def delete_player(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    player.delete()
    messages.success(request, "Гравця видалено.")
    return redirect("get_players")

