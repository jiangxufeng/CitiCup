# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-14 19:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20180914_1433'),
    ]

    operations = [
        migrations.AddField(
            model_name='loginuser',
            name='commenttags',
            field=models.CharField(default='{}', max_length=500),
        ),
        migrations.AlterField(
            model_name='loginuser',
            name='posttags',
            field=models.CharField(default='{}', max_length=500),
        ),
    ]
