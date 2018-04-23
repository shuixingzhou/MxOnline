from django.urls import path
from .views import OrgView, AddUserAskView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView, AddFavView, \
    TeacherListView, TeacherDetailView

app_name = 'org'
urlpatterns = [
    path('list', OrgView.as_view(), name='org_index'),
    path('addask', AddUserAskView.as_view(), name='addask'),
    path('home/<int:org_id>', OrgHomeView.as_view(), name='org_detail_home'),
    path('course/<int:org_id>', OrgCourseView.as_view(), name='org_detail_course'),
    path('desc/<int:org_id>', OrgDescView.as_view(), name='org_detail_desc'),
    path('teacher/<int:org_id>', OrgTeacherView.as_view(), name='org_detail_teacher'),
    path('add_fav', AddFavView.as_view(), name='org_add_fav'),

    path('teacher/list', TeacherListView.as_view(), name='teacher_list'),
    path('teacher/detail/<int:teacher_id>', TeacherDetailView.as_view(), name='teacher_detail'),
]