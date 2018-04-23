from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, HeadimgUploadForm, ModifyPasswordForm, UserInfoForm
from utils.email import send_register_email
import json


class CustomerBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'index.html')
                else:
                    return render(request, 'login.html', {'msg': '用户未激活'})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误', 'username': username, 'password': password})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')
            if UserProfile.objects.filter(email=email):
                return render(request, 'register.html', {'msg': '邮箱已存在', 'register_form': register_form})
            else:
                user_profole = UserProfile()
                user_profole.email = email
                user_profole.username = email
                user_profole.password = make_password(password)
                user_profole.is_active = False
                user_profole.save()
                send_register_email(email, 'register')
                return render(request, 'index.html')
        else:
            return render(request, 'register.html', {'register_form': register_form})
        return render(request, 'register.html')


class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
            return render(request, 'login.html')


class UserInfoView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'usercenter-info.html')
        else:
            return render(request, 'login.html')


class HeadimgUploadView(View):
    def post(self, request):
        form = HeadimgUploadForm(request.POST, request.FILES, instance=request.user)
        data = []
        if form.is_valid():
            request.user.save();
            data['success'] = True
            return JsonResponse(data)


class ModifyPassword(View):
    def post(self, request):
        form = ModifyPasswordForm(request.POST)
        data = {}
        if request.user.is_authenticated:
            if form.is_valid():
                pwd1 = request.POST.get('password1', '')
                pwd2 = request.POST.get('password2', '')
                if pwd1 != pwd2:
                    data['success'] = False
                    data['msg'] = '两次输入的密码不一致'
                    return JsonResponse(data)
                user = request.user
                user.password = make_password(pwd2)
                user.save()
                data['success'] = True
                return JsonResponse(data)
            data['success'] = False
            data['msg'] = json.dumps(form.errors, ensure_ascii=False)
            return JsonResponse(data)
        data['success'] = False
        data['msg'] = '用户未登录'
        return JsonResponse(data)


class SendEmailCodeView(View):
    def get(self, request):
        email = request.GET.get('email', '')
        data = {}
        if UserProfile.objects.filter(email=email):
            data['success'] = False
            data['msg'] = '邮箱已存在'
            return JsonResponse(data)
        else:
            send_register_email(email, 'update_email')
            data['success'] = True
            data['msg'] = '验证码已经发送'
            return JsonResponse(data)


class ModifyEmailView(View):
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        data = {}
        exist = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email')
        if exist:
            user = request.user
            user.email = email
            user.save()
            data['success'] = True
            return JsonResponse(data)
        else:
            data['success'] = False
            data['msg'] = '验证码错误'
            return JsonResponse(data)


class UserInfoSaveView(View):
    def post(self, request):
        userinfo_form = UserInfoForm(request.POST, instance=request.user)
        data = {}
        if userinfo_form.is_valid():
            userinfo_form.save()
            data['success'] = True
        else:
            data['success'] = False
            data['msg'] = json.dumps(userinfo_form.errors, ensure_ascii=False)
        return JsonResponse(data)


class UserCourseView(View):
    def get(self, request):
        return render(request, 'usercenter-mycourse.html')