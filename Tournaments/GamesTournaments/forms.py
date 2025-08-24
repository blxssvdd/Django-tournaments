from django import forms
from .models import Team, Tournament, Player


class TournamentForm(forms.Form):
    name = forms.CharField(
        label="Назва турніру",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    location = forms.CharField(
        label="Місце проведення",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    description = forms.CharField(
        label="Опис турніру",
        widget=forms.Textarea(attrs={"class": "form-control"})
    )
    date = forms.DateField(
        label="Дата проведення",
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"})
    )


class PlayerForm(forms.Form):
    name = forms.CharField(
        label="Ім'я",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    description = forms.CharField(
        label="Опис гравця",
        widget=forms.Textarea(attrs={"class": "form-control"})
    )
    team = forms.ModelChoiceField(
        label="Команда",
        queryset=Team.objects.all(),
        widget=forms.Select(attrs={"class": "form-select"})
    )


class TeamForm(forms.Form):
    name = forms.CharField(
        label="Назва команди",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    description = forms.CharField(
        label="Опис команди",
        widget=forms.Textarea(attrs={"class": "form-control"})
    )
    tournament = forms.ModelChoiceField(
        label="Турнір",
        queryset=Tournament.objects.all(),
        widget=forms.Select(attrs={"class": "form-select"})
    )
