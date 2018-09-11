# -*- coding:utf-8 -*-
# author: jiangxf
# created: 2018-08-14

from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^posts/$', PostListView.as_view(), name='post_list'),
    url(r'^posts/publish', PostPublishView.as_view(), name='post_publish'),
    url(r'^posts/user/$', PostOfUserListView.as_view(), name='post_of_user'),
    url(r'^posts/(?P<pk>\d+)/$', PostDetailView.as_view(), name='post-update'),
    url(r'^posts/new/$', PostNewListView.as_view(), name='post-new'),
    url(r'^posts/hot/$', PostHotListView.as_view(), name='post-hot'),
    url(r'^posts/recenthot/$', PostRecentHotListView.as_view(), name='post-recenthot'),
    url(r'^posts/tagposts/(?P<tag_id>\d+)/$', PostTagListView.as_view(), name='post-tagpost'),
    url(r'^posts/images/$', PostImageUploadView.as_view(), name='post_image_upload'),
    url(r'^posts/tags/$', TagListView.as_view(), name="post_tags"),
    url(r'^posts/likes/(?P<pid>\d+)/$',LikeOrDisDetailView.as_view(),name='likeordis_detail'),
    url(r'^posts/likeslist/(?P<pid>\d+)/$',LikeOrDisListView.as_view(),name='likeordis-list'),
    url(r'^posts/likes/post/$',LikeOrDisPostView.as_view(),name='likeordis-post'),
    url(r'^posts/comments/post/$', PostCommentsPostView.as_view(),name = 'postcomments-post'),
    url(r'^posts/comments/(?P<post_id>\d+)/$',PostCommentsListView.as_view(),name='postcomments-list'),
    url(r'^posts/getToken/$', TokenReturnView.as_view(), name="get_token"),
]

