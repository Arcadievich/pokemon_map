from django.db import models


class Pokemon(models.Model):
    title = models.TextField(verbose_name='Название')
    title_en = models.CharField(blank=True,verbose_name='Название на английском')
    title_jp = models.CharField(blank=True,verbose_name='Название на японском')
    description = models.TextField(blank=True,verbose_name='Описание')
    image = models.ImageField(null=True, blank=True,verbose_name='Изображение')
    previous_evolution = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='next_evolution',
        verbose_name='Из кого эволюционировал',
    )

    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        verbose_name='Покемон',
    )
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(verbose_name='Появится')
    disappeared_at = models.DateTimeField(verbose_name='Исчезнет')
    level = models.IntegerField(default=1,verbose_name='Уровень')
    health = models.IntegerField(default=1,verbose_name='Здоровье')
    strength = models.IntegerField(default=1,verbose_name='Сила')
    defence = models.IntegerField(default=1,verbose_name='Защита')
    stamina = models.IntegerField(default=1,verbose_name='Выносливость')

    def __str__(self):
        return f'{self.pokemon.title}'