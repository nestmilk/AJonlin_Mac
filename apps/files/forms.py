# _*_ coding: utf-8 _*_
from files.models import UploadFile

__author__ = 'nestmilk'
__date__ = '2019/3/8 13:21'

from django import forms


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadFile
        fields = ['name','file_type','category','upload_file']