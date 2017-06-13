# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import date, timedelta

from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from dishes.models import DailyMenu
from main.models import Client

# Create your views here.


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
    return render(request, 'main/home.html')


def get_mon_fri_of_current_week(today):
    monday_date = today + timedelta(days=0 - today.weekday())
    friday_date = today + timedelta(days=4 - today.weekday())
    return monday_date, friday_date


def auth_view(request):
    phone = request.POST.get('phone')
    password = request.POST.get('password')
    try:
        Client.objects.get(phone=phone)

        user = authenticate(request,username=phone,password=password)

        if user:
            login(request, user)
    except Client.DoesNotExist:
        pass

    return HttpResponseRedirect(reverse('home'))


def reg_view(request):
    phone = request.POST.get('phone')
    sms = request.POST.get('sms')
    pasword = request.POST.get('password')
    #TODO: check if user exist
    client = Client.objects.get(phone=phone)
    if client:
        user = User.objects.create_user(username=phone,password=pasword)
        client = Client.objects.create(user=user,phone=phone)
        login(request,user)

    return HttpResponseRedirect(reverse('home'))

def logout_view(request):
    logout_view(request)
    return HttpResponseRedirect(reverse('home'))