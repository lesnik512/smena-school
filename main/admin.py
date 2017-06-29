# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from main.models import Basket, Client


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ['created', 'client', 'address', 'delivery_at', 'order_date', 'sum', 'quantity']


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['phone', 'user']