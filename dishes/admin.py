# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from dishes.models import *


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ['name', 'weight', 'calorie', 'price', 'type']


@admin.register(Dinner)
class DinnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'image']
    filter_horizontal = ['dishes']


@admin.register(DailyMenu)
class DailyMenuAdmin(admin.ModelAdmin):
    list_display = ['date']
    filter_horizontal = ['dinners']