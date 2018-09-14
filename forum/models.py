# -*- coding:utf-8 -*-
# author: jiangxf
# created: 2018-08-15

from django.db import models
from django.conf import settings


# 发帖图片上传地址
def get_pyImage_upload_to(instance, filename):
    return 'Posts/' + filename


# 帖子
class Post(models.Model):
    # 发帖人
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts')
    # 帖子标题
    title = models.CharField(max_length=36, verbose_name="postTitle")
    # 帖子内容
    content = models.TextField(verbose_name="postContent", default="")
    # 发帖时间
    created_at = models.DateTimeField(auto_now_add=True)
    # view times
    viewtimes = models.IntegerField(default=0, null=False)
    # 标签
    tags = models.ManyToManyField("Tag", verbose_name="tags", null=True)
    # like
    like = models.IntegerField(default=0,null=False)
    # dislike
    diss = models.IntegerField(default=0,null=False)

    def __str__(self):
        return self.title


# 图片
class PostImage(models.Model):
    # 图片
    image = models.ImageField(upload_to=get_pyImage_upload_to, verbose_name="PyPostImages", null=False)

    def __str__(self):
        return self.image

    def get_img_url(self):
        return 'http://p9260z3xy.bkt.clouddn.com/' + str(self.image)


# 标签
class Tag(models.Model):
    # 标签名
    name = models.CharField(max_length=36, null=False, verbose_name="name")
    # 标签信息
    info = models.FloatField(default=0.0, null=False, verbose_name="info")

    def __str__(self):
        return self.name


class PostComments(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='postuser', null=False, blank=False)
    post = models.ForeignKey("Post", related_name='comments', null=False, blank=False)
    content = models.TextField(verbose_name="postContent", default="")
    created_at = models.DateTimeField(auto_now=True)
    userprefer = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username + self.post.title


class LikeOrDis(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='likeuser', null=False, blank=False)
    post = models.ForeignKey("Post", related_name='likes', null=False, blank=False)
    userprefer = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        unique_together = (('user', 'post'),)


# 历史记录
class History(models.Model):
    OPERATION_CHOICE = (
        (1, '发帖'),
        (2, '点赞'),
        (3, '踩'),
        (4, '评论')
    )
    # 用户
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='history')
    # 操作
    operation = models.IntegerField(default=1, choices=OPERATION_CHOICE, verbose_name="operation")
    # 收益
    income = models.FloatField(default=0.0, verbose_name='income')
    # 操作对象
    to = models.ForeignKey(Post, verbose_name='object')
    # 标签
    tags = models.CharField(max_length=144, default="", verbose_name="tags")

    def __str__(self):
        return self.user.username
