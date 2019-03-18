# _*_ encoding: utf-8 _*_

"""AJonline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.views.static import serve

import xadmin
from AJonline.settings import MEDIA_ROOT
from neoatigen.views import AddDealView, EditDealView, EditSpecimenView, \
    AddSpecimenView, NamePhoneQueryView, QueryResultView, EditPatientView, AddPatientView, EditExperimentView, \
    AddExperimentView, PatientsListView, PatientView, IndexView, EditAnalysisView, AddAnalysisView, EditPeptideView, \
    AddPeptideView, EditVaccineView, AddVaccineView

urlpatterns = [
    #配置html页面针对数据库中上传文件的访问处理函数,这个MDEIA_ROOT是自己引入的
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    url(r'^xadmin/', xadmin.site.urls),

    url(r'^$',IndexView.as_view(),name='index'),

    url(r'^patients_list/$', PatientsListView.as_view(), name='patients_list'),
    url(r'^patient_detail/(?P<patient_id>.*)/', PatientView.as_view(), name='patient_detail'),

    url(r'^add_patient/$', AddPatientView.as_view(), name='add_deal'),
    url(r'^edit_patient/$', EditPatientView.as_view(), name='edit_patient'),

    url(r'^add_deal/$', AddDealView.as_view(), name='add_deal'),
    url(r'^edit_deal/$', EditDealView.as_view(), name='edit_deal'),

    url(r'^add_specimen/$', AddSpecimenView.as_view(), name='add_specimen'),
    url(r'^edit_specimen/$', EditSpecimenView.as_view(), name='edit_specimen'),

    url(r'^name_phone_query/$', NamePhoneQueryView.as_view(), name='name_phone_query'),
    url(r'^query_result/$', QueryResultView.as_view(), name='query_result'),

    url(r'^add_experiment/$', AddExperimentView.as_view(), name='add_experiment'),
    url(r'^edit_experiment/$', EditExperimentView.as_view(), name='edit_experiment'),

    url(r'^add_analysis/$', AddAnalysisView.as_view(), name='add_analysis'),
    url(r'^edit_analysis/$', EditAnalysisView.as_view(), name='edit_analysis'),

    url(r'^add_peptide/$', AddPeptideView.as_view(), name='add_peptide'),
    url(r'^edit_peptide/$', EditPeptideView.as_view(), name='edit_peptide'),

    url(r'^add_vaccine/$', AddVaccineView.as_view(), name='add_vaccine'),
    url(r'^edit_vaccine/$', EditVaccineView.as_view(), name='edit_vaccine'),

    #用户相关url配置
    url(r'^users/', include('users.urls', namespace="users")),

    #上传文件url配置
    url(r'^files/', include('files.urls', namespace="files")),

    url(r'^captcha/', include('captcha.urls')),

]
