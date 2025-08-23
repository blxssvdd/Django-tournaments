from django.shortcuts import render, redirect

from .forms import TournamentForm, TeamForm, PlayerForm
from .models import Tournament, Team, Player

# Create your views here.


def index(request):
    context = {
        "tournaments": [
            {
                "name": "Турнір 1",
                "count": 5,
                "date": "2023-10-01",
                "players": 20
            },
            {
                "name": "Турнір 2",
                "count": 3,
                "date": "2023-10-15",
                "players": 15
            },
            {
                "name": "Турнір 3",
                "count": 4,
                "date": "2023-11-01",
                "players": 25
            }

    ]}
    return render(request=request, template_name="index.html", context=context)


def add_tournament(request):
    if request.method != "POST":
        form = TournamentForm()
        return render(request=request, template_name="add_tournament.html", context=dict(form=form))

    form = TournamentForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data["name"]
        location = form.cleaned_data["location"]
        description = form.cleaned_data["description"]
        tournament = Tournament(name=name, location=location, description=description)
        tournament.save()
        return redirect("get_tournaments")


def get_tournaments(request):
    tournaments = Tournament.objects.all()
    return render(request=request, template_name="tournaments.html", context=dict(tournaments=tournaments))


def get_players(request):
    return render(
        request=request,
        template_name="players.html",
        context=dict(players=Player.objects.all())
    )


def add_player(request):
    if request.method == "POST":
        form = PlayerForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            description = form.cleaned_data.get("description")
            team = form.cleaned_data.get("team")
            tournaments = form.cleaned_data.get("tournaments")
            player = Player(
                name=name,
                description=description,
                team=team,
                tournaments=tournaments
            )
            player.save()
            player.tournaments.set(tournaments)
            return redirect("get_players")

        return redirect("add_player")



    return render(
        request=request,
        template_name="add_player.html",
        context=dict(form=PlayerForm())
    )



def get_teams(request):
    return render(
        request=request,
        template_name="teams.html",
        context=dict(teams=Team.objects.all())
    )


def add_team(request):
    if request.method == "POST":
        form = TeamForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            description = form.cleaned_data.get("description")
            players = form.cleaned_data.get("players")
            tournament = form.cleaned_data.get("tournament")
            team = Team(
                name=name,
                description=description,
                tournament=tournament
            )
            team.save()
            team.players.set(players)
            team.tournament.set(tournament)
            return redirect("get_teams")

        return redirect("add_team")

    return render(
        request=request,
        template_name="add_team.html",
        context=dict(form=TeamForm())
    )

