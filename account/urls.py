# -*- coding:utf-8 -*-
# author: jiangxf
# created: 2018-08-14

from django.conf.urls import url
from .views import *



urlpatterns = [
    url(r'^users/code/', SendVerificationCodeView.as_view(), name="send_code"),
    url(r'^users/register/', UserRegisterView.as_view(), name="user_register"),
    url(r'^users/login_code/', UserLoginView.as_view(), name="user_login_code"),
    url(r'^users/login_passwd/', UserLogin2View.as_view(), name="user_login_passwd"),
    url(r'^users/(?P<pk>\d+)/$', UserDetailView.as_view(), name="loginuser-detail"),
    url(r'^users/$', LoginUserDetailView.as_view(), name="logedinuser-detail"),
    url(r'^users/logout', UserLogoutView.as_view(),name="user_logout"),
    url(r'^users/update/(?P<uid>\d+)/$', UserUpdateView.as_view(), name="user-update"),
]
