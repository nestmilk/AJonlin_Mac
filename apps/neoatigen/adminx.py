# _*_ coding: utf-8 _*_
__author__ = 'nestmilk'
__date__ = '2019/1/21 13:55'


import xadmin

from models import Patient, Deal, Specimen, Experiment, Analysis, Peptide, Vaccine

class DealInline(object):
    model = Deal
    extra = 0


class SpecimenInline(object):
    model = Specimen
    extra = 0


class PatientAdmin(object):
    list_display = ['id','name','nick_name','age','gender', 'id_card', 'address','diagnosis','mobile','add_time']
    search_fields = ['id','name','nick_name','age','gender', 'id_card', 'address','diagnosis','mobile']
    list_filter =['id','name','nick_name','age','gender', 'id_card', 'address','diagnosis','mobile','add_time']
    relfield_style = 'fk-ajax'
    inlines = [DealInline, SpecimenInline]


class DealAdmin(object):
    list_display = ['id','name','price','invoice', 'status','pay_status', 'add_time','patient']
    search_fields = ['id','name','price','invoice','status','pay_status','patient__name','patient__nick_name']
    list_filter = ['id','name','price','invoice','status','pay_status', 'add_time','patient']


class SpecimenAdmin(object):
    list_display = ['id','name', 'original_name', 'sample_type','num', 'site','location', 'add_time','patient']
    search_fields = ['id','name', 'original_name', 'sample_type','num', 'site','location', 'patient__name', 'patient__nick_name']
    list_filter = ['id','name', 'original_name', 'sample_type','num','site', 'location', 'add_time','patient']


class ExperimentAdmin(object):
    list_display = ['id','name', 'CRO_name','CRO_company','experiment_type','express_company','express_number','price','status','pay_status','result_status','add_time','specimen','deal','patient']
    search_fields = ['id','name', 'CRO_name','CRO_company','experiment_type','express_company','express_number','price','status','pay_status','result_status','specimen__name','deal__name','patient__nick_name','patient__name']
    list_filter = ['id','name', 'CRO_name','CRO_company','experiment_type','express_company','express_number','price','status','pay_status','result_status','add_time','specimen','deal','patient']


class AnalysisAdmin(object):
    list_display = ['id','name','status','add_time','experiment','patient']
    search_fields = ['id','name','status','experiment__name','patient__nick_name','patient__name']
    list_filter = ['id','name','status','add_time','experiment','patient']


class PeptideAdmin(object):
    list_display = ['id','name','CRO_name','CRO_company','price','status','pay_status','add_time','analysis','patient']
    search_fields = ['id','name','CRO_name','CRO_company','price','status','pay_status','analysis__name','patient__nick_name','patient__name']
    list_filter = ['id','name','CRO_name','CRO_company','price','status','pay_status','add_time','analysis','patient']


class VaccineAdmin(object):
    list_display = ['id','name','status','express_company','express_number','add_time','peptide','patient']
    search_fields = ['id','name','status','express_company','express_number','peptide__name','patient__nick_name','patient__name']
    list_filter = ['id','name','status','express_company','express_number','add_time','peptide','patient']



xadmin.site.register(Patient, PatientAdmin)
xadmin.site.register(Deal, DealAdmin)
xadmin.site.register(Specimen, SpecimenAdmin)
xadmin.site.register(Experiment, ExperimentAdmin)
xadmin.site.register(Analysis,AnalysisAdmin)
xadmin.site.register(Peptide, PeptideAdmin)
xadmin.site.register(Vaccine,VaccineAdmin)
