# _*_ coding: utf-8 _*_
from datetime import datetime
import json

from django.contrib.auth.hashers import make_password
from django.db import models, transaction
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View
from pure_pagination import Paginator, PageNotAnInteger

from files.models import UploadFile
from neoatigen.forms import DealForm, SpecimenForm, QueryForm, PatientForm, ExperimentForm, AddExperimentForm, \
    AnalysisForm, AddAnalysisForm, PeptideForm, AddPeptideForm, VaccineForm, AddVaccineForm
from users.models import Banner
from users.utils.mixin_utils import LoginRequiredMixin

from neoatigen.models import Patient, Experiment, Specimen, Analysis, Deal, Peptide, Vaccine


def eight(str):
    length = 8- len(str)
    new_str=''
    for i in range(0,length):
        new_str+='0'
    new_str+=str
    return  new_str


# class DealView(View):
#     def get(self,request):
#         # patient_all_information = PatientAllInformation()
#         # patient_all_information.patient = PatientViewModel(Patient.objects.first())
#         # d1 = DealViewModel(Deal.objects.get(patient = Patient.objects.first()))
#         # d2 = d1
#         # patient_all_information.deals.append(d1)
#         # patient_all_information.deals.append(d2)
#         all = []
#         for patient in Patient.objects.all().order_by('add_time'):
#             patient_all_information = PatientAllInformation()
#             patient_vo = PatientViewModel(patient)
#             patient_all_information.patient = patient_vo
#             try:
#                 deal_set = patient.deal_set.all()
#                 patient_all_information.deals = [DealViewModel(deal) for deal in deal_set]
#             except Deal.DoesNotExist:
#                 pass
#
#             try:
#                 specimen_set = patient.specimen_set.all()
#                 patient_all_information.specimens = [SpecimenViewModel(specimen) for specimen in specimen_set]
#             except Specimen.DoesNotExist:
#                 all.append(patient_all_information)
#                 continue
#
#             experiment_set = set()
#             for specimen in specimen_set:
#                 try:
#                     experiments = set(list(Experiment.objects.filter(specimen = specimen)))
#                 except Experiment.DoesNotExist:
#                     experiments = set()
#                 experiment_set = set.union(experiment_set, experiments)
#             if experiment_set:
#                 patient_all_information.experiments = [ExperimentViewModel(experiment) for experiment in experiment_set]
#             else:
#                 all.append(patient_all_information)
#                 continue
#
#             analysis_set = set()
#             for experiment in experiment_set:
#                 try:
#                     analyses = set(list(Analysis.objects.filter(experiment=experiment)))
#                 except Analysis.DoesNotExist:
#                     analyses = set()
#                 analysis_set = set.union(analysis_set, analyses)
#             if analysis_set:
#                 patient_all_information.analyses = [AnalysisViewModel(analysis) for analysis in analysis_set]
#             else:
#                 all.append(patient_all_information)
#                 continue
#
#             peptide_set = set()
#             for analysis in analysis_set:
#                 try:
#                     peptides = set(list(Peptide.objects.filter(analysis = analysis)))
#                 except Peptide.DoesNotExist:
#                     peptides = set()
#                 peptide_set = set.union(peptide_set, peptides)
#             if peptide_set:
#                 patient_all_information.peptides = [PeptideViewModel(peptide) for peptide in peptide_set]
#             else:
#                 all.append(patient_all_information)
#                 continue
#
#             vaccine_set = set()
#             for peptide in peptide_set:
#                 try:
#                     vaccines = set(list(Vaccine.objects.filter(peptide = peptide)))
#                 except Vaccine.DoesNotExist:
#                     vaccines = set()
#                 vaccine_set = set.union(vaccine_set, vaccines)
#             patient_all_information.vaccines = [VaccineViewModel(vaccine) for vaccine in vaccine_set]
#
#             all.append(patient_all_information)
#
#         return render(request, "overview_all.html", {"all": all})


class IndexView(View):
    """
    艾进后台首页
    """
    def get(self,request):
        all_banners = Banner.objects.all().order_by('index')
        return render(request, 'index.html', {
            "all_banners": all_banners,
        })



class PatientsListView(LoginRequiredMixin, View):
    def get(self,request):
        all_patients = Patient.objects.all().order_by('-add_time')

        #搜索
        nick_name = request.GET.get('nick_name',"")
        if nick_name:
            all_patients = all_patients.filter(nick_name__icontains=nick_name)

        mobile = request.GET.get('mobile', "")
        if mobile:
            all_patients = all_patients.filter(mobile__icontains=mobile)

        invoice = request.GET.get('invoice', "")
        if invoice:
            all_patients = all_patients.filter(deal__invoice__icontains=invoice)

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_patients, 10, request=request)

        patients = p.page(page)

        return render(request, "patients-list.html", {
            "all_patients": patients
        })


class PatientView(LoginRequiredMixin, View):
    def get(self, request, patient_id):
        patient = Patient.objects.get(id=patient_id)
        all_deals = patient.deal_set.all().order_by("-add_time")
        all_specimens = patient.specimen_set.all().order_by("-add_time")

        all_experiments = Experiment.objects.filter(patient_id=patient_id)
        all_analyses = Analysis.objects.filter(patient_id=patient_id)
        all_peptides = Peptide.objects.filter(patient_id=patient_id)
        all_vaccines  = Vaccine.objects.filter(patient_id=patient_id)
        all_applies = UploadFile.objects.filter(patient=patient, category='apply')
        all_MedRecords = UploadFile.objects.filter(patient=patient, category='MedRecord')

        return render(request, 'patient_detail.html', {
            "patient": patient,
            "all_deals": all_deals,
            "all_specimens": all_specimens,
            "all_experiments": all_experiments,
            "all_analyses": all_analyses,
            "all_peptides": all_peptides,
            "all_vaccines": all_vaccines,
            "all_applies": all_applies,
            "all_MedRecords": all_MedRecords,

        })


class AddDealView(LoginRequiredMixin, View):
    """
    添加订单
    """
    def post(self, request):
        deal_form = DealForm(request.POST)
        patient_id = request.POST.get('patient_id')
        if deal_form.is_valid():
            patient = Patient.objects.get(id= patient_id)
            deal = Deal(
                name= deal_form.cleaned_data['name'],
                price = deal_form.cleaned_data['price'],
                invoice = deal_form.cleaned_data['invoice'],
                status = deal_form.cleaned_data['status'],
                pay_status = deal_form.cleaned_data['pay_status'],
                patient = patient
            )
            deal.save()
            return HttpResponse(json.dumps({"status": "success"}),content_type="application/json")
        else:
            s = json.dumps({"status": "fail", "errors": deal_form.errors})
            return HttpResponse(json.dumps({"status": "fail", "errors": deal_form.errors}),content_type="application/json")


class EditDealView(LoginRequiredMixin, View):
    """
    修改订单
    """
    def post(self,request):
        deal_id = request.POST.get("deal_id")
        deal = Deal.objects.get(id=deal_id)

        deal_form = DealForm(request.POST, instance=deal)
        if deal_form.is_valid():
            deal_form.save()
            return HttpResponse(json.dumps({"status": "success"}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"status": "fail", "errors": deal_form.errors}),
                                content_type="application/json")


class AddSpecimenView(LoginRequiredMixin, View):
    """
    添加样本信息
    """
    def post(self,request):
        specimen_form = SpecimenForm(request.POST)
        patient_id = request.POST.get('patient_id')
        if specimen_form.is_valid():
            patient = Patient.objects.get(id=patient_id)
            specimen = Specimen()
            specimen.name = specimen_form.cleaned_data['name']
            specimen.original_name =specimen_form.cleaned_data['original_name']
            specimen.sample_type=specimen_form.cleaned_data['sample_type']
            specimen.num=specimen_form.cleaned_data['num']
            specimen.site=specimen_form.cleaned_data['site']
            specimen.location=specimen_form.cleaned_data['location']
            specimen.patient=patient
            specimen.save()
            return HttpResponse(json.dumps({"status": "success"}),content_type="application/json")
        else:
            return HttpResponse(json.dumps({"status": "fail", "errors": specimen_form.errors}),
                                content_type="application/json")


class EditSpecimenView(LoginRequiredMixin, View):
    """
    修改样本信息
    """
    def post(self,request):
        specimen_id = request.POST.get('specimen_id')
        specimen = Specimen.objects.get(id=specimen_id)
        specimen_form = SpecimenForm(request.POST,instance=specimen)
        if specimen_form.is_valid():
            specimen_form.save()
            return HttpResponse(json.dumps({"status": "success"}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"status": "fail", "errors": specimen_form.errors}),
                                content_type="application/json")


class NamePhoneQueryView(View):
    """
    通过姓名和电话查询疫苗进度
    """
    def get(self,request):
        return render(request, 'name_phone_query.html', {})


class QueryResultView(View):
    """
    疫苗进度查询结果
    """
    def post(self,request):
        query_form = QueryForm(request.POST)
        if query_form.is_valid():
            nick_name = query_form.cleaned_data['nick_name']
            mobile = query_form.cleaned_data['mobile']
            try:
                patient = Patient.objects.get(nick_name=nick_name, mobile=mobile)
                all_experiments = Experiment.objects.filter(patient=patient)
                all_analyses = Analysis.objects.filter(patient=patient)
                all_peptides = Peptide.objects.filter(patient=patient)
                all_vaccines = Vaccine.objects.filter(patient=patient)
                return render(request, 'query_result.html', {
                    "patient": patient,
                    "all_experiments": all_experiments,
                    "all_analyses": all_analyses,
                    "all_peptides": all_peptides,
                    "all_vaccines": all_vaccines,

                })
            except Patient.DoesNotExist:
                return render(request, 'name_phone_query.html', {
                    "msg": "您查询的用户不存在，请重新输入！",
                    "nick_name": request.POST.get('nick_name'),
                    "mobile": request.POST.get('mobile'),
                })
        else:
            return render(request, 'name_phone_query.html',{
                "errors": query_form.errors,
                "nick_name": request.POST.get('nick_name'),
                "mobile": request.POST.get('mobile'),
            })



class AddPatientView(LoginRequiredMixin, View):
    """
    增加病人信息
    """
    def post(self, request):
        patient_form = PatientForm(request.POST)

        if patient_form.is_valid():
            patient_form.save()
            return HttpResponse(json.dumps({"status": "success"}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"status": "fail", "errors": patient_form.errors}),
                                content_type="application/json")

class EditPatientView(LoginRequiredMixin, View):
    """
    修改病人信息
    """
    def post(self,request):
        patient = Patient.objects.get(id=request.POST.get('patient_id'))
        patient_form = PatientForm(request.POST, instance=patient)
        if patient_form.is_valid():
            patient_form.save()
            return HttpResponse(json.dumps({"status": "success"}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"status": "fail", "errors": patient_form.errors}),
                            content_type="application/json")


class AddExperimentView(LoginRequiredMixin, View):
    """
    添加实验
    """
    @transaction.atomic
    def post(self, request):
        patient_id = request.POST.get("patient_id")
        add_experiment_form = AddExperimentForm(request.POST)

        if add_experiment_form.is_valid():
            experiment = add_experiment_form.save()

            experiment.patient = Patient.objects.get(id=patient_id)

            specimen_id_list = request.POST.getlist('specimen_id_list')
            specimen_list = Specimen.objects.filter(id__in=specimen_id_list)

            deal_id_list = request.POST.getlist('deal_id_list')
            deal_list = Deal.objects.filter(id__in=deal_id_list)

            experiment.specimen = specimen_list
            experiment.deal = deal_list
            experiment.save()
            return HttpResponse(json.dumps({"status": "success"}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"status": "fail", "errors": add_experiment_form.errors}),
                                content_type="application/json")


class EditExperimentView(LoginRequiredMixin, View):
    """
    修改实验信息
    """
    def post(self, request):
        experiment_id = request.POST.get('experiment_id')
        experiment = Experiment.objects.get(id=experiment_id)

        if_edit_finish_time = False
        # 判断之前是否实验状态为进行中，之后改为已结束，就把结束时间进行修改
        if experiment.status == 'InProgress' and request.POST.get('status') != 'InProgress':
            if_edit_finish_time = True

        experiment_form = ExperimentForm(request.POST, instance=experiment)
        specimen_id_list = request.POST.getlist('specimen_id_list')
        deal_id_list = request.POST.getlist('deal_id_list')
        if experiment_form.is_valid():
            experiment_form.save()
            specimen_list = Specimen.objects.filter(id__in=specimen_id_list)
            deal_list = Deal.objects.filter(id__in=deal_id_list)
            experiment.specimen = specimen_list
            experiment.deal = deal_list
            if if_edit_finish_time:
                experiment.finish_time = datetime.now()
            experiment.save()
            return HttpResponse(json.dumps({"status": "success"}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"status": "fail", "errors": experiment_form.errors}),
                                content_type="application/json")


class AddAnalysisView(LoginRequiredMixin, View):
    """
    添加分析信息
    """
    @transaction.atomic
    def post(self, request):
        add_analysis_form = AddAnalysisForm(request.POST)
        if add_analysis_form.is_valid():
            analysis = add_analysis_form.save()

            experiment_id_list = request.POST.getlist('experiment_id_list')
            experiment_list = Experiment.objects.filter(id__in=experiment_id_list)
            analysis.experiment =experiment_list

            patient_id = request.POST.get('patient_id')
            patient = Patient.objects.get(id=patient_id)
            analysis.patient = patient

            analysis.save()
            return HttpResponse(json.dumps({"status": "success"}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"status": "fail", "errors": add_analysis_form.errors}),
                                content_type="application/json")


class EditAnalysisView(LoginRequiredMixin, View):
    """
    编辑分析信息
    """
    @transaction.atomic
    def post(self, request):
        analysis_id = request.POST.get('analysis_id')
        analysis = Analysis.objects.get(id=analysis_id)

        if_edit_finish_time = False
        # 判断之前是否分析状态为进行中，之后改为已结束，就把结束时间进行修改
        if analysis.status == 'InProgress' and request.POST.get('status') != 'InProgress':
            if_edit_finish_time = True

        analysis_form = AnalysisForm(request.POST, instance=analysis)
        experiment_id_list = request.POST.getlist('experiment_id_list')
        if analysis_form.is_valid():
            analysis_form.save()
            experiment_list = Experiment.objects.filter(id__in=experiment_id_list)
            analysis.experiment = experiment_list
            if if_edit_finish_time:
                analysis.finish_time = datetime.now()
            analysis.save()
            return HttpResponse(json.dumps({"status": "success"}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"status": "fail", "errors": analysis_form.errors}),
                                content_type="application/json")


class AddPeptideView(LoginRequiredMixin, View):
    """
    添加多肽信息
    """
    @transaction.atomic
    def post(self,request):
        add_peptide_form=AddPeptideForm(request.POST)
        patient_id = request.POST.get('patient_id')
        analysis_id_list = request.POST.getlist('analysis_id_list')

        if add_peptide_form.is_valid():
            peptide = add_peptide_form.save()
            patient = Patient.objects.get(id=patient_id)
            peptide.patient = patient
            analysis_list = Analysis.objects.filter(id__in=analysis_id_list)
            peptide.analysis = analysis_list
            peptide.save()
            return HttpResponse(json.dumps({"status": "success"}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"status": "fail", "errors": add_peptide_form.errors}),
                                content_type="application/json")


class EditPeptideView(LoginRequiredMixin, View):
    """
    编辑多肽信息
    """
    @transaction.atomic
    def post(self, request):
        peptide_id = request.POST.get('peptide_id')
        peptide = Peptide.objects.get(id=peptide_id)

        if_edit_finish_time = False
        # 判断之前是否分析状态为进行中，之后改为已结束，就把结束时间进行修改
        if peptide.status == 'InProgress' and request.POST.get('status') != 'InProgress':
            if_edit_finish_time = True

        peptide_form = PeptideForm(request.POST, instance=peptide)
        analysis_id_list = request.POST.getlist('analysis_id_list')
        if peptide_form.is_valid():
            peptide_form.save()
            analysis_list = Analysis.objects.filter(id__in=analysis_id_list)
            peptide.analysis = analysis_list

            if if_edit_finish_time:
                peptide.finish_time = datetime.now()

            peptide.save()
            return HttpResponse(json.dumps({"status": "success"}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"status": "fail", "errors": peptide_form.errors}),
                                content_type="application/json")


class AddVaccineView(LoginRequiredMixin, View):
    """
    添加疫苗信息
    """
    @transaction.atomic
    def post(self, request):
        patient_id = request.POST.get('patient_id')
        peptide_id_list = request.POST.getlist('peptide_id_list')
        add_vaccine_form = AddVaccineForm(request.POST)
        if add_vaccine_form.is_valid():
            vaccine=add_vaccine_form.save()
            patient = Patient.objects.get(id=patient_id)
            vaccine.patient = patient
            peptide_list = Peptide.objects.filter(id__in=peptide_id_list)
            vaccine.peptide =peptide_list
            vaccine.save()
            return HttpResponse(json.dumps({"status": "success"}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"status": "fail", "errors": add_vaccine_form.errors}),
                                content_type="application/json")


class EditVaccineView(LoginRequiredMixin, View):
    """
    添加疫苗信息
    """
    @transaction.atomic
    def post(self, request):
        vaccine_id = request.POST.get('vaccine_id')
        vaccine = Vaccine.objects.get(id=vaccine_id)

        if_edit_finish_time = False
        # 判断之前是否分析状态为进行中，之后改为已结束，就把结束时间进行修改
        if vaccine.status == 'InProgress' and request.POST.get('status') != 'InProgress':
            if_edit_finish_time = True

        vaccine_form = VaccineForm(request.POST,instance=vaccine)
        peptide_id_list = request.POST.getlist('peptide_id_list')
        if vaccine_form.is_valid():
            vaccine = vaccine_form.save()
            peptide_list = Peptide.objects.filter(id__in = peptide_id_list)
            vaccine.peptide = peptide_list
            if if_edit_finish_time:
                vaccine.finish_time = datetime.now()
            vaccine.save()
            return HttpResponse(json.dumps({"status": "success"}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"status": "fail", "errors": vaccine_form.errors}),
                                content_type="application/json")
