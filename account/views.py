# -*- coding:utf-8 -*-
# author: jiangxf
# created: 2018-08-14

from rest_framework.views import APIView
from .serializers import (
    SendVerificationCodeSerializer,
    UserLoginSerializer,
    UserRegisterSerializer,
    UserDetailSerializer,
)
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
)
from django.contrib.auth import login
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rewrite.exceptions import UserDoesNotExist, PhoneExist, UsernameExist
from django.http import Http404
from rest_framework import mixins
from rest_framework import generics
from .message import send_sms
from .models import LoginUser
import uuid
import random
import json


# 发送验证码
class SendVerificationCodeView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = SendVerificationCodeSerializer

    def post(self, request):
        serializer = SendVerificationCodeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            code = random.randint(100000, 999999)
            phone = serializer.validated_data['phone']
            business_id = uuid.uuid1()
            params = json.dumps({"code": code})
            try:
                send_sms(business_id, phone, "汉姆", "SMS_142148460", params)  # 发送验证码
                request.session['verifycode'] = code
                msg = Response(status=HTTP_204_NO_CONTENT)
            except:
                msg = Response({
                    'error': 70000,
                    'error_msg': "Failed to send verification code.",
                }, status=HTTP_400_BAD_REQUEST)
            return msg


# 用户注册
class UserRegisterView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer

    # 验证手机号或用户名是否已注册
    def has_exist(self, types, param):
        try:
            if types == 'phone':
                LoginUser.objects.get(phone=param)
                raise PhoneExist
            else:
                LoginUser.objects.get(username=param)
                raise UsernameExist
        except LoginUser.DoesNotExist:
            return True

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            vcode = serializer.validated_data['code']
            phone = serializer.validated_data['phone']
            if self.has_exist(types='phone', param=phone) and self.has_exist(types='username', param=username):
                try:
                    verify_code = request.session['verifycode']
                except:
                    msg = Response({
                        'error': 70001,
                        'error_msg': "验证码已失效，请重新发送"
                    }, status=HTTP_400_BAD_REQUEST)
                    return msg
                else:
                    if vcode == verify_code:
                        user = LoginUser.objects.create_user(username=username, password=password, phone=phone)
                        user.save()
                        del request.session['verifycode']
                        msg = Response({
                            'error': 0,
                            'data': {"username": username, "uid": user.id},
                            'message': 'Success to register.'
                        }, HTTP_201_CREATED)
                    else:
                        msg = Response({
                            'error': 70002,
                            'error_msg': '验证码错误.'
                        }, HTTP_400_BAD_REQUEST)
                    return msg


# 用户登录
class UserLoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def get_user(self, phone):
        try:
            return LoginUser.objects.get(phone=phone)
        except LoginUser.DoesNotExist:
            raise UserDoesNotExist

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone = serializer.validated_data['phone']
            vcode = serializer.validated_data['code']
            try:
                verify_code = request.session['verifycode']
            except:
                msg = Response({
                    'error': 70001,
                    'error_msg': "验证码已失效，请重新发送"
                }, status=HTTP_400_BAD_REQUEST)
                return msg
            else:
                if vcode == verify_code:
                    user = self.get_user(phone)
                    # login(request, user)
                    del request.session['verifycode']
                    # return HttpResponseRedirect(reverse("user:loginview"))
                    msg = Response({
                        'error': 0,
                        'data': {"username": user.username, "uid": user.id},
                        'message': 'Success to login.'
                    }, HTTP_200_OK)
                else:
                    msg = Response({
                        'error': 70002,
                        'error_msg': '验证码错误.'
                    }, HTTP_400_BAD_REQUEST)
                return msg


# 获取用户详情
class UserDetailView(mixins.RetrieveModelMixin,
                     generics.GenericAPIView):

    # 该权限为当前登录用户只能获取自己信息
    permission_classes = (AllowAny,)
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = (ExpiringTokenAuthentication,)
    # permission_classes = (AllowAny, )
    # queryset = LoginUser.objects.all()
    serializer_class = UserDetailSerializer

    def get(self, request, pk):
        try:
            user = LoginUser.objects.get(pk=pk)
            cont = UserDetailSerializer(user)
            msg = Response(data={
                'error': 0,
                'data': cont.data,
                'message': 'Success to get the info.'
            }, status=HTTP_200_OK)
        except Http404:    # 获取失败，没有找到对应数据
            raise UserDoesNotExist
        return msg