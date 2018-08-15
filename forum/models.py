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
