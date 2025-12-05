from django.db import models  # noqa F401

# your models here
class Pokemon(models.Model):
    title = models.TextField()
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return f'{self.title}'