# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-15 01:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_merge_20180915_0036'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loginuser',
            name='posttags',
        ),
    ]