# _*_ coding: utf-8 _*_
import os

from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View

from files.forms import UploadFileForm
from neoatigen.models import Patient
from users.utils.mixin_utils import LoginRequiredMixin


class UploadFileView(LoginRequiredMixin, View):
    """
    处理上传文件
    """
    @transaction.atomic
    def post(self,request):
        upload_file_form = UploadFileForm(request.POST, request.FILES)
        patient_id = request.POST.get('patient_id')
        if upload_file_form.is_valid():
            upload_file = upload_file_form.save()
            if upload_file.name == '':
                file_name =os.path.basename(upload_file.upload_file.name)
                upload_file.name = file_name
            patient = Patient.objects.get(id=patient_id)
            upload_file.patient = [patient]
            upload_file.save()
            return HttpResponseRedirect(
                reverse('patient_detail', kwargs={'patient_id':patient_id})
            )
        else:
            return render(request, 'error_message.html', {
                "title": "上传文件失败",
                "errors": upload_file_form.errors,
                "patient_id": patient_id,
                "url": request.META['HTTP_REFERER'],
            })


