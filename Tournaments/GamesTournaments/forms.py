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
    tournaments = forms.ModelMultipleChoiceField(
        queryset=Tournament.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "form-select"}),
        label="Виберіть турніри"
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
    players = forms.ModelMultipleChoiceField(
        queryset=Player.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "form-select"}),
        label="Виберіть гравців"
    )
