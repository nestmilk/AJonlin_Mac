# _*_ coding: utf-8 _*_
from files.models import UploadFile

__author__ = 'nestmilk'
__date__ = '2019/3/8 11:37'

import xadmin

class UploadFileAdmin(object):
    list_display = ['id','name','upload_file','category', 'file_type','patient','add_time']
    search_fields = ['id','name','upload_file','category', 'file_type','patient__nick_name']
    list_filter = ['id','name','upload_file','category', 'file_type','patient','add_time']


xadmin.site.register(UploadFile, UploadFileAdmin)