from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Case, Count, IntegerField, Sum, Value, When, Prefetch
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from django.urls import reverse

from .forms import TournamentForm, TeamForm, PlayerForm, JoinTeamForm
from .models import Tournament, Team, Player, Registration
from .serializers import TournamentSerializer

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


@api_view(["GET"])
def tournaments_api(request: HttpRequest):
    tournaments = Tournament.objects.all().order_by("-date", "name")
    serializer = TournamentSerializer(instance=tournaments, many=True)
    return Response(serializer.data)


@login_required(login_url="/users/sign_in/")
def add_tournament(request):
    if not request.user.has_perm("GamesTournaments.manage_tournaments"):
        messages.error(request, "У вас немає прав створювати турніри.")
        return redirect("get_tournaments")

    form = TournamentForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        name = form.cleaned_data["name"]
        location = form.cleaned_data["location"]
        description = form.cleaned_data["description"]
        date = form.cleaned_data["date"]
        banner = form.cleaned_data.get("banner")
        tournament = Tournament(name=name, location=location, description=description, date=date, banner=banner)
        tournament.save()
        return redirect("get_tournaments")
    return render(request=request, template_name="add_tournament.html", context=dict(form=form))


@login_required(login_url="/users/sign_in/")
def edit_tournament(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    if not request.user.has_perm("GamesTournaments.manage_tournaments"):
        messages.error(request, "У вас немає прав змінювати турніри.")
        return redirect("get_tournaments")

    initial = {
        "name": tournament.name,
        "location": tournament.location,
        "description": tournament.description,
        "date": tournament.date,
    }
    form = TournamentForm(request.POST or None, request.FILES or None, initial=initial)
    if request.method == "POST" and form.is_valid():
        tournament.name = form.cleaned_data["name"]
        tournament.location = form.cleaned_data["location"]
        tournament.description = form.cleaned_data["description"]
        tournament.date = form.cleaned_data["date"]
        new_banner = form.cleaned_data.get("banner")
        if new_banner:
            tournament.banner = new_banner
        tournament.save()
        cache.clear()
        messages.success(request, "Турнір оновлено.")
        return redirect("get_tournaments")

    return render(
        request=request,
        template_name="edit_tournament.html",
        context={"form": form, "tournament": tournament},
    )


def get_tournaments(request):
    cache_key = f"tournaments_{request.user.id}" if request.user.is_authenticated else "tournaments_anon"
    tournaments = cache.get(cache_key)

    if not tournaments:
        teams_prefetch = Prefetch(
            "team_set",
            queryset=Team.objects.annotate(player_count=Count("player")).order_by("name"),
        )
        tournaments_qs = Tournament.objects.all().prefetch_related(teams_prefetch)
        if request.user.is_authenticated:
            tournaments_qs = tournaments_qs.annotate(
                user_registration_count=Sum(
                    Case(
                        When(registrations__user=request.user, then="registrations__count"),
                        default=Value(0),
                        output_field=IntegerField()
                    )
                ),
                team_count=Count("team", distinct=True),
            )
        else:
            tournaments_qs = tournaments_qs.annotate(team_count=Count("team", distinct=True))
        tournaments = list(tournaments_qs.order_by("-date", "name"))
        cache.set(cache_key, tournaments, 30)
    return render(
        request=request,
        template_name="tournaments.html",
        context=dict(tournaments=tournaments)
    )


def get_tournaments_paginated(request):
    teams_prefetch = Prefetch(
        "team_set",
        queryset=Team.objects.annotate(player_count=Count("player")).order_by("name"),
    )
    tournaments_qs = Tournament.objects.all().prefetch_related(teams_prefetch)
    if request.user.is_authenticated:
        tournaments_qs = tournaments_qs.annotate(
            user_registration_count=Sum(
                Case(
                    When(registrations__user=request.user, then="registrations__count"),
                    default=Value(0),
                    output_field=IntegerField()
                )
            ),
            team_count=Count("team", distinct=True),
        )
    else:
        tournaments_qs = tournaments_qs.annotate(team_count=Count("team", distinct=True))
    tournaments = tournaments_qs.order_by("-date", "name")
    paginator = Paginator(tournaments, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    registrations_map = {}
    if request.user.is_authenticated:
        registrations_map = {
            reg.tournament_id: reg.count
            for reg in Registration.objects.filter(user=request.user)
        }
    return render(
        request=request,
        template_name="tournaments_paginated.html",
        context=dict(page_obj=page_obj, registrations_map=registrations_map)
    )


def get_players(request):
    return render(
        request=request,
        template_name="players.html",
        context=dict(players=Player.objects.select_related("team__tournament", "user").all())
    )


@login_required(login_url="/users/sign_in/")
def add_player(request):
    if not request.user.has_perm("GamesTournaments.manage_roster"):
        messages.error(request, "У вас немає прав додавати гравців вручну.")
        return redirect("get_players")

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
    memberships = set()
    if request.user.is_authenticated:
        memberships = set(
            Player.objects.filter(user=request.user).values_list("team_id", flat=True)
        )
    return render(
        request=request,
        template_name="teams.html",
        context=dict(
            teams=Team.objects.select_related("tournament").all(),
            memberships=memberships,
        )
    )


@login_required(login_url="/users/sign_in/")
def join_team(request, team_id=None):
    initial = {}
    preselected_team = None
    if team_id:
        preselected_team = get_object_or_404(Team, pk=team_id)
        initial["team"] = preselected_team
    form = JoinTeamForm(request.POST or None, initial=initial)
    if request.method == "POST" and form.is_valid():
        team = form.cleaned_data["team"]
        note = form.cleaned_data["note"]
        player, created = Player.objects.get_or_create(
            user=request.user,
            team=team,
            defaults={
                "name": request.user.get_full_name() or request.user.username,
                "description": note or "",
            },
        )
        if not created and note:
            player.description = note
            player.save(update_fields=["description"])
        messages.success(
            request,
            f"{'Додано до команди' if created else 'Дані в команді оновлено'}: {team.name}",
        )
        return redirect("get_teams")

    return render(
        request=request,
        template_name="join_team.html",
        context=dict(form=form, preselected_team=preselected_team),
    )


@login_required(login_url="/users/sign_in/")
@require_POST
def leave_team(request, team_id):
    membership = get_object_or_404(Player, user=request.user, team_id=team_id)
    membership.delete()
    messages.success(request, "Ви покинули команду.")
    return redirect("get_teams")


@login_required(login_url="/users/sign_in/")
def add_team(request):
    if not request.user.has_perm("GamesTournaments.manage_teams"):
        messages.error(request, "У вас немає прав створювати команди.")
        return redirect("get_teams")

    form = TeamForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        name = form.cleaned_data.get("name")
        description = form.cleaned_data.get("description")
        tournament = form.cleaned_data.get("tournament")
        emblem = form.cleaned_data.get("emblem")
        team = Team(
            name=name,
            description=description,
            tournament=tournament,
            emblem=emblem,
        )
        team.save()
        return redirect("get_teams")

    return render(
        request=request,
        template_name="add_team.html",
        context=dict(form=form)
    )


@login_required(login_url="/users/sign_in/")
def edit_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    if not request.user.has_perm("GamesTournaments.manage_teams"):
        messages.error(request, "У вас немає прав змінювати команди.")
        return redirect("get_teams")

    initial = {
        "name": team.name,
        "description": team.description,
        "tournament": team.tournament,
    }
    form = TeamForm(request.POST or None, request.FILES or None, initial=initial)
    if request.method == "POST" and form.is_valid():
        team.name = form.cleaned_data.get("name")
        team.description = form.cleaned_data.get("description")
        team.tournament = form.cleaned_data.get("tournament")
        new_emblem = form.cleaned_data.get("emblem")
        if new_emblem:
            team.emblem = new_emblem
        team.save()
        cache.clear()
        messages.success(request, "Команду оновлено.")
        return redirect("get_teams")

    return render(
        request=request,
        template_name="edit_team.html",
        context={"form": form, "team": team},
    )


@login_required(login_url="/users/sign_in/")
@require_POST
def delete_tournament(request, tournament_id):
    if not request.user.has_perm("GamesTournaments.manage_tournaments"):
        messages.error(request, "У вас немає прав видаляти турніри.")
        return redirect("get_tournaments")

    tournament = get_object_or_404(Tournament, pk=tournament_id)
    tournament.delete()
    messages.success(request, "Турнір видалено.")
    return redirect("get_tournaments")


@login_required(login_url="/users/sign_in/")
@require_POST
def delete_team(request, team_id):
    if not request.user.has_perm("GamesTournaments.manage_teams"):
        messages.error(request, "У вас немає прав видаляти команди.")
        return redirect("get_teams")

    team = get_object_or_404(Team, pk=team_id)
    team.delete()
    messages.success(request, "Команду видалено.")
    return redirect("get_teams")


@login_required(login_url="/users/sign_in/")
@require_POST
def delete_player(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    if player.user_id == request.user.id:
        player.delete()
        messages.success(request, "Ви покинули команду.")
        return redirect("get_teams")

    if not request.user.has_perm("GamesTournaments.manage_roster"):
        messages.error(request, "У вас немає прав видаляти гравців.")
        return redirect("get_players")

    player.delete()
    messages.success(request, "Гравця видалено.")
    return redirect("get_players")


@login_required(login_url="/users/sign_in/")
@require_POST
def add_to_registration(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    try:
        increment = int(request.POST.get("count", 1))
    except (TypeError, ValueError):
        increment = 1

    increment = 1 if increment < 1 else increment

    registration, created = Registration.objects.get_or_create(
        user=request.user,
        tournament=tournament,
        defaults={"count": increment}
    )
    if not created:
        registration.count += increment
        registration.save(update_fields=["count"])

    messages.success(request, f"Додано {increment} слот(и) для {tournament.name}.")
    redirect_url = request.POST.get("next") or request.META.get("HTTP_REFERER")
    if not redirect_url or not url_has_allowed_host_and_scheme(redirect_url, allowed_hosts={request.get_host()}):
        redirect_url = reverse("my_registrations")
    return redirect(redirect_url)


@login_required(login_url="/users/sign_in/")
def my_registrations(request):
    registrations = Registration.objects.select_related("tournament").filter(
        user=request.user
    ).order_by("-tournament__date", "tournament__name")
    total_count = sum(reg.count for reg in registrations)
    return render(
        request=request,
        template_name="my_registrations.html",
        context=dict(registrations=registrations, total_count=total_count)
    )


@login_required(login_url="/users/sign_in/")
@require_POST
def remove_registration(request, tournament_id):
    registration = get_object_or_404(Registration, user=request.user, tournament_id=tournament_id)
    try:
        decrement = int(request.POST.get("count", registration.count))
    except (TypeError, ValueError):
        decrement = registration.count

    decrement = 1 if decrement < 1 else decrement

    if decrement >= registration.count:
        registration.delete()
        messages.success(request, f"Реєстрацію для {registration.tournament.name} видалено.")
    else:
        registration.count -= decrement
        registration.save(update_fields=["count"])
        messages.success(request, f"Зменшено слотів для {registration.tournament.name} на {decrement} (залишилось {registration.count}).")

    redirect_url = request.POST.get("next") or request.META.get("HTTP_REFERER")
    if not redirect_url or not url_has_allowed_host_and_scheme(redirect_url, allowed_hosts={request.get_host()}):
        redirect_url = reverse("my_registrations")
    return redirect(redirect_url)
