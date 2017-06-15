# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

from dishes.models import Dinner


class Client(models.Model):
    phone = models.CharField(max_length=15, unique=True)
    user = models.OneToOneField(User)


class Basket(models.Model):
    client = models.ForeignKey(Client, null=True)
    address = models.CharField(max_length=512, null=True)
    delivery_at = models.DateTimeField(null=True)

class BasketItem(models.Model):
    basket = models.ForeignKey(Basket, related_name='items')
    dinner = models.ForeignKey(Dinner)
    quantity = models.IntegerField()