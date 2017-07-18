from django.conf.urls import url

from main.views import (
    WeeklyMenuView, HomeView, LoginView, RegistrationView, LogoutView, AccountView, ChangePasswordView,
    ChangeAmountView, PurchasingView, OrderInfoView)

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^weekly_menu/$', WeeklyMenuView.as_view(), name='weekly_menu'),
    url(r'^registration/$', RegistrationView.as_view(), name='registration'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^account/$', AccountView.as_view(), name='account'),
    url(r'^change_password/$', ChangePasswordView.as_view(), name='change_password'),
    url(r'^change_amount/(\d+)/$', ChangeAmountView.as_view(), name='change_amount'),
    url(r'^purchasing/$', PurchasingView.as_view(), name='purchasing'),
    url(r'^order_info/(\d+)/$', OrderInfoView.as_view(), name='order_info')
]
