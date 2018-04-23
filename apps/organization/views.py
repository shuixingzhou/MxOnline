from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, JsonResponse


from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .models import CourseOrg, CityDict, Teacher
from .forms import UserAskForm
from operation.models import UserFavorite


class OrgView(View):
    def get(self, request):
        all_city = CityDict.objects.all()
        all_org = CourseOrg.objects.all()
        hot_org = all_org.order_by('-click_nums')[:3]
        #取出城市
        city_id = request.GET.get('city', '')
        #类别
        categroy = request.GET.get('ct', '')
        #排序
        sort = request.GET.get('sort','')
        if city_id:
            all_org = all_org.filter(city_id=int(city_id))
        if categroy:
            all_org = all_org.filter(categroy= categroy)
        total = all_org.count()
        if sort:
            if sort == 'students':
                all_org = all_org.order_by('-students')
            elif sort == 'courses':
                all_org = all_org.order_by('-course_nums')
        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_org,1, request=request)
        orgs = p.page(page)
        return render(request, 'org-list.html',{
            'all_org': orgs,
            'all_city': all_city,
            'city_id': city_id,
            'categroy': categroy,
            'total': total,
            'hot_org': hot_org,
            'sort': sort,
        })


class AddUserAskView(View):
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            userask = userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"添加出错"}', content_type= 'application/json')


class OrgHomeView(View):
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_course = course_org.course_set.all()[:3]
        all_teacher = course_org.teacher_set.all()[:3]
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user,fav_id=course_org.id,fav_type=2):
                has_fav = True
        return render(request, 'org-detail-homepage.html',{
            'course_org': course_org,
            'all_course': all_course,
            'all_teacher': all_teacher,
            'current_page': 'home',
            'has_fav':has_fav,
        })


class OrgCourseView(View):
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_course = course_org.course_set.all()
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user,fav_id=course_org.id,fav_type=2):
                has_fav = True
        return render(request, 'org-detail-course.html',{
            'course_org': course_org,
            'all_course': all_course,
            'current_page': 'course',
            'has_fav': has_fav,
        })


class OrgDescView(View):
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user,fav_id=course_org.id,fav_type=2):
                has_fav = True
        return render(request, 'org-detail-desc.html',{
            'course_org': course_org,
            'current_page': 'desc',
            'has_fav': has_fav,
        })


class OrgTeacherView(View):
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teacher = course_org.teacher_set.all()[:3]
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user,fav_id=course_org.id,fav_type=2):
                has_fav = True
        return render(request, 'org-detail-teachers.html',{
            'course_org': course_org,
            'all_teacher': all_teacher,
            'current_page': 'teacher',
            'has_fav': has_fav,
        })


class AddFavView(View):
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)
        return_data = {}
        if not request.user.is_authenticated:
            return_data['success'] = False
            return_data['msg'] = '用户未登录'
            return JsonResponse(return_data)

        exists_record = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exists_record:
            exists_record.delete()
            return_data['success'] = True
            return_data['msg'] = '收藏'
            return JsonResponse(return_data)
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                return_data['success'] = True
                return_data['msg'] = '已收藏'
            else:
                return_data['success'] = False
                return_data['msg'] = '未知错误'
            return JsonResponse(return_data)


class TeacherListView(View):
    def get(self,request):
        all_teacher = Teacher.objects.all()
        sort = request.GET.get('sort', '')
        if sort:
            all_teacher = all_teacher.order_by('-click_nums')
        count = all_teacher.count()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_teacher, 1, request=request)
        teachers = p.page(page)
        teacher_rank = Teacher.objects.all().order_by('-click_nums')[:5]
        return render(request, 'teachers-list.html',{
            'all_teacher': teachers,
            'count': count,
            'sort': sort,
            'teacher_rank': teacher_rank,
        })


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher_rank = Teacher.objects.all().order_by('-click_nums')[:5]
        has_fav_teacher = False
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user,fav_id=int(teacher.id),fav_type='3'):
                has_fav_teacher = True
            if UserFavorite.objects.filter(user=request.user, fav_id=int(teacher.org_id), fav_type='2'):
                has_fav_org = True
        return render(request, 'teacher-detail.html',{
            'teacher': teacher,
            'teacher_rank': teacher_rank,
            'has_fav_teacher': has_fav_teacher,
            'has_fav_org': has_fav_org,
        })