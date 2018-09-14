# -*- coding:utf-8 -*-
# author: jiangxf
# updated: 2018-08-14

from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed, APIException
from django.utils.translation import ugettext_lazy as _


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    # try:
    #     temp_dict = eval(str(response.data))
    #     keys = list(temp_dict.keys())
    #     temp_values = []
    #     for i in keys:
    #         temp_values.append(temp_dict[i][0])
    # except AttributeError:
    #     code = 90002
    #     detail = "asdadas"

    try:
        code = int(response.data['detail'][:5])
        detail = response.data['detail'][5:]
    except ValueError:
        code = 90001
        detail = response.data['detail']
    # except KeyError:
    #     if "This field may not be blank." in set(temp_values):
    #         code = 70001
    #         detail = 'Invalid params'
    #         response.data.clear()
    #     # 商家评价评分不在0-5之间
    #     elif 'score' in response.data:
    #         code = 30008
    #         detail = response.data['score'][0]
    #         del response.data['score']
    #     # 手机号码格式不正确
    #     elif 'phone' in response.data:
    #         code = 20004
    #         detail = response.data['phone'][0]
    #         del response.data['phone']
    #     elif 'title' in response.data:
    #         code = 30008
    #         detail = response.data['title'][0]
    #         del response.data['title']
    #     elif 'location' in response.data:
    #         code = 30009
    #         detail = response.data['location'][0]
    #         del response.data['location']
    #     else:
    #         code = 90003
    #         detail = 'werwrwe'
    except:
        code = 90004
        detail = 'werwrwe'

    if response is not None:
        response.data['error'] = code
        try:
            response.data['error_msg'] = detail
            del response.data['detail']  # 删除detail字段
            return response
        except KeyError:
            return response


# 错误异常： detail前5位为错误码
# 手机号格式不正确
class IllegalPhone(APIException):
    default_detail = _("20005Please input the correct format phone number.")
    status_code = 400


# 用户不存在
class UserDoesNotExist(APIException):
    default_detail = _("20001The user does not exist. Please register.")
    status_code = 404


# 手机号已注册
class PhoneExist(APIException):
    default_detail = _("20004The phone number has been registered.")
    status_code = 400


# 用户名已注册
class UsernameExist(APIException):
    default_detail = _("20003The username has been registered.")
    status_code = 400


# 帖子不存在
class FoundPostFailed(APIException):
    default_detail = _("40001Not found the post.")
    status_code = 404
