# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-01-23 14:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('neoatigen', '0005_auto_20190123_1352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analysis',
            name='name',
            field=models.CharField(default='', max_length=20, unique=True, verbose_name='\u672c\u5730\u5206\u6790\u7f16\u53f7'),
        ),
        migrations.AlterField(
            model_name='deal',
            name='name',
            field=models.CharField(default='', max_length=50, unique=True, verbose_name='\u8ba2\u5355\u7f16\u53f7'),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='CRO_name',
            field=models.CharField(default='', max_length=100, unique=True, verbose_name='\u5916\u5305\u5b9e\u9a8c\u7f16\u53f7'),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='name',
            field=models.CharField(default='', max_length=20, unique=True, verbose_name='\u672c\u5730\u5b9e\u9a8c\u7f16\u53f7'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='name',
            field=models.CharField(default='', max_length=50, unique=True, verbose_name='\u75c5\u4eba\u7f16\u53f7'),
        ),
        migrations.AlterField(
            model_name='peptide',
            name='name',
            field=models.CharField(default='', max_length=20, unique=True, verbose_name='\u672c\u5730\u5408\u6210\u7f16\u53f7'),
        ),
        migrations.AlterField(
            model_name='specimen',
            name='name',
            field=models.CharField(default='', max_length=20, unique=True, verbose_name='\u672c\u5730\u6837\u672c\u7f16\u53f7'),
        ),
        migrations.AlterField(
            model_name='specimen',
            name='original_name',
            field=models.CharField(default='', max_length=100, unique=True, verbose_name='\u539f\u59cb\u6837\u672c\u7f16\u53f7'),
        ),
        migrations.AlterField(
            model_name='vaccine',
            name='name',
            field=models.CharField(default='', max_length=20, unique=True, verbose_name='\u75ab\u82d7\u5236\u5907\u7f16\u53f7'),
        ),
    ]
