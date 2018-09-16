# -*- coding:utf-8 -*-
# author: jiangxf
# created: 2018-08-14

from rest_framework.serializers import (
    ModelSerializer,
    ValidationError,
    IntegerField,
    Serializer,
    CharField,
)
from .models import LoginUser,UserIIS
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
        fields = ('username', 'password', 'phone', 'code',)


# 用户登录(使用手机号接受验证码）
class UserLoginSerializer(SendVerificationCodeSerializer):
    code = IntegerField()


# 用户登录(账号密码登录)
class UserLogin2Serializer(ModelSerializer):
    username = CharField(max_length=100)

    class Meta:
        model = LoginUser
        fields = ('username', 'password')


class UserUpdateSerializer(ModelSerializer):

    class Meta:
        model = LoginUser
        fields = ('username', 'first_name', 'last_name', 'email',
                  'address', 'major', 'job', 'company', 'wealth', 'risk_preference')


# logout
class UserLogoutSerializer(Serializer):
    pass


# 用户信息
class UserDetailSerializer(ModelSerializer):
    uid = IntegerField(source='id')

    class Meta:
        model = LoginUser
        fields = ('username', 'uid')


# 登录用户详情
class LoginUserDetailSerializer(ModelSerializer):

    class Meta:
        model = LoginUser
        exclude = ['password', 'groups', 'user_permissions']


# class UserIISDetailSerializer(serializer):
#
#     def unpack(self, ob):
#         dics = eval(ob)
#         return dics
#
#     buy =
#
#
#     class Meta:
#         model = UserIIS
#         fields = ('buy', 'sell', 'month_get',
#                   'month_rate', 'year_rate', 'days')
