# _*_ coding: utf-8 _*_

from __future__ import unicode_literals

from datetime import datetime

from django.db import models

# Create your models here.
from neoatigen.models import Patient


class UploadFile(models.Model):
    name = models.CharField(verbose_name=u'文件名', max_length=50, default='', null=True, blank=True)
    upload_file = models.FileField(upload_to = "patient/%Y/%m", verbose_name=u"上传文件",max_length=100)
    file_type = models.CharField(verbose_name=u"文件类型" , choices=(("pic", "图片"), ("pdf", "PDF"), ("others", "其它")), max_length=10)
    category = models.CharField(verbose_name=u"类别", choices=(("apply", "疫苗申请单"), ("MedRecord", "病历"), ("invoice", "发票"), ("express","快递单")), max_length=20, null=True, blank=True)
    patient = models.ManyToManyField(Patient, verbose_name=u"对应病人", null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"文件上传"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name