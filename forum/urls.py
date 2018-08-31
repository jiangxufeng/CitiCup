# -*- coding:utf-8 -*-
# author: jiangxf
# created: 2018-08-14

from django.conf.urls import url
from .views import *



urlpatterns = [
    url(r'^posts/publish', PostPublishView.as_view(), name='post_publish'),
    #url(r'^posts/(?P<pk>\d+)/$', PostDetailView.as_view(), name='post-detail'),
    url(r'^posts/detail/(?P<pid>\d+)/$', PostDetailView.as_view(), name='post-update'),
    url(r'^posts/images$', PostImageUploadView.as_view(), name='post_image_upload'),
    url(r'^posts/likes/(?P<pid>\d+)/$',LikeOrDisDetailView.as_view(),name='likeordis_detail'),
    url(r'^posts/likeslist/(?P<pid>\d+)/$',LikeOrDisListView.as_view(),name='likeordis-list'),
    url(r'^posts/likes/post/$',LikeOrDisPostView.as_view(),name='likeordis-post'),
   	url(r'^posts/comments/post/$',PostCommentsPostView.as_view(),name = 'postcomments-post'),
   	url(r'^posts/comments/(?P<post_id>\d+)/$',PostCommentsListView.as_view(),name='postcomments-list'),
]

