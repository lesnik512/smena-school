# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class Client(models.Model):
    phone = models.CharField(max_length=15, unique=True)
    user = models.OneToOneField(User)