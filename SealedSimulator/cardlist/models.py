from django.db import models

class Card(models.Model):
    card_name = models.CharField(max_length=200)
    set_abbrev = models.CharField(max_length=200)
    image_url = models.CharField(max_length=200)
    def __str__(self):
        return self.card_name

class Set(models.Model):
    set_name = models.CharField(max_length=200)
    set_abbrev = models.CharField(max_length=200)
    release_date = models.DateTimeField()
    def __str__(self):
        return self.set_name
