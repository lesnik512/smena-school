# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from main.utils import clean_phone


class SmsForm(forms.Form):
    phone = forms.CharField(max_length=16, error_messages={'required': 'Введите номер телефона'})

    def clean_phone(self):
        phone = clean_phone(self.cleaned_data['phone'])
        if phone:
            return phone
        else:
            raise forms.ValidationError('Введите номер телефона')


class RegistrationForm(forms.Form):
    phone = forms.CharField(max_length=16, error_messages={'required': 'Введите номер телефона'})
    password = forms.CharField(max_length=255, error_messages={'required': 'Введите пароль'})
    sms_code = forms.CharField(error_messages={'required': 'Введите код из sms'})

    def clean_phone(self):
        phone = clean_phone(self.cleaned_data['phone'])
        if phone:
            return phone
        else:
            raise forms.ValidationError('Введите номер телефона')


class LoginForm(forms.Form):
    phone = forms.CharField(max_length=16, error_messages={'required': 'Введите номер телефона'})
    password = forms.CharField(max_length=255, error_messages={'required': 'Введите пароль'})

    def clean_phone(self):
        phone = clean_phone(self.cleaned_data['phone'])
        if phone:
            return phone
        else:
            raise forms.ValidationError('Введите номер телефона')


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
