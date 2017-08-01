# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-26 15:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_basket_order_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=512)),
                ('city', models.CharField(max_length=50, null=True)),
                ('street', models.CharField(max_length=50, null=True)),
                ('house', models.IntegerField(null=True)),
                ('geo_lat', models.CharField(max_length=50, null=True)),
                ('geo_lon', models.CharField(max_length=50, null=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to='main.Client')),
            ],
        ),
        migrations.AlterField(
            model_name='basket',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Address'),
        ),
    ]
