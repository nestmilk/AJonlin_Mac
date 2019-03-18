# _*_ coding: utf-8 _*_

from __future__ import unicode_literals

from datetime import datetime

from django.db import models

# Create your models here.


class Patient(models.Model):
    name = models.CharField(verbose_name=u"病人编号", max_length=50, default="", unique=True)
    nick_name = models.CharField(verbose_name=u"姓名", max_length=50, default="", null=True, blank=True)
    age = models.IntegerField(verbose_name=u"年龄", default=0, null=True, blank=True)
    gender = models.CharField(verbose_name=u"性别", max_length=10,
                              choices=(("male", u"男"), ("female", u"女"), ("unknown", u"*")), default="unknown")
    id_card = models.CharField(verbose_name=u"身份证号", max_length=18, null=True, blank=True)
    address = models.CharField(verbose_name=u"地址", max_length=100, default="", null=True, blank=True)
    diagnosis = models.CharField(verbose_name=u"诊断结果", max_length=100, default="", null=True, blank=True)
    mobile = models.CharField(verbose_name=u"手机号", max_length=11, default="", null=True, blank=True)
    add_time = models.DateField(verbose_name=u"添加时间", default= datetime.now)

    class Meta:
        verbose_name = "病人信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name + " " + self.nick_name


class Specimen(models.Model):
    name = models.CharField(verbose_name=u"本地样本编号", max_length=20, default="", unique=True)
    original_name = models.CharField(verbose_name= u"原始样本编号", max_length=100, default="", null=True, blank=True)
    sample_type = models.CharField(verbose_name=u"样本类型", max_length=15, choices=(("FFPE", u"蜡块"),("BLOOD", u"全血"),("FreshTissue",u"新鲜组织"),("ParaffinSlice",u"白片")))
    num = models.IntegerField(verbose_name=u"数量", default=1)
    site = models.CharField(verbose_name=u"取样部位",max_length=50,default="", null=True, blank=True)
    location = models.CharField(verbose_name=u"样品保存位置",max_length=50,default="", null=True, blank=True)
    add_time = models.DateTimeField(verbose_name=u"到样时间", default= datetime.now)
    patient = models.ForeignKey(Patient, verbose_name=u"对应病人", null=True, blank=True)

    class Meta:
        verbose_name = "样本信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class Deal(models.Model):
    name = models.CharField(verbose_name=u"订单编号", max_length=50, default="", unique=True)
    price = models.IntegerField(verbose_name=u"价格", default=0)
    invoice= models.CharField(verbose_name=u"发票号", max_length=20,default="",  null=True, blank=True)
    status = models.CharField(verbose_name=u"订单状态",max_length=10, choices=(("InProgress",u"进行中"),("canceled", u"已取消"),("finished",u"已完结")),default="InProgress")
    pay_status = models.CharField(verbose_name=u"付费状态",max_length=10, choices=(("unpaied",u"未支付"),("paid",u"已支付")),default="unpaied")
    add_time = models.DateTimeField(verbose_name=u"添加时间", default= datetime.now)
    patient = models.ForeignKey(Patient, verbose_name=u"对应病人")

    class Meta:
        verbose_name = "订单信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name



class Experiment(models.Model):
    name = models.CharField(verbose_name=u"本地实验编号", max_length=20, default="", unique=True)
    CRO_name = models.CharField(verbose_name=u"外包实验编号", max_length=100, default="", null=True, blank=True)
    CRO_company = models.CharField(verbose_name=u"外包公司名称",max_length=50, choices=(("WuXi",u"药明康德"),("NovoGene",u"诺禾致源"),("CloudHealth",u"云健康")),default="WuXi")
    experiment_type = models.CharField(verbose_name=u"实验类型", max_length=15, choices=(
    ("WES", u"全外显子测序"), ("TS", u"RNA测序")),default="WES")
    express_company = models.CharField(verbose_name=u"快递公司",max_length=10,choices=(("SF",u"顺丰快递"),("YT",u"圆通快递"),("ST",u"申通快递"),("YD",u"韵达快递"),("ZS",u"自送")),default="SF")
    express_number = models.CharField(verbose_name=u"快递单号",max_length=20, null=True, blank=True)
    price = models.IntegerField(verbose_name=u"价格", default=0)
    status = models.CharField(verbose_name=u"实验状态", max_length=10,
                              choices=(("InProgress", u"进行中"), ("canceled", u"已取消"), ("finished", u"已完结")),
                              default="InProgress")
    pay_status = models.CharField(verbose_name=u"支付状态", max_length=10, choices=(("unpaied", u"未支付"), ("paid", u"已支付")),
                                  default="unpaied")
    result_status = models.CharField(verbose_name=u"实验结果", max_length=10, choices=(("unknown", u"未知"),("success", u"成功"), ("fail", u"失败")),
                                  default="unknown")
    add_time = models.DateTimeField(verbose_name=u"开始时间", default=datetime.now)
    finish_time = models.DateTimeField(verbose_name=u"结束时间", null=True, blank=True)
    specimen = models.ManyToManyField(Specimen, verbose_name=u"对应样本")
    deal = models.ManyToManyField(Deal,verbose_name=u'对应订单')
    patient = models.ForeignKey(Patient, verbose_name=u"对应病人", null=True, blank=True)


    class Meta:
        verbose_name = "实验信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class Analysis(models.Model):
    name = models.CharField(verbose_name=u"本地分析编号", max_length=20, default="", unique=True)
    status = models.CharField(verbose_name=u"分析状态", max_length=10,
                              choices=(("InProgress", u"进行中"), ("canceled", u"已取消"), ("finished", u"已完结")),
                              default="InProgress")
    add_time = models.DateTimeField(verbose_name=u"开始时间", default=datetime.now)
    finish_time = models.DateTimeField(verbose_name=u"结束时间",  null=True, blank=True)
    experiment = models.ManyToManyField(Experiment, verbose_name=u"对应实验")
    patient = models.ForeignKey(Patient, verbose_name=u"对应病人", null=True, blank=True)


    class Meta:
        verbose_name = "分析信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class Peptide(models.Model):
    name = models.CharField(verbose_name=u"本地合成编号", max_length=20, default="", unique=True)
    CRO_name = models.CharField(verbose_name=u"外包合成编号", max_length=100, default="", null=True, blank=True)
    CRO_company = models.CharField(verbose_name=u"外包公司名称",max_length=50, choices=(("gl",u"吉尔"),("cp",u"中肽")),default="gl")
    num = models.IntegerField(verbose_name=u"多肽条数",default=0)
    quantity = models.IntegerField(verbose_name=u"单条多肽订购量", default=5)
    unit = models.CharField(verbose_name=u"单位",max_length=10, choices=(("mg",u"毫克"),("g",u"克")),default="mg")
    price = models.IntegerField(verbose_name=u"价格", default=0)
    status = models.CharField(verbose_name=u"合成状态", max_length=10,
                              choices=(("InProgress", u"进行中"), ("canceled", u"已取消"), ("finished", u"已完结")),
                              default="InProgress")
    pay_status = models.CharField(verbose_name=u"支付状态", max_length=10, choices=(("unpaied", u"未支付"), ("paid", u"已支付")),
                                  default="unpaied")
    add_time = models.DateTimeField(verbose_name=u"开始时间", default=datetime.now)
    finish_time = models.DateTimeField(verbose_name=u"结束时间",  null=True, blank=True)
    analysis = models.ManyToManyField(Analysis, verbose_name=u"对应分析")
    patient = models.ForeignKey(Patient, verbose_name=u"对应病人", null=True, blank=True)


    class Meta:
        verbose_name = "多肽信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class Vaccine(models.Model):
    name = models.CharField(verbose_name=u"疫苗制备编号", max_length=20, default="", unique=True)
    status = models.CharField(verbose_name=u"制备状态", max_length=10,
                              choices=(("InProgress", u"进行中"), ("canceled", u"已取消"), ("finished", u"已完成"),("sent", u"已寄出")),
                              default="InProgress")
    express_company = models.CharField(verbose_name=u"快递公司", max_length=10,
                                       choices=(("SF", u"顺丰快递"), ("YT", u"圆通快递"), ("ST", u"申通快递"), ("YD", u"韵达快递")),
                                       default="SF")
    express_number = models.CharField(verbose_name=u"快递单号", max_length=20, null=True, blank=True)
    add_time = models.DateTimeField(verbose_name=u"开始时间", default=datetime.now)
    finish_time = models.DateTimeField(verbose_name=u"结束时间",  null=True, blank=True)

    peptide = models.ManyToManyField(Peptide, verbose_name=u"对应多肽")
    patient = models.ForeignKey(Patient, verbose_name=u"对应病人", null=True, blank=True)


    class Meta:
        verbose_name = "疫苗信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

