# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random
from datetime import timedelta, date, time, datetime

import requests
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.defaulttags import register
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from main.utils import sms_code_is_valid, get_mon_fri_of_current_week, create_basket_item, clean_phone

from dishes.models import DailyMenu
from main.forms import LoginForm, RegistrationForm, ChangePasswordForm, SmsForm
from main.models import Client, Basket, BasketItem, Address, SmsCode


class WeeklyMenuView(View):
    template_name = 'main/weekly_menu.html'

    def get(self, request):
        today = date.today()
        if today.weekday() in [5, 6]:
            mon, fri = get_mon_fri_of_current_week(today + timedelta(days=2))
        else:
            mon, fri = get_mon_fri_of_current_week(today)
        weekly_menu = DailyMenu.objects.filter(date__gte=mon, date__lte=fri).prefetch_related('dinners')
        context = {
            'today': today,
            'monday_date': mon,
            'friday_date': fri,
            'weekly_menu': weekly_menu
        }
        return render(request, self.template_name, context)


class HomeView(View):
    template_name = 'main/home.html'

    def get(self, request):
        try:
            daily_menu = DailyMenu.objects.get(date=date.today())
        except DailyMenu.DoesNotExist:
            daily_menu = False
        dinners = daily_menu.dinners.all() if daily_menu else False
        basket = request.basket
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
        return render(request, self.template_name, context)


class LoginView(View):
    def post(self, request):
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


class RegistrationView(View):

    def post(self, request):
        is_sms = bool(request.POST.get('action') == 'send_sms')
        form = SmsForm(request.POST) if is_sms else RegistrationForm(request.POST)
        if form.is_valid():
            if is_sms:
                phone = form.cleaned_data['phone']
                sms_code = str(random.randrange(100000, 999999))
                try:
                    sms_code_object = SmsCode.objects.get(phone=phone)
                except SmsCode.DoesNotExist:
                    sms_code_object = SmsCode.objects.create(phone=phone)
                sms_code_object.sms_code = sms_code
                sms_code_object.save()
                params = {
                    'api_id': 'f567a71e-f7b2-c134-0da6-4c6bbd49602b',
                    'to': phone,
                    'msg': 'code: ' + sms_code,
                    'json': 1
                }
                content = requests.post('https://sms.ru/sms/send/', params=params).json()
                if content['status'] == 'OK':
                    pass
                return redirect('home')
            else:
                phone = form.cleaned_data['phone']
                password = form.cleaned_data['password']
                sms_code = str(form.cleaned_data['sms_code'])

                if Client.objects.filter(phone=phone):
                    print 'user already existed'
                    return redirect('home')

                if not sms_code_is_valid(sms_code, phone):
                    print 'code in note valid'
                    return redirect('home')

                user = User.objects.create_user(username=phone,
                                                password=password)

                Client.objects.create(phone=phone, user=user)

                login(request, user)

            return redirect('home')


class LogoutView(View):
    def get(self, request):
        basket_id = request.session.get('basket_id')
        logout(request)
        if basket_id:
            request.session['basket_id'] = basket_id
        return redirect('home')


class AccountView(View):
    template_name = 'main/account.html'

    @method_decorator(login_required())
    def get(self, request):
        order_list = Basket.objects.filter(order_date__isnull=False, client=request.user.client).order_by('-order_date')
        paginator = Paginator(order_list, 10)
        page = request.GET.get('page')
        try:
            orders = paginator.page(page)
        except PageNotAnInteger:
            orders = paginator.page(1)
        context = {
            'orders': orders
        }
        return render(request, self.template_name, context)


class ChangePasswordView(View):
    @method_decorator(login_required())
    def post(self, request):
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


class ChangeAmountView(View):
    def post(self, request, item_id):
        basket = request.basket
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


class PurchasingView(View):
    def post(self, request):
        basket = request.basket
        address = request.POST.get('address')
        geo_lat = request.POST.get('address_geo_lat')
        geo_lon = request.POST.get('address_geo_lon')
        try:
            minutes = int(request.POST.get('minutes'))
        except ValueError:
            minutes = False
        try:
            hours = int(request.POST.get('hours'))
        except ValueError:
            hours = False
        is_complete = False
        url = ''

        address_object = False
        if geo_lat and geo_lon:
            address_object = Address.objects.create(
                address=address,
                geo_lat=request.POST.get('address_geo_lat'),
                geo_lon=request.POST.get('address_geo_lon'),
                client=request.user.client
            )
            response = requests.post(
                'http://95.213.141.29/route/create/',
                headers={'host': 'cme.frfrdev.ru'},
                data={'lat': geo_lat, 'lon': geo_lon}
            )
            if response.status_code == 200:
                content = response.json()
                basket.route_id = content['id']
                basket.save()
        elif address:
            address_object = Address.objects.create(
                address=address,
                client=request.user.client
            )

        if address_object:
            basket.address = address_object
            basket.save()

        if minutes and hours:
            basket.delivery_at = datetime.combine(date.today(), time(hours, minutes))

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
        return HttpResponseRedirect(reverse('order_info', args=[basket.id])) if is_complete else redirect('home')


class OrderInfoView(View):
    template_name = 'main/order_view.html'

    def get(self, request, order_id):
        try:
            order = Basket.objects.get(id=order_id, client=request.user.client)
        except Basket.DoesNotExist:
            order = False
        if not order:
            return redirect('account')
        basket_items = order.items.all() if order else False
        context = {
            'order': order,
            'basket_items': basket_items
        }
        return render(request, self.template_name, context)


class CurrentPointView(View):
    def get(self, request, route_id):
        context = {}
        if route_id:
            response = requests.get(
                'http://95.213.141.29/route/'+route_id+'/current_point/',
                headers={'host': 'cme.frfrdev.ru'}
            )
            if response.status_code == 200:
                context = json.loads(response.content)
        return JsonResponse(context)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
