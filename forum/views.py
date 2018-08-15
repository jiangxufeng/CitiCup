# -*- coding:utf-8 -*-
# author: jiangxf
# created: 2018-08-15

from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)
from .serializers import (
    PyPostPublishSerializer,
    PyPostDetailSerializer,
    UploadPostImageSerializer,
)
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import mixins, generics
from rest_framework.permissions import AllowAny
from .models import PostImage, Post
from rewrite.exceptions import FoundPostFailed
from account.models import LoginUser


# 发帖
class PostPublishView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = PyPostPublishSerializer

    def post(self, request):
        serializer = PyPostPublishSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            pk = serializer.validated_data['uid']
            title = serializer.validated_data['title']
            content = serializer.validated_data['content']
            # owner = get_authentication(pk=pk, sign=request.META.get("HTTP_SIGN"))
            owner = LoginUser.objects.get(pk=pk)
            passage = Post.objects.create(owner=owner, title=title, content=content)
            passage.save()
            msg = Response({
                'error': 0,
                'data': PyPostDetailSerializer(passage, context={'request': request}).data,
                'message': 'Success to publish the post.'
            }, HTTP_201_CREATED)
            return msg


# 某个帖子详情
class PostDetailView(mixins.RetrieveModelMixin,
                       generics.GenericAPIView):
    permission_classes = (AllowAny,)
    # authentication_classes = (ExpiringTokenAuthentication)
    serializer_class = PyPostDetailSerializer
    queryset = Post.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            cont = self.retrieve(request, *args, **kwargs)
            msg = Response(data={
                'error': 0,
                'data': cont.data,
                'message': 'Success to get the info.'
            }, status=HTTP_200_OK)
        except Http404:  # 获取失败，没有找到对应数据
            raise FoundPostFailed
        else:
            return msg

    def delete(self, request, pk):
        try:
            Post.objects.get(pk=pk).delete()
            return Response(status=HTTP_204_NO_CONTENT)
        except Http404:
            raise FoundPostFailed


# 上传图片
class PostImageUploadView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UploadPostImageSerializer

    def post(self, request):
        serializer = UploadPostImageSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            image = serializer.validated_data['image']
            images = PostImage.objects.create(image=image)
            images.save()
            msg = Response({
                'error': 0,
                'data': {'image': images.get_img_url()},
                'message': 'Success to upload the image'
            }, HTTP_201_CREATED)
            return msg
