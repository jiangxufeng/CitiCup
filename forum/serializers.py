# -*- coding:utf-8 -*-
# author: jiangxf
# created: 2018-08-15


from rest_framework.serializers import (
    SerializerMethodField,
    ImageField,
    IntegerField,
    HyperlinkedModelSerializer,
    HyperlinkedRelatedField,
    ModelSerializer,
    CharField,
)

from .models import *


# 上传图片
class UploadPostImageSerializer(ModelSerializer):
    image = ImageField(allow_null=False)

    class Meta:
        model = PostImage
        fields = ('image',)


# 图片返回
class PostImageReturnSerializer(ModelSerializer):
    image = ImageField(allow_null=False)

    class Meta:
        model = PostImage
        fields = ('image',)


# 发布帖子
class PyPostPublishSerializer(ModelSerializer):


    class Meta:
        model = Post
        fields = ('title', 'content')

class PyPostUpdateSerializer(ModelSerializer):

    class Meta:
        model = Post
        fields = ('title','content')

# 帖子详情
class PyPostDetailSerializer(HyperlinkedModelSerializer):
    owner = HyperlinkedRelatedField(view_name="loginuser-detail", read_only=True)
    username = SerializerMethodField()
    pid = IntegerField(source='id',read_only=True)
    likesNum = SerializerMethodField()    

    class Meta:
        model = Post
        fields = ('owner', 'username', 'title', 'content', 'created_at', 'pid', 'likesNum')

    def get_username(self, obj):
        return obj.owner.username

    def get_likesNum(self, obj):
        return obj.postpost.all().count()


#登录用户观察自己是否点赞
class LikeOrDisDetailSerializer(ModelSerializer):

    class Meta:
        model = LikeOrDis
        fields = ('userprefer','created_at')


class LikeOrDisListSerializer(HyperlinkedModelSerializer):
    post_id = IntegerField(source='post.id')

    class Meta:
        model = LikeOrDis
        lookup_field = 'post_id'
        fields = ('user','userprefer','post_id')


class LikeOrDisPostSerializer(ModelSerializer):

    class Meta:
        model = LikeOrDis
        fields = ('post','userprefer')


class PostCommentPostSerializer(ModelSerializer):

    class Meta:
        model = PostComments
        fields = ('post','content')

class PostCommentListSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = PostComments
        fields = ('content','userprefer','created_at','user')

class PostCommentDetailSerializer(HyperlinkedModelSerializer):
    
    class Meta:
        pass



