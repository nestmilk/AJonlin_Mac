# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-03-08 19:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0004_auto_20190308_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadfile',
            name='name',
            field=models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='\u6587\u4ef6\u540d'),
        ),
    ]