# -*- coding:utf-8 -*-
# author: jiangxf
# created: 2018-08-14

from django.conf.urls import url
from .views import (
    PostImageUploadView,
    PostPublishView,
    PostDetailView
)

urlpatterns = [
    url(r'^posts/publish', PostPublishView.as_view(), name='post_publish'),
    url(r'^posts/(?P<pk>\d+)/$', PostDetailView.as_view(), name='post_detail'),
    url(r'^posts/images$', PostImageUploadView.as_view(), name='post_image_upload'),
]
