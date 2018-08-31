# -*- coding:utf-8 -*-
# author: jiangxf
# created: 2018-08-14

from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
)
from django.contrib.auth import login,logout,authenticate
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
from rest_framework.authentication import (
    SessionAuthentication,
    BasicAuthentication,
    )
from django.core.exceptions import ObjectDoesNotExist
import uuid
import random
import json
from account.permissions import IsOwnerOrReadOnly,IsUserOrReadOnly,IsLoginUserOrReadOnly

# 发送验证码
class SendVerificationCodeView(generics.GenericAPIView):
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
class UserRegisterView(generics.GenericAPIView):
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

class UserUpdateView(generics.UpdateAPIView):
    '''
    put:
        用户更新信息，提交json中如不含相关字段则表示本字段不更改.username字段不能为空
    '''
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsLoginUserOrReadOnly,)
    serializer_class = UserUpdateSerializer
    queryset = LoginUser.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'uid'


# 用户登录
class UserLoginView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def get_user(self, phone):
        try:
            return LoginUser.objects.get(phone=phone)
        except LoginUser.DoesNotExist:
            raise UserDoesNotExist

    def post(self, request):
        '''通过验证码方式登录'''
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
                    login(request, user)
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

class UserLogin2View(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLogin2Serializer

    def post(self, request):
        '''通过账号密码方式登录'''
        serializer = UserLogin2Serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data.get('username','')
            password = serializer.validated_data.get('password','')

            user = authenticate(username=username,password=password)

            if user:
                login(request, user)
                msg = Response({
                        'error': 0,
                        'data': {"username": user.username, "uid": user.id},
                        'message': 'Success to login.'
                    }, HTTP_200_OK)
            else:
                msg = Response({
                        'error': 70003,
                        'error_msg': '账号或密码错误.'
                    }, HTTP_400_BAD_REQUEST)
            return msg

#logout
class UserLogoutView(generics.GenericAPIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = UserLogoutSerializer
    

    def get(self,request):
        '''logout'''
        #return Response(request.user)
        logout(request)
        msg = Response({
            'error':0,
            'message': 'Success to logout.'
            },HTTP_200_OK)
        return msg


# 获取用户详情
class UserDetailView(generics.GenericAPIView):

    # 该权限为当前登录用户只能获取自己信息
    permission_classes = (AllowAny,)
    serializer_class = UserDetailSerializer


    def get(self, request, pk):
        '''通过id获取用户详情'''
        try:
            user = LoginUser.objects.get(pk = pk)
            cont = UserDetailSerializer(user)
            msg = Response(data={
                'error': 0,
                'data': cont.data,
                'message': 'Success to get the info.'
            }, status=HTTP_200_OK)
        except ObjectDoesNotExist:    # 获取失败，没有找到对应数据
            raise UserDoesNotExist
        return msg

class LoginUserDetailView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LoginUserDetailSerializer
    queryset = LoginUser.objects.all()

    def get(self, request):
        '''通过id获取用户详情'''
        try:
            user = LoginUser.objects.get(id = request.user.id)
            cont = LoginUserDetailSerializer(user)
            msg = Response(data={
                'error': 0,
                'data': cont.data,
                'message': 'Success to get the info.'
            }, status=HTTP_200_OK)
        except ObjectDoesNotExist:    # 获取失败，没有找到对应数据
            msg = Response(data={
                'error': 0,
                'message': 'Please Login'
            }, status=HTTP_400_BAD_REQUEST )
        return msg

