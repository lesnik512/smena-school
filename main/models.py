# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

from dishes.models import Dinner


class Client(models.Model):
    phone = models.CharField(max_length=15, unique=True)
    user = models.OneToOneField(User)


class Address(models.Model):
    address = models.CharField(max_length=512, null=False)
    geo_lat = models.CharField(max_length=50, null=True)
    geo_lon = models.CharField(max_length=50, null=True)
    client = models.ForeignKey(Client, related_name='addresses')


class Basket(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey(Client, null=True)
    address = models.ForeignKey(Address, null=True)
    delivery_at = models.DateTimeField(null=True)
    order_date = models.DateTimeField(null=True)
    route_id = models.IntegerField(null=True)

    def sum(self):
        summary = 0
        for basket_item in self.items.all():
            summary += basket_item.price * basket_item.quantity
        return summary

    def quantity(self):
        quantity = 0
        for basket_item in self.items.all():
            quantity += basket_item.quantity
        return quantity


class BasketItem(models.Model):
    basket = models.ForeignKey(Basket, related_name='items')
    dinner = models.ForeignKey(Dinner)
    quantity = models.IntegerField(default=0)
    price = models.FloatField(default=0)

    def sum(self):
        return self.quantity * self.price


class SmsCode(models.Model):
    phone = models.CharField(max_length=15, unique=True)
    sms_code = models.IntegerField(null=True)
    modified = models.DateTimeField(auto_now=True)