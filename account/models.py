# -*- coding:utf-8 -*-
# author: jiangxf
# created: 2018-08-14

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# 用户信息
class LoginUser(AbstractUser):
    # 手机号
    RISK_CHOICE = (
        (0, 'low'),
        (1, 'medium'),
        (2, 'high')
    )

    phone = models.CharField(max_length=11, unique=True, verbose_name="phone")
    address = models.CharField(max_length=128, blank=True, null=True)
    major = models.IntegerField(blank=True, default=0)
    job = models.IntegerField(blank=True, default=0)
    company = models.CharField(max_length=128, blank=True, null=True)
    wealth = models.FloatField(blank=True, default=0.0)
    alltags = models.TextField(blank=True, default='{\"post\":{}, \"like\":{}, \"comment\":{}}')
    forumcoin = models.IntegerField(blank=True, default=0)
    risk_preference = models.IntegerField(choices=RISK_CHOICE, default=0)


    class Meta:
        db_table = 'LoginUser'
        ordering = ['-id']

    def __str__(self):
        return self.username


class UserIIS(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='iis')
    buys = models.CharField(max_length=2560, default='[]')
    sells = models.CharField(max_length=2560, default='[]')
    month_get = models.FloatField(blank=True, default=0.0)
    month_rate = models.FloatField(blank=True, default=0.0)
    year_rate = models.FloatField(blank=True, default=0.0)
    days = models.CharField(max_length=128, blank=False, default='1970-01-01')

    def __str__(self):
        return self.user.username

