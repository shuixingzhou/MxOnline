from django.urls import path

from .views import CourseListView, CourseDetailView,CourseVideoView, CourseCommentView, AddCommentView

app_name = 'course'
urlpatterns = [
    path('list', CourseListView.as_view(), name='course_list'),
    path('detail/<int:course_id>', CourseDetailView.as_view(), name='course_detail'),
    path('video/<int:course_id>', CourseVideoView.as_view(), name='course_video'),
    path('comment/<int:course_id>', CourseCommentView.as_view(), name='course_comment'),
    path('add_comment', AddCommentView.as_view(), name='course_add_comment'),
]