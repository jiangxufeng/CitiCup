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


# 标签
class TagReturnSerializer(ModelSerializer):

    class Meta:
        model = Tag
        fields = ('name',)


# 发布帖子
class PyPostPublishSerializer(ModelSerializer):
    tag = CharField()

    class Meta:
        model = Post
        fields = ('title', 'content', 'tag', 'degree')


class PyPostUpdateSerializer(ModelSerializer):

    class Meta:
        model = Post
        fields = ('title', 'content')


# 帖子列表
class PostListSerializer(HyperlinkedModelSerializer):
    owner = HyperlinkedRelatedField(view_name="loginuser-detail", read_only=True)
    username = SerializerMethodField()
    commentsNum = SerializerMethodField()
    pid = IntegerField(source='id')
    tags = TagReturnSerializer(many=True)

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related('owner')
        return queryset

    class Meta:
        model = Post
        fields = ('owner', 'username', 'title', 'content', 'tags',
                  'created_at', 'pid', 'like', 'diss', 'commentsNum', 'degree')

    def get_likesNum(self, obj):
        return obj.likes.all().count()

    def get_commentsNum(self, obj):
        return obj.comments.all().count()

    def get_username(self, obj):
        return obj.owner.username


# 帖子详情
class PyPostDetailSerializer(HyperlinkedModelSerializer):
    owner = HyperlinkedRelatedField(view_name="loginuser-detail", read_only=True)
    username = SerializerMethodField()
    pid = IntegerField(source='id', read_only=True)
    tags = TagReturnSerializer(many=True)

    class Meta:
        model = Post
        fields = ('owner', 'username', 'title', 'content', 'created_at', 'pid', 'like','diss', 'tags', 'degree')

    def get_username(self, obj):
        return obj.owner.username

    def get_likesNum(self, obj):
        return obj.likes.all().count()


# 登录用户观察自己是否点赞
class LikeOrDisDetailSerializer(ModelSerializer):

    class Meta:
        model = LikeOrDis
        fields = ('times', 'created_at', 'tags')


class LikeOrDisListSerializer(HyperlinkedModelSerializer):
    post_id = IntegerField(source='post.id')

    class Meta:
        model = LikeOrDis
        lookup_field = 'post_id'
        fields = ('user','times','post_id')


class LikeOrDisPostSerializer(ModelSerializer):

    class Meta:
        model = LikeOrDis
        fields = ('post', 'times', 'tags')


class PostCommentPostSerializer(ModelSerializer):

    class Meta:
        model = PostComments
        fields = ('post', 'content', 'userprefer', 'tags')


class PostCommentListSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = PostComments
        fields = ('content', 'userprefer', 'created_at', 'user')


class PostCommentDetailSerializer(HyperlinkedModelSerializer):
    
    class Meta:
        pass


# 返回所有标签
class TagDetailSerializer(ModelSerializer):

    class Meta:
        model = Tag
        fields = ("name", "id")
