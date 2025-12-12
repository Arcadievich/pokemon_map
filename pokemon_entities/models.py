from django.db import models


class Pokemon(models.Model):
    title = models.TextField()
    title_en = models.CharField(blank=True)
    title_jp = models.CharField(blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField()
    disappeared_at = models.DateTimeField()
    level = models.IntegerField(default=1)
    health = models.IntegerField(default=1)
    strength = models.IntegerField(default=1)
    defence = models.IntegerField(default=1)
    stamina = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.pokemon.title}'