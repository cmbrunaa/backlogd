from django import forms
from .models import Game


class GameForm(forms.ModelForm):

    class Meta:

        model = Game

        fields = [
            'nome',
            'status',
            'nota',
            'review',
            'favorito',
            'imagem_url',
            'rawg_id',
            'descricao',
        ]

        widgets = {
            'imagem_url': forms.HiddenInput(),
            'rawg_id': forms.HiddenInput(),
            'descricao': forms.HiddenInput(),
        }