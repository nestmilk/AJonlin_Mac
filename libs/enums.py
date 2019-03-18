# _*_ coding: utf-8 _*_
__author__ = 'nestmilk'
__date__ = '2019/1/24 13:31'


status_enum = {
    'InProgress': '进行中',
    'canceled':'已取消',
    'finished': '已完结',
    'unpaied': '未支付',
    'paid': '已支付',
    'unknown':'未知',
    'success':'成功',
    'fail':'失败',
    'sent':'已寄出'
}

gender_enum = {
    'male': '男',
    'female': '女',
    'unknown': '未知'
}

sample_type_enum = {
    'FFPE': '蜡块',
    'BLOOD': '全血',
    'FreshTissue': '新鲜组织',
    'ParaffinSlice':'白片'
}

unit_enum = {
    'block':'块',
    'piece':'片',
    'tube':'管',
    'mg':'毫克',
    'g':'克'
}

experiment_type_enum = {
    'WES':'全外显子测序',
    'TS':'RNA测序'
}

company_enum = {
    'SF':'顺丰快递',
    'YT':'圆通快递',
    'ST':'申通快递',
    'YD':'韵达快递',
    'ZS':'自送',
    'WuXi':'药明康德',
    'NovoGene':'诺禾致源',
    'CloudHealth':'云健康',
    'gl':'吉尔',
    'cp':'中肽'
}
