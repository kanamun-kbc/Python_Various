from django.db import models

class Animal(models.Model):
    animal_key = models.IntegerField()
    animal_name = models.CharField(max_length=100)
