# coding=utf-8
from django.contrib.auth import user_logged_in
from django.db.models.signals import post_save
from django.dispatch import receiver

from main.models import Basket


@receiver(post_save, sender=Basket)
def new_order(instance, **kwargs):
    order = instance
    if (order.order_date):
        print "Получен новый заказ №", order.id


@receiver(user_logged_in)
def log_login(request, user, **kwargs):
    request.basket.client = user.client
    request.basket.save()
