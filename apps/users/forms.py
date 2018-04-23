from django import forms
from captcha.fields import CaptchaField

from .models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(min_length=5, required=True, max_length=16)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


class HeadimgUploadForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


class ModifyPasswordForm(forms.Form):
    password1 = forms.CharField(min_length=6, max_length=16, required=True)
    password2 = forms.CharField(min_length=6, max_length=16, required=True)


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'gender', 'birthday', 'address', 'mobile']