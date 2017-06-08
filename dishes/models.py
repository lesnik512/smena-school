# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Dish(models.Model):
    name = models.CharField(max_length=255)
    weight = models.FloatField()
    calorie = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    TYPES_OF_DISHES = (
        ('HOT', 'hot'),
        ('SECOND', 'second'),
        ('SALAD', 'salad'),
        ('DESSERT', 'dessert'),
    )
    type = models.CharField(max_length=10,
                            choices=TYPES_OF_DISHES,
                            default='HOT')

class Dinner(models.Model):
    name = models.CharField(max_length=255)
    dishes = models.ForeignKey(Dish)
    image = models.FileField(upload_to='uploads/')

class DailyMenu(models.Model):
    date = models.DateField(auto_now=True)
    dinners = models.ForeignKey(Dinner)
