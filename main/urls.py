"""smena URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from main.views import (
    weekly_menu_view, home_view, registration_view, login_view, logout_view,
    account_view, change_password_view, order_info_view, change_amount_view,
    purchasing_view)

urlpatterns = [
    url(r'^$', home_view, name='home'),
    url(r'^weekly_menu/$', weekly_menu_view, name='weekly_menu'),
    url(r'^registration/$', registration_view, name='registration'),
    url(r'^login/$', login_view, name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^account/$', account_view, name='account'),
    url(r'^change_password/$', change_password_view, name='change_password'),
    url(r'^change_amount/(\d+)/$', change_amount_view, name='change_amount'),
    url(r'^purchasing/$', purchasing_view, name='purchasing'),
    url(r'^order_info/(\d+)/$', order_info_view, name='order_info')
]
