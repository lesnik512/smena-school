import re
from datetime import timedelta

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect

from dishes.models import Dinner

from main.models import Basket, BasketItem, Client, SmsCode


def get_mon_fri_of_current_week(today):
    monday_date = today + timedelta(days=0 - today.weekday())
    friday_date = today + timedelta(days=4 - today.weekday())
    return monday_date, friday_date


def sms_code_is_valid(sms_code, phone):
    try:
        sms_code_object = SmsCode.objects.get(phone=phone)
    except SmsCode.DoesNotExist:
        return False
    true_sms_code = str(sms_code_object.sms_code)
    response = (sms_code == true_sms_code)
    if response:
        sms_code_object.delete()
    return response


def clean_phone(dirty_phone):
    r = re.match(r'\+7\((\d+)\).(\d+)-(\d+)', dirty_phone)
    if hasattr(r,'groups'):
        return ''.join(r.groups())
    else:
        return False


def create_basket(request):
    basket_id = request.session.get('basket_id')
    try:
        basket = Basket.objects.get(id=basket_id) if basket_id else False
    except Basket.DoesNotExist:
        basket = False
    if not basket:
        client = False
        if request.user.is_authenticated:
            try:
                client = request.user.client
            except Client.DoesNotExist:
                pass
            if not client:
                Client.objects.create(phone=request.user.username, user=request.user)
        if client:
            basket = Basket.objects.create(client=client)
        else:
            basket = Basket.objects.create()

        request.session['basket_id'] = basket.id

    return basket


def get_basket(request):
    return {'basket': request.basket}


def create_basket_item(basket, item_id):
    dinner = Dinner.objects.get(id=item_id)
    try:
        basket_item = BasketItem.objects.get(basket=basket, dinner=dinner)
    except BasketItem.DoesNotExist:
        basket_item = False

    if not basket_item:
        basket_item = BasketItem.objects.create(basket=basket, dinner=dinner, quantity=0)
    if not basket_item.price:
        basket_item.price = dinner.price
    return basket_item


def form_response(request, form, status, url):
    if not form.is_valid():
        errors = form.errors
        for i in errors:
            error = form.errors[i][0]
            if error:
                messages.error(request, error)

    if request.is_ajax():
        django_messages = []
        for message in messages.get_messages(request):
            django_messages.append({
                "level": message.level,
                "message": message.message,
                "extra_tags": message.tags,
            })

        return JsonResponse({
            'success': status,
            'messages': django_messages
        })
    else:
        return redirect(url)