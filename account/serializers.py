# -*- coding:utf-8 -*-
# author: jiangxf
# created: 2018-08-14

from rest_framework.serializers import (
    ModelSerializer,
    ValidationError,
    IntegerField,
    Serializer,
)
from .models import LoginUser
from rewrite.exceptions import IllegalPhone


# 发送验证码手机格式有效验证
class SendVerificationCodeSerializer(Serializer):
    phone = IntegerField()

    def validate_phone(self, value):
        try:
            phone = self.get_initial()['phone']
            data = int(phone)
        except ValueError:   # 如果传入的phone不是纯数字，报错
            raise IllegalPhone
        else:
            if len(phone) != 11:
                raise IllegalPhone
            elif phone[0] != '1':
                raise IllegalPhone
        return value


# 用户注册
class UserRegisterSerializer(ModelSerializer):
    code = IntegerField()

    class Meta:
        model = LoginUser
        fields = ('username', 'password', 'phone', 'code')


# 用户登录(使用手机号接受验证码）
class UserLoginSerializer(SendVerificationCodeSerializer):
    code = IntegerField()


# 用户信息
class UserDetailSerializer(ModelSerializer):
    uid = IntegerField(source='id')

    class Meta:
        model = LoginUser
        fields = ('username', 'uid', 'phone')