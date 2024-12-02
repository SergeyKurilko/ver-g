import json
from lib2to3.fixes.fix_input import context

from django.core.paginator import Paginator
from django.db.models import Exists, OuterRef
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView

from education_platform.auth_forms import StudentLoginForm, StudentRegistrationForm
from education_platform.cache_models import get_cached_training_course_with_slug
from education_platform.course_process_views import course_progress_dashboard_view
from education_platform.models import TrainingCourse, AccessToCourse, CoursePack, AccessToCoursePack, CommentForStep, \
    CourseProgress


# Функция для определения является ли запрос ajax
def is_ajax(request):
  return request.headers.get('x-requested-with') == 'XMLHttpRequest'


class EducationPlatformHomeView(View):
    template_name = 'education_platform/education_home.html'

    def get(self, request, *args, **kwargs):
        latest_courses = TrainingCourse.objects.filter(published=True)[:6]
        latest_course_packs = CoursePack.objects.prefetch_related('courses').filter(published=True)[:6]

        context = {
            'latest_courses': latest_courses,
            'latest_course_packs': latest_course_packs,
        }

        if not request.user.is_authenticated:
            context['login_form'] = StudentLoginForm
            context['register_form'] = StudentRegistrationForm

        return render(request, self.template_name, context)


class TrainingCourseDetailView(DetailView):
    template_name = 'education_platform/course_detail.html'
    context_object_name = 'course'
    model = TrainingCourse
    slug_url_kwarg = 'course_slug'
    slug_field = 'slug'

    def get_object(self, queryset=None):
        course_slug = self.kwargs.get(self.slug_url_kwarg)
        return get_cached_training_course_with_slug(course_slug)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        context['blocks_count'] = course.blocks.all().count()
        points = 0
        # context['points_count'] = [for points in course.blocks.all()]
        context['difficulty_level'] = course.difficulty
        if not self.request.user.is_authenticated:
            context['login_form'] = StudentLoginForm
            context['register_form'] = StudentRegistrationForm
            return context
        else:
            return context


    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        # Проверка, есть ли у пользователя доступ к курсу уже (для аутентифицированного юзера)
        if request.user.is_authenticated:
            student = request.user.student
            course = self.object
            if not AccessToCourse.objects.filter(student=student, training_course=course).exists():
                # если нет доступа к курсу, то стандартное поведение
                return self.render_to_response(context)
            else:
                return course_progress_dashboard_view(self.request, student_pk=self.request.user.student.pk, course_pk=course.pk)
        else:
            # Если не аутентифицирован, то стандартное поведение
            return self.render_to_response(context)




class CoursePackDetailView(View):
    def get(self, request, course_pack_slug):
        context = {}

        course_pack = CoursePack.objects.get(
            slug=course_pack_slug
        )

        context['course_pack'] = course_pack
        courses_data = []


        # Если пользователь не авторизован, то добавляем в
        # контекст формы авторизации/регистрации
        if not self.request.user.is_authenticated:
            context['login_form'] = StudentLoginForm
            context['register_form'] = StudentRegistrationForm

            for course in course_pack.courses.all():
                courses_data.append({
                    "course": course,
                })



        # Проверка, есть ли доступ к этому пакету уже
        if self.request.user.is_authenticated:
            student = self.request.user.student
            context['access_to_course_pack'] = (
                AccessToCoursePack.objects.filter(student=student, course_pack=course_pack).exists())

            for course in course_pack.courses.all():
                courses_data.append({
                    "course": course,
                    "access_to_course": AccessToCourse.objects.filter(
                        student=student,
                        training_course_id=course.pk
                    ).exists()
                })




        context['courses_data'] = courses_data

        return render(request,
                      'education_platform/course_pack_detail.html',
                      context)


def course_pack_list(request):
    course_packs = CoursePack.objects.prefetch_related('courses').filter(published=True)
    context = {}

    if course_packs.count() == 0:
        context['no_published_course_packs'] = True

    #фильтрация по стоимости
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')

    if price_from:
        course_packs = course_packs.filter(price__gte=price_from)
    if price_to:
        course_packs = course_packs.filter(price__lte=price_to)

    paginator = Paginator(course_packs, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context['page_obj'] = page_obj

    if not request.user.is_authenticated:
        context['login_form'] = StudentLoginForm
        context['register_form'] = StudentRegistrationForm

    return render(request,
                  "education_platform/course_pack_list.html",
                  context)


def course_list_view(request):
    courses = TrainingCourse.objects.filter(published=True)
    context = {}

    if courses.count() == 0:
        context['no_published_courses'] = True

    difficulty_list = []
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')

    if price_from:
        courses = courses.filter(price__gte=price_from)
    if price_to:
        courses = courses.filter(price__lte=price_to)
    if request.GET.get('free') == 'on':
        courses = courses.filter(is_free=True)

    if request.GET.get('hard_level') == 'on':
        difficulty_list.append(3)
    if request.GET.get('normal_level') == 'on':
        difficulty_list.append(2)
    if request.GET.get('easy_level') == 'on':
        difficulty_list.append(1)

    if difficulty_list:
        courses = courses.filter(difficulty__in=difficulty_list)

    # Аннотация для проверки, подписан ли пользователь на курс
    if request.user.is_authenticated:
        student = request.user.student
        subscribed_annotation = Exists(
            AccessToCourse.objects.filter(
                student=student,
                training_course=OuterRef('pk')
            )
        )
        courses = courses.annotate(subscribed=subscribed_annotation)


    paginator = Paginator(courses, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    context['page_obj'] = page_obj

    if not request.user.is_authenticated:
        context['login_form'] = StudentLoginForm
        context['register_form'] = StudentRegistrationForm
    return render(request,
                  'education_platform/course_list.html',
                  context)


def get_cert_test_page(request, progress_pk):
    progress = CourseProgress.objects.get(pk=progress_pk)

    context = {
        'cert_num': progress.pk,
        'student_name': f"{progress.student.user.first_name} {progress.student.user.last_name}",
        'course_name': progress.training_course.title,
        'course_author': progress.training_course.author,
        'completed_date': progress.completed_date,
        'author_title': progress.training_course.author_title,
        'author_signature': progress.training_course.signature.url,
    }
    return render(request, 'education_platform/certificate_templates/certificate_template.html', context)

