from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class Game(models.Model):

    STATUS_CHOICES = [
        ('wishlist', 'Quero Jogar'),
        ('playing', 'Jogando'),
        ('finished', 'Zerado'),
        ('dropped', 'Abandonado'),
    ]

    usuario = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    null=True,
    blank=True
    )

    nome = models.CharField(max_length=100)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='wishlist'
    )

    nota = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10)
        ]
    )

    review = models.TextField(blank=True)

    favorito = models.BooleanField(default=False)

    imagem_url = models.URLField(blank=True)

    rawg_id = models.IntegerField(
        null=True,
        blank=True
    )

    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.nome