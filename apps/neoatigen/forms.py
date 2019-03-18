# _*_ coding: utf-8 _*_
import re

from django import forms

from neoatigen.models import Deal, Patient, Specimen, Experiment, Analysis, Peptide, Vaccine

__author__ = 'nestmilk'
__date__ = '2019/2/22 15:30'


class DealForm(forms.ModelForm):
    class Meta:
        model = Deal
        fields = ['name', 'price', 'invoice', 'status', 'pay_status']


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'nick_name', 'age', 'gender', 'id_card','address', 'diagnosis', 'mobile', 'add_time']

    def clean_mobile(self):
        """
        验证手机号码是否合法
        """
        mobile = self.cleaned_data['mobile']
        REGES_MOBILE = "^((13[0-9])|(14[5,7])|(15[0-3,5-9])|(17[0,3,5-8])|(18[0-9])|166|198|199|(147))\d{8}$"
        p = re.compile(REGES_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u"手机号码非法", code="mobile_invalid")


class SpecimenForm(forms.ModelForm):
    class Meta:
        model = Specimen
        fields = ['name', 'original_name', 'site', 'sample_type','num', 'location']


class QueryForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['nick_name', 'mobile']

    def clean_mobile(self):
        """
        验证手机号码是否合法
        """
        mobile = self.cleaned_data['mobile']
        REGES_MOBILE = "^((13[0-9])|(14[5,7])|(15[0-3,5-9])|(17[0,3,5-8])|(18[0-9])|166|198|199|(147))\d{8}$"
        p = re.compile(REGES_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u"手机号码非法", code="mobile_invalid")

class ExperimentForm(forms.ModelForm):
    class Meta:
        model = Experiment
        fields =['name','experiment_type','CRO_name','CRO_company','express_company','express_number'
                 ,'price','status','pay_status','result_status','add_time','finish_time']


class AddExperimentForm(forms.ModelForm):
    class Meta:
        model = Experiment
        fields =['name','experiment_type','CRO_name','CRO_company','express_company','express_number'
                 ,'price','status','pay_status','result_status']


class AnalysisForm(forms.ModelForm):
    class Meta:
        model = Analysis
        fields = ['name', 'status', 'add_time', 'finish_time']


class AddAnalysisForm(forms.ModelForm):
    class Meta:
        model = Analysis
        fields= ['name']


class PeptideForm(forms.ModelForm):
    class Meta:
         model = Peptide
         fields = ['name','CRO_name','CRO_company','num','quantity','unit','price','status','pay_status','add_time','finish_time']


class AddPeptideForm(forms.ModelForm):
    class Meta:
        model = Peptide
        fields = ['name', 'CRO_name', 'CRO_company', 'num', 'quantity', 'unit', 'price', 'status', 'pay_status']


class VaccineForm(forms.ModelForm):
    class Meta:
        model = Vaccine
        fields = ['name','status','express_company','express_number','add_time','finish_time']


class AddVaccineForm(forms.ModelForm):
    class Meta:
        model = Vaccine
        fields = ['name', 'status', 'express_number', 'express_company']