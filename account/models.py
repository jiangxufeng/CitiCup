# -*- coding:utf-8 -*-
# author: jiangxf
# created: 2018-08-14

from django.db import models
from django.contrib.auth.models import AbstractUser


# 用户信息
class LoginUser(AbstractUser):
    # 手机号
    phone = models.CharField(max_length=11, unique=True, verbose_name="phone")

    class Meta:
        db_table = 'LoginUser'
        ordering = ['-id']

    def __str__(self):
        return self.username
