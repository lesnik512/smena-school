# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-01 04:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20170727_1044'),
    ]

    operations = [
        migrations.AddField(
            model_name='basket',
            name='route_id',
            field=models.IntegerField(null=True),
        ),
    ]
