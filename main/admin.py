# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from main.models import Basket, Client, BasketItem, Address


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ['created', 'client', 'address', 'delivery_at', 'order_date', 'sum', 'quantity', 'route_id']


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['phone', 'user']


@admin.register(Address)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['address', 'geo_lat', 'geo_lon']