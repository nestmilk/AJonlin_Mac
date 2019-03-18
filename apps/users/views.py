# _*_ encoding: utf-8 _*_
from django.contrib.auth import authenticate, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import login
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View

from users.forms import RegisterForm, LoginForm
from users.models import UserProfile, EmailVerifyRecord
from users.utils.email_send import send_register_email


class CustomBackends(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get("email","")
            try:
                if UserProfile.objects.get(email=email):
                    return render(request, "register.html", {"register_form": register_form, "msg": "邮箱已经存在！"})
            except UserProfile.DoesNotExist:
                pass
            password = request.POST.get("password","")
            user_profile = UserProfile()
            user_profile.username = email
            user_profile.email = email
            user_profile.is_active = False
            user_profile.password = make_password(password)
            user_profile.save()

            send_status = send_register_email(email, "register")
            if send_status:
                return render(request, "login.html", {"msg":"请先去邮箱激活！！"})
            else:
                return render(request, "register.html",{"register_form": register_form, "msg":"邮件发送失败"})
        else:
            return render(request, "register.html", {"register_form": register_form})


class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email = email)
                user.is_active = True
                user.save()
        else:
            return render(request, "active_fail.html")

        return render(request, "login.html")


class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, "login.html", {"msg": "账号尚未激活！"})

            else:
                return render(request, "login.html", {"msg": "账号或密码错误！"})
        else:
            return render(request, "login.html", {"login_form": login_form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))