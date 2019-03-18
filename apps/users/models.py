# _*_ encoding: utf-8 _*_
from __future__ import unicode_literals

from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class UserProfile(AbstractUser):
    name = models.CharField(verbose_name=u"姓名", max_length=50, default="")
    age = models.IntegerField(verbose_name=u"年龄", default=0)
    gender = models.CharField(verbose_name=u"性别", max_length=10, choices=(("male",u"男"),("female",u"女"),("unknown",u"未知")),default="unknown")
    id_card = models.CharField(verbose_name=u"身份证号", max_length=18)
    address = models.CharField(verbose_name=u"地址", max_length=100,default="")
    mobile = models.CharField(verbose_name=u"手机号", max_length=11, default="")

    class Meta:
        verbose_name="用户信息"
        verbose_name_plural=verbose_name

    def __unicode__(self):
        return self.name


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20,verbose_name=u"验证码")
    email = models.EmailField(max_length=50,verbose_name=u"邮箱")
    send_type = models.CharField(verbose_name=u"验证码类型", choices=(("register",u"注册"),("forget",u"找回密码"), ("update_email",u"修改邮箱")), max_length=20)
    send_time = models.DateTimeField(verbose_name=u"发送时间", default=datetime.now)

    class Meta:
        verbose_name=u"邮箱验证码"
        verbose_name_plural=verbose_name

    def __str__(self):
        return '{0}({1})'.format(self.code, self.email)


class Banner(models.Model):
    title = models.CharField(max_length=100,verbose_name=u"标题")
    image = models.ImageField(upload_to="banner/%Y/%m", verbose_name=u"轮播图", max_length=100)
    url = models.URLField(max_length=200,verbose_name="访问地址")
    index = models.IntegerField(default=100,verbose_name=u"顺序")
    add_time= models.DateTimeField(default=datetime.now,verbose_name=u"添加时间")

    class Meta:
        verbose_name=u"轮播图"
        verbose_name_plural=verbose_name
