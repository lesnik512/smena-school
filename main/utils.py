import re
from datetime import timedelta, date

from dishes.models import DailyMenu, Dinner

from main.models import Basket, BasketItem, Client


def get_mon_fri_of_current_week(today):
    monday_date = today + timedelta(days=0 - today.weekday())
    friday_date = today + timedelta(days=4 - today.weekday())
    return monday_date, friday_date


def sms_code_is_valid(sms_code):
    return True


def clean_phone(dirty_phone):
    r = re.match(r'\+7\((\d+)\).(\d+)-(\d+)', dirty_phone)
    return ''.join(r.groups())


def create_basket(request):
    basket_id = request.session.get('basket_id')
    try:
        basket = Basket.objects.get(id=basket_id) if basket_id else False
    except Basket.DoesNotExist:
        basket = False
    if not basket:
        daily_menu = DailyMenu.objects.get(date=date.today())
        dinners = daily_menu.dinners.all()
        client = False
        if request.user.is_authenticated:
            try:
                client = request.user.client
            except Client.DoesNotExist:
                pass
            if not client:
                Client.objects.create(phone=request.user.username, user=request.user)
        if client:
            basket = Basket.objects.create(client=client, delivery_at=daily_menu.date)
        else:
            basket = Basket.objects.create(delivery_at=daily_menu.date)

        for dinner in dinners:
            BasketItem.objects.create(basket=basket, dinner=dinner, quantity=0)

        request.session['basket_id'] = basket.id

    return basket


def get_basket(request):
    basket_id = request.session.get('basket_id')
    try:
        basket = Basket.objects.get(id=basket_id) if basket_id else False
    except Basket.DoesNotExist:
        basket = False
    return {'basket': basket}


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
