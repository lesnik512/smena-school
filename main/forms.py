# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from main.utils import clean_phone


class RegistrationForm(forms.Form):
    phone = forms.CharField(max_length=16)
    password = forms.CharField(max_length=255)
    sms_code = forms.CharField(max_length=10, min_length=1)

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        return clean_phone(phone)


class LoginForm(forms.Form):
    phone = forms.CharField(max_length=16)
    password = forms.CharField(max_length=255)

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        return clean_phone(phone)


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(max_length=255)
    new_password = forms.CharField(max_length=255)
    new_password_repeat = forms.CharField(max_length=255)

    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()
        new_password = cleaned_data.get('new_password')
        new_password_repeat = cleaned_data.get('new_password_repeat')

        if new_password != new_password_repeat:
            raise forms.ValidationError('Пароли не совпадают')

        return cleaned_data