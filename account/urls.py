# -*- coding:utf-8 -*-
# author: jiangxf
# created: 2018-08-14

from django.conf.urls import url
from .views import (
    UserRegisterView,
    SendVerificationCodeView,
    UserLoginView,
    UserDetailView,
)

urlpatterns = [
    url(r'^users/code', SendVerificationCodeView.as_view(), name="send_code"),
    url(r'^users/register/', UserRegisterView.as_view(), name="user_register"),
    url(r'^users/login', UserLoginView.as_view(), name="user_login"),
    url(r'^users/(?P<pk>\d+)/$', UserDetailView.as_view(), name="user_detail"),
]
