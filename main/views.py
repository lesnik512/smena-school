# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import date, timedelta

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from dishes.models import DailyMenu
from main.forms import LoginForm, RegistrationForm, ChangePasswordForm
from main.models import Client

# Create your views here.
from main.utils import sms_code_is_valid, get_mon_fri_of_current_week


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
        'weekly_menu': weekly_menu
    }
    return render(request, 'main/weekly_menu.html', context)


def home_view(request):
    daily_menu = DailyMenu.objects.get(date=date.today())
    dinners = daily_menu.dinners.all()
    context = {
        'today': date.today(),
        'dinners': dinners
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


@require_POST #TODO ask why require_POST
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
    return render(request, 'main/account.html')


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

    return redirect('account')