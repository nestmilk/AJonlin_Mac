# _*_ coding: utf-8 _*_

from django.conf.urls import url

from files.views import UploadFileView

__author__ = 'nestmilk'
__date__ = '2019/3/8 11:35'

urlpatterns = [
    #用户注册
    url(r'^upload_file/$', UploadFileView.as_view(), name='upload_file'),

]