# _*_ coding: utf-8 _*_
from users.models import EmailVerifyRecord, Banner

__author__ = 'nestmilk'
__date__ = '2019/1/13 22:03'

import xadmin

from xadmin import views

class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

class GlobalSetting(object):
    site_title = '艾进后台管理系统'
    site_footer = '上海艾进生物科技有限公司'
    menu_style = 'accordion'


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', "send_time",'send_type' ]
    search_fields = ['code', 'email', 'send_type' ]
    list_filter = ['code', 'email', "send_time",'send_type']


class BannerAdmin(object):
    list_display = ['title', 'image', "url", 'index', 'add_time']
    search_fields = ['title', 'image', "url", 'index']
    list_filter = ['title', 'image', "url", 'index', 'add_time']


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)

xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)