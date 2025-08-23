from django.db import models


class Tournament(models.Model):
    name = models.CharField(max_length=100, default=None, null=True)
    location = models.CharField(max_length=100, default=None, null=True)
    description = models.TextField(default=None, null=True)
    count = models.IntegerField(default=0, null=True)
    date = models.DateField(default=None, null=True)
    teams = models.ManyToManyField("Team", default=None)


    def __str__(self):
        return f"Турнір: {self.name}, Місце: {self.location}, Дата: {self.date}, Кількість команд: {self.teams.all()}"


class Team(models.Model):
    name = models.CharField(max_length=100, default=None, null=True)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, default=None)
    description = models.TextField(default=None, null=True)

    def __str__(self):
        return f"Команда: {self.name}, Турнір: {self.tournament.name}"



class Player(models.Model):
    name = models.CharField(max_length=100, default=None, null=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, default=None)
    description = models.TextField(default=None, null=True)

    def __str__(self):
        return f"Гравець: {self.name}, Команда: {self.team.name}, Турніри: {self.tournaments.all()}"