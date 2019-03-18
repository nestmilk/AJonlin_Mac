# _*_ coding: utf-8 _*_
from datetime import datetime

from captcha.fields import CaptchaField
from django import forms

__author__ = 'nestmilk'
__date__ = '2019/3/4 10:13'


class RegisterForm(forms.Form):
    email = forms.EmailField(required = True)
    password = forms.CharField(required=True, min_length=6)
    captcha = CaptchaField(error_messages={"invalid":u"验证码错误"})


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=3)

