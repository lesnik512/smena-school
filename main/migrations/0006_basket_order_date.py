# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-29 06:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20170629_1047'),
    ]

    operations = [
        migrations.AddField(
            model_name='basket',
            name='order_date',
            field=models.DateTimeField(null=True),
        ),
    ]
