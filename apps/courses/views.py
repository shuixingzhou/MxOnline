from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import JsonResponse

from .models import Course
from operation.models import UserFavorite, UserCourse, CourseComments


class CourseListView(View):
    def get(self, request):
        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1
        all_courses = Course.objects.all()
        keyword = request.GET.get('keyword')
        if keyword:
            all_courses = all_courses.filter(name__icontains=keyword)
        sort = request.GET.get('sort')
        if sort == 'students':
            all_courses = all_courses.order_by('-students')
        elif sort == 'hot':
            all_courses = all_courses.order_by('-click_nums')
        else:
            all_courses = all_courses.order_by('-add_time')

        p = Paginator(all_courses,9, request=request)
        courses = p.page(page)
        hot_courses = Course.objects.order_by('-students')[:3]
        return render(request, 'course-list.html',{
            'all_courses': courses,
            'hot_courses': hot_courses,
            'sort': sort,
        })


class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id,fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id,fav_type=2):
                has_fav_org = True
        students = course.usercourse_set.all()[:5]
        recommends = Course.objects.filter(~Q(id=course.id), course_org=course.course_org)[:3]
        return render(request, 'course-detail.html',{
            'course': course,
            'students': students,
            'recommends': recommends,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org,
        })


class CourseVideoView(View):
    def get(self,request, course_id):

        if request.user.is_authenticated:
            course = Course.objects.get(id=int(course_id))
            if UserCourse.objects.filter(user=request.user,course=course):
                pass
            else:
                user_course = UserCourse()
                user_course.user = request.user
                user_course.course = course
                user_course.save()
                course.students += 1
                course.save()
            return render(request, 'course-video.html', {
                'course': course,
            })
        else:
            return render(request,'login.html')


class CourseCommentView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_comments = course.coursecomments_set.all().order_by('-add_time')
        return render(request, 'course-comment.html',{
            'course': course,
            'all_comments': all_comments,
        })


class AddCommentView(View):
    def post(self, request):
        return_data = {}
        if request.user.is_authenticated:
            comment = request.POST.get('comments', '')
            course_id = request.POST.get('course_id', 0)
            if int(course_id)>0 and comment:
                course_comment = CourseComments()
                course = Course.objects.get(id=int(course_id))
                course_comment.user = request.user
                course_comment.course = course
                course_comment.comments = comment
                course_comment.save()
                return_data['success'] = True
                return JsonResponse(return_data)
        else:
            return_data['success'] = False
            return_data['msg'] = '用户未登录'
            return JsonResponse(return_data)