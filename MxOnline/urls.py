"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path

from django.views.generic import TemplateView
from users.views import LoginView, RegisterView, ActiveUserView
from organization.views import OrgView
import xadmin
from MxOnline.settings import MEDIA_ROOT
from django.views.static import serve


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    path('',TemplateView.as_view(template_name='index.html'), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('captcha/', include('captcha.urls')),
    path('active/<str:active_code>/', ActiveUserView.as_view()),
    re_path('^media/(?P<path>.*)$',serve, {"document_root": MEDIA_ROOT}),
    # 机构urls
    path('org/', include('organization.urls', namespace='org')),
    # 课程urls
    path('course/', include('courses.urls', namespace='course')),
    #用户个人中心
    path('users/', include('users.urls', namespace='users'))
]
