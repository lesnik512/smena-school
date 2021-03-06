# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-13 04:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dishes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dinner',
            name='image',
        ),
        migrations.AlterField(
            model_name='dailymenu',
            name='date',
            field=models.DateField(),
        ),
        migrations.RemoveField(
            model_name='dailymenu',
            name='dinners',
        ),
        migrations.AddField(
            model_name='dailymenu',
            name='dinners',
            field=models.ManyToManyField(to='dishes.Dinner'),
        ),
        migrations.RemoveField(
            model_name='dinner',
            name='dishes',
        ),
        migrations.AddField(
            model_name='dinner',
            name='dishes',
            field=models.ManyToManyField(to='dishes.Dish'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='calorie',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='dish',
            name='price',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='dish',
            name='type',
            field=models.CharField(choices=[('soup', '\u0421\u0443\u043f'), ('second', '\u0412\u0442\u043e\u0440\u043e\u0435'), ('salad', '\u0421\u0430\u043b\u0430\u0442'), ('dessert', '\u0414\u0435\u0441\u0435\u0440\u0442')], default='soup', max_length=10),
        ),
        migrations.AlterField(
            model_name='dish',
            name='weight',
            field=models.IntegerField(),
        ),
    ]
