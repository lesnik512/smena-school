# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date, timedelta, datetime

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.defaulttags import register
from django.urls import reverse
from django.views.decorators.http import require_POST

from main.utils import sms_code_is_valid, get_mon_fri_of_current_week, create_basket, create_basket_item, get_basket

from dishes.models import DailyMenu
from main.forms import LoginForm, RegistrationForm, ChangePasswordForm
from main.models import Client, Basket, BasketItem


def weekly_menu_view(request):
    today = date.today()
    if today.weekday() in [5, 6]:
        mon, fri = get_mon_fri_of_current_week(today + timedelta(days=2))
    else:
        mon, fri = get_mon_fri_of_current_week(today)
    weekly_menu = DailyMenu.objects.filter(date__gte=mon, date__lte=fri)
    context = {
        'today': today,
        'monday_date': mon,
        'friday_date': fri,
        'weekly_menu': weekly_menu,
        'basket': False
    }
    return render(request, 'main/weekly_menu.html', context)


def home_view(request):
    try:
        daily_menu = DailyMenu.objects.get(date=date.today())
    except DailyMenu.DoesNotExist:
        daily_menu = False
    dinners = daily_menu.dinners.all() if daily_menu else False
    basket_id = request.session.get('basket_id')
    try:
        basket = Basket.objects.get(id=basket_id) if basket_id else False
    except Basket.DoesNotExist:
        basket = False
    basket_dict = {} if basket else False
    if basket and dinners:
        for dinner in dinners:
            try:
                basket_item = BasketItem.objects.get(basket=basket, dinner=dinner)
            except BasketItem.DoesNotExist:
                basket_item = False
            quantity = basket_item.quantity if basket_item else 0
            basket_dict[dinner.id] = quantity
    context = {
        'today': date.today(),
        'dinners': dinners,
        'basket_dict': basket_dict
    }
    return render(request, 'main/home.html', context)


@require_POST
def login_view(request):
    form = LoginForm(request.POST)

    if form.is_valid():
        phone = form.cleaned_data['phone']
        password = form.cleaned_data['password']

        try:
            Client.objects.get(phone=phone)

            user = authenticate(request, username=phone, password=password)

            if user:
                login(request, user)

        except Client.DoesNotExist:
            return redirect('home')
    else:
        redirect('home')

    return redirect('home')


@require_POST
def registration_view(request):
    form = RegistrationForm(request.POST)

    if form.is_valid():
        phone = form.cleaned_data['phone']
        password = form.cleaned_data['password']
        sms_code = form.cleaned_data['sms_code']

        if Client.objects.filter(phone=phone):
            return redirect('home')

        if not sms_code_is_valid(sms_code):
            return redirect('home')

        user = User.objects.create_user(username=phone,
                                        password=password)

        Client.objects.create(phone=phone, user=user)

        login(request, user)

    return redirect('home')


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def account_view(request):
    order_list = Basket.objects.filter(order_date__isnull=False, client=request.user.client).order_by('-order_date')
    paginator = Paginator(order_list, 2)
    page = request.GET.get('page')
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    context = {
        'orders': orders
    }
    return render(request, 'main/account.html', context)


@login_required
@require_POST
def change_password_view(request):
    form = ChangePasswordForm(request.POST)

    if form.is_valid():
        old_password = form.cleaned_data['old_password']
        new_password = form.cleaned_data['new_password']

        user = authenticate(request,
                            username=request.user.username,
                            password=old_password)

        if not user:
            return redirect('account')

        user.set_password(new_password)
        user.save()

        login(request, user)
    else:
        redirect('account')

    return redirect('account')


@require_POST
def change_amount_view(request, item_id):
    basket = create_basket(request)
    amount = int(request.POST.get('amount'))
    context = {
        'status': False,
        'amount': 0
    }
    if item_id:
        item = create_basket_item(basket, item_id)
        quantity = item.quantity + amount
        item.quantity = quantity if quantity > 0 else 0
        item.save()
        context['status'] = True
        context['amount'] = item.quantity
    if request.is_ajax():
        context['basket_sum'] = basket.sum()
        context['basket_amount'] = basket.quantity()
        return JsonResponse(context)
    return redirect('home')


@require_POST
def purchasing_view(request):
    basket = create_basket(request)

    address = request.POST.get('address')
    minutes = request.POST.get('minutes')
    hours = request.POST.get('hours')
    is_complete = False
    url = ''

    if address:
        basket.address = address
        basket.save()

    if minutes and hours:
        basket.delivery_at = date.today() + timedelta(hours=int(hours), minutes=int(minutes))

    if basket.address and minutes and hours:
        basket.order_date = datetime.now()
        basket.save()
        del request.session['basket_id']
        is_complete = True
        url = reverse('order_info', args=[basket.id])

    if request.is_ajax():
        context = {
            'status': is_complete,
            'url': url
        }
        return JsonResponse(context)
    # return redirect('order_info', False, args=[basket.id])
    return HttpResponseRedirect(reverse('order_info', args=[basket.id])) if is_complete else redirect('home')


def order_info_view(request, order_id):
    try:
        order = Basket.objects.get(id=order_id, client=request.user.client)
    except DailyMenu.DoesNotExist:
        order = False
    if not order:
        redirect('account')
    basket_items = order.items.all() if order else False
    context = {
        'order': order,
        'basket_items': basket_items
    }
    return render(request, 'main/order_view.html', context)


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
