import re
from datetime import timedelta, date

from dishes.models import DailyMenu, Dinner

from main.models import Basket, BasketItem


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
    if not basket_id:
        daily_menu = DailyMenu.objects.get(date=date.today())
        dinners = daily_menu.dinners.all()
        if request.user.is_authenticated:
            basket = Basket.objects.create(client=request.user.client,
                                           delivery_at=daily_menu.date)
        else:
            basket = Basket.objects.create(delivery_at=daily_menu.date)

        for dinner in dinners:
            BasketItem.objects.create(basket=basket, dinner=dinner, quantity=0)

        request.session['basket_id'] = basket.id
    else:
        basket = Basket.objects.get(id=basket_id)
    return basket


def create_basket_item(basket,item_id):
    dinner = Dinner.objects.get(id=item_id)
    basket_item = BasketItem.objects.get(basket=basket, dinner=dinner)
    if not basket_item:
        basket_item = BasketItem.objects.create(basket=basket, dinner=dinner, quantity=0)
    return basket_item