# -*- coding:utf-8 -*-
# author: JXF
# date: 2018-1-27
from rest_framework import permissions


# 拥有者是否为当前用户
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
        当请求方式为POST、PUT、DELETE等非安全方式时，判断obj拥有者是否为当前认证用户
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user



# class IsOwnerFilterBackend(filters.Base):
#     """
#     Filter that only allows users to see their own objects.
#     """
#     def filter_queryset(self, request, queryset, view):
#         return queryset.filter(receiver=request.user)
