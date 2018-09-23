# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-14 21:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_auto_20180914_1957'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loginuser',
            name='commenttags',
        ),
        migrations.RemoveField(
            model_name='loginuser',
            name='posttags',
        ),
        migrations.AddField(
            model_name='loginuser',
            name='tags',
            field=models.CharField(default='[{}, {}, {}]', max_length=1280),
        ),
    ]
