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
from django.shortcuts import get_object_or_404
from .serializers import *
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import mixins, generics
from rest_framework.permissions import AllowAny
from .models import *
from rewrite.exceptions import FoundPostFailed
from account.models import LoginUser
from rest_framework.authentication import (
    SessionAuthentication,
    BasicAuthentication,
    )
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from account.permissions import IsOwnerOrReadOnly,IsUserOrReadOnly
from rewrite.authentication import CsrfExemptSessionAuthentication

# 发帖
class PostPublishView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PyPostPublishSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request):
        '''已登录用户发帖'''
        serializer = PyPostPublishSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data['title']
            content = serializer.validated_data['content']
            passage = Post.objects.create(title=title, content=content, owner=request.user)
            passage.save()
            msg = Response({
                'error': 0,
                'data': PyPostDetailSerializer(passage, context={'request': request}).data,
                'message': 'Success to publish the post.'
            }, HTTP_201_CREATED)
            return msg


# 
# class PostDetailView(generics.RetrieveAPIView):

#     serializer_class = PyPostDetailSerializer
#     queryset = Post.objects.all()
#     permission_classes = (IsOwnerOrReadOnly,)
#     authentication_classes = (SessionAuthentication,)


#     def get(self, request, *args, **kwargs):
#         '''返回一个帖子详情'''

#         try:
#             cont = self.retrieve(request, *args, **kwargs)
#             msg = Response(data={
#                 'error': 0,
#                 'data': cont.data,
#                 'message': 'Success to get the info.'
#             }, status=HTTP_200_OK)
#         except Http404:  # 获取失败，没有找到对应数据
#             raise FoundPostFailed
#         else:
#             return msg

#     def delete(self, request, pk):
#         '''已登录用户根据id删除一个帖子'''
#         obj = self.get_object() 
#         self.check_object_permissions(self.request, obj)
#         try:
#             Post.objects.get(pk=pk).delete()
#             return Response(status=HTTP_204_NO_CONTENT)
#         except Http404:
#             raise FoundPostFailed 

# 某个帖子详情
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    '''
    get:
        获取文章信息

    put:
        登录用户更新本人所发文章内容 

    delete:
        登录用户删除本人整篇文章

    '''

    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (IsOwnerOrReadOnly,IsAuthenticated)
    serializer_class = PyPostDetailSerializer
    queryset = Post.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'pid'



# 上传图片
class PostImageUploadView(generics.GenericAPIView):
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


class LikeOrDisDetailView(generics.RetrieveUpdateDestroyAPIView):

    '''
    get:
        已登录用户获取自己是否赞/踩这个帖子

    put:
        已登录用户更新自己对一篇文章喜好程度

    delete:
        已登录用户取消喜好

    '''
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = LikeOrDisDetailSerializer
    queryset = LikeOrDis.objects.all()


    def get(self,request,pid):   

        queryset = LikeOrDis.objects.filter(post_id = pid,user = request.user)
        s = LikeOrDisDetailSerializer(queryset,many=True,context={'request': request})
        return Response(s.data)

    def put(self,request,pid):

        s = LikeOrDisDetailSerializer(data=request.data)
        
        if s.is_valid(raise_exception=True):
            lod = LikeOrDis.objects.filter(post_id=pid ,user_id = request.user.id)
            if lod:
                userprefer = s.validated_data['userprefer']
                lod.update(userprefer = userprefer)
                msg = Response({
                    'error': 0,
                    'message': 'Success to update'
                }, HTTP_200_OK)
            else:
                msg = Response({
                    'error': 0,
                    'message': 'Failed to update. You do not like it before.'
                }, HTTP_400_BAD_REQUEST)
        else:
            msg = Response({
                'error': 0,
                'message': 'BAD_REQUEST'
            }, HTTP_400_BAD_REQUEST)
        return msg


    def delete(self,request,pid):
        try:
            s = LikeOrDis.objects.get(post_id=pid ,user_id = request.user.id)
            s.delete()
            msg = Response({
                    'error': 0,
                    'message': 'Success to delete'
                }, HTTP_200_OK)
        except:
            msg = Response({
                'error': 0,
                'message': 'BAD_REQUEST'
            }, HTTP_400_BAD_REQUEST)

        return msg




class LikeOrDisListView(generics.ListAPIView):
    '''
    get:
        列出这篇文章所有点赞/踩的人

    '''
    permission_classes = (AllowAny,)
    queryset = LikeOrDis.objects.all()
    serializer_class = LikeOrDisListSerializer
    authentication_classes = ()


    def get(self,request,pid):
        queryset = LikeOrDis.objects.filter(post_id = pid)
        s = LikeOrDisListSerializer(queryset,many=True,context={'request': request})
        return Response(s.data)



class LikeOrDisPostView(generics.CreateAPIView):

    '''
    post:
        已登录用户赞/踩一个帖子
    
    '''

    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = LikeOrDisPostSerializer


    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

    def post(self,request, *args, **kwargs):
        post_id = request.data.get('post','')
        user = request.user
        res = LikeOrDis.objects.filter(user=user,post_id=post_id)
        if res:
            msg = Response(data={
                'error': 0000,
                'message': 'You have already like it.'
            }, status=HTTP_400_BAD_REQUEST)
            return msg
        else:
            return self.create(request, *args, **kwargs)




class PostCommentsPostView(generics.CreateAPIView):
    '''
    post:
        已登录用户对一个文章发布评论
    '''

    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = PostCommentPostSerializer

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)


class PostCommentsListView(generics.GenericAPIView):
    '''
    get:
        列出所有这篇文章的评论信息

    '''
    permission_classes = (AllowAny,)
    queryset = PostComments.objects.all()
    serializer_class = PostCommentListSerializer
    authentication_classes = ()


    def get(self,request,post_id):
        queryset = PostComments.objects.filter(post_id = post_id)
        s = PostCommentListSerializer(queryset,many=True,context={'request': request})
        return Response(s.data)



