# -*- coding:utf-8 -*-
# author: jiangxf
# created: 2018-08-15


from rest_framework.serializers import (
    SerializerMethodField,
    ImageField,
    IntegerField,
    HyperlinkedModelSerializer,
    HyperlinkedRelatedField,
    ModelSerializer
)

from .models import Post, PostImage


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
    uid = IntegerField()

    class Meta:
        model = Post
        fields = ('title', 'content', 'uid')


# 帖子详情
class PyPostDetailSerializer(HyperlinkedModelSerializer):
    owner = HyperlinkedRelatedField(view_name="user_detail", read_only=True)
    username = SerializerMethodField()
    pid = IntegerField(source='id')
    # headImg = SerializerMethodField()
    # likes = PostLikeReturnSerializer(many=True)
    # comments = PostCommentDetailSerializer(many=True)
    # pid = IntegerField(source='id')
    # images = PostImageReturnSerializer(many=True)

    class Meta:
        model = Post
        fields = ('owner', 'username', 'title', 'content', 'created_at', 'pid')

    def get_username(self, obj):
        return obj.owner.username
