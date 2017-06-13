# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.db import models


@python_2_unicode_compatible
class Dish(models.Model):
    TYPES = (
        ('soup', 'Суп'),
        ('second', 'Второе'),
        ('salad', 'Салат'),
        ('dessert', 'Десерт'),
    )
    name = models.CharField(max_length=255)
    weight = models.IntegerField()
    calorie = models.IntegerField()
    price = models.IntegerField()
    type = models.CharField(max_length=10, choices=TYPES, default='soup')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Dinner(models.Model):
    name = models.CharField(max_length=255)
    dishes = models.ManyToManyField(Dish)

    def __str__(self):
        return self.name

    @property
    def price(self):
        price = 0
        for dish in self.dishes.all():
            price += dish.price
        return price

    @property
    def weight(self):
        weight = 0
        for dish in self.dishes.all():
            weight += dish.weight
        return weight

    @property
    def calorie(self):
        calorie = 0
        for dish in self.dishes.all():
            calorie += dish.calorie
        return calorie

    @property
    def soup(self):
        return self.dishes.get(type='soup')

    @property
    def second(self):
        return self.dishes.get(type='second')

    @property
    def salad(self):
        return self.dishes.get(type='salad')

    @property
    def dessert(self):
        return self.dishes.get(type='dessert')


@python_2_unicode_compatible
class DailyMenu(models.Model):
    date = models.DateField()
    dinners = models.ManyToManyField(Dinner)

    def __str__(self):
        return 'Меню на {}'.format(self.date)