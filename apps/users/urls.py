# _*_ coding: utf-8 _*_
from django.conf.urls import url

from users.views import RegisterView, ActiveUserView, LoginView, LogoutView

__author__ = 'nestmilk'
__date__ = '2019/3/4 10:08'


urlpatterns = [
    #用户注册
    url(r'^register/$', RegisterView.as_view(), name='register'),

    #注册后，邮箱打开激活链接
    url(r'^active/(?P<active_code>.*)/', ActiveUserView.as_view(), name='user_active'),

    #用户登陆
    url(r'^login/$', LoginView.as_view(), name='login'),

    #退出登陆
    url(r'^logout/$', LogoutView.as_view(), name='logout'),

]