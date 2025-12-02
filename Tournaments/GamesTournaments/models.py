from django.contrib.auth import get_user_model
from django.db import models


class Tournament(models.Model):
    name = models.CharField(max_length=100, default=None, null=True)
    location = models.CharField(max_length=100, default=None, null=True)
    description = models.TextField(default=None, null=True)
    date = models.DateField(default=None, null=True)
    banner = models.ImageField(upload_to="tournaments/banners/", blank=True, null=True)
    teams = models.ManyToManyField("Team", default=None, related_name='+')


    def __str__(self):
        return f"Турнір: {self.name}, Місце: {self.location}, Дата: {self.date}, Кількість команд: {self.teams.all()}"

    class Meta:
        permissions = (
            ("manage_tournaments", "Може створювати та видаляти турніри"),
        )


class Team(models.Model):
    name = models.CharField(max_length=100, default=None, null=True)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, default=None)
    description = models.TextField(default=None, null=True)
    emblem = models.ImageField(upload_to="teams/emblems/", blank=True, null=True)

    def __str__(self):
        return f"Команда: {self.name}, Турнір: {self.tournament.name}"

    class Meta:
        permissions = (
            ("manage_teams", "Може створювати та видаляти команди"),
        )


class Player(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="team_memberships", null=True, blank=True)
    name = models.CharField(max_length=100, default=None, null=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, default=None)
    description = models.TextField(default=None, null=True)

    class Meta:
        permissions = (
            ("manage_roster", "Може керувати складом гравців"),
        )
        unique_together = ("user", "team")

    def __str__(self):
        return f"Гравець: {self.name}, Команда: {self.team.name}"


class Registration(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="tournament_registrations")
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name="registrations")
    count = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("user", "tournament")
        verbose_name = "Реєстрація на турнір"
        verbose_name_plural = "Реєстрації на турніри"

    def __str__(self):
        return f"{self.user.username} → {self.tournament.name} (x{self.count})"
