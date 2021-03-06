# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-08 07:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DailyMenu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Dinner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('image', models.FileField(upload_to='uploads/')),
            ],
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('weight', models.FloatField()),
                ('calorie', models.PositiveIntegerField()),
                ('price', models.PositiveIntegerField()),
                ('type', models.CharField(choices=[('HOT', 'hot'), ('SECOND', 'second'), ('SALAD', 'salad'), ('DESSERT', 'dessert')], default='HOT', max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='dinner',
            name='dishes',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dishes.Dish'),
        ),
        migrations.AddField(
            model_name='dailymenu',
            name='dinners',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dishes.Dinner'),
        ),
    ]
