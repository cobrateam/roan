# -*- coding: utf-8 -*-
from django.db import models


class Poll(models.Model):
    title = models.CharField(max_length=100)


class Choice(models.Model):
    title = models.CharField(max_length=100)
    poll = models.ForeignKey(Poll)
