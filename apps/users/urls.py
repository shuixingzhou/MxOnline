from django.urls import path
from .views import UserInfoView, HeadimgUploadView, ModifyPassword, SendEmailCodeView, ModifyEmailView, UserInfoSaveView, UserCourseView

app_name = 'users'
urlpatterns = [
    path('info', UserInfoView.as_view(), name='info'),
    path('headimg/upload', HeadimgUploadView.as_view(), name='headimg_upload'),
    path('modifypasssword', ModifyPassword.as_view(), name ='modify_password'),
    path('send_email_code', SendEmailCodeView.as_view(), name ='send_email_code'),
    path('modify_email', ModifyEmailView.as_view(), name='modify_email'),
    path('save_info', UserInfoSaveView.as_view(), name='save_info'),
    path('course', UserCourseView.as_view(), name='course'),
]