# -*- coding:utf-8 -*-
# author: jiangxf
# created: 2018-08-14

from django.db import models
from django.contrib.auth.models import AbstractUser


# 用户信息
class LoginUser(AbstractUser):
    # 手机号
    phone = models.CharField(max_length=11, unique=True, verbose_name="phone")
    address = models.CharField(max_length=128, blank=True, null=True)
    major = models.IntegerField(blank=True, default=0)
    job = models.IntegerField(blank=True, default=0)
    company = models.CharField(max_length=128, blank=True, null=True)
    wealth = models.DecimalField(max_digits=40, decimal_places=5, blank=True, null=True)

    class Meta:
        db_table = 'LoginUser'
        ordering = ['-id']

    def __str__(self):
        return self.username




