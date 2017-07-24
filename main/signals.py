# coding=utf-8
from django.contrib.auth import user_logged_in, user_logged_out
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
    print 'log in:', user.username


@receiver(user_logged_out)
def log_logout(user, **kwargs):
    print 'log out:', user.username
