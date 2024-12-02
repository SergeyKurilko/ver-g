from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.core.files.storage import default_storage
from django.utils import timezone

from blog.models import Article
from education_platform.models import CourseProgress, Student, TrainingCourse


def get_my_personal_account(request):
    if not request.user.is_authenticated:
        return redirect("education_platform:home")
    else:
        student = request.user.student
        progresses = CourseProgress.objects.filter(student=student)
        completed_courses_count = progresses.filter(is_completed=True).count()
        context = {
            "student": student,
            "progresses": progresses,
            "completed_courses_count": completed_courses_count
        }

        return render(request, "education_platform/personal_account.html", context)


# @login_required(redirect_field_name=reverse("education_platform:home"))
def avatar_upload_ajax(request):
    """
    Принимает ajax запрос из скрипта. В теле так же имеется форма с файлом аватара
    """
    if request.method == "POST":
        # Проверка, когда последний раз пользователь обновлял данные
        last_avatar_update_time = request.session.get('last_avatar_update_time')
        if last_avatar_update_time:
            since_update_time = timezone.now() - timezone.datetime.fromisoformat(last_avatar_update_time)
            if since_update_time.total_seconds() < 60:
                return JsonResponse({
                    "status": "time_error",
                    "message": "Слишком часто. Попробуйте обновить через две минуты."
                })
        student = get_object_or_404(Student, pk=request.user.student.pk)
        avatar = request.FILES.get("avatar")

        # Проверка, есть ли сейчас файл аватара
        if student.avatar:
            # Получаем путь до расположения файла
            old_avatar_path = student.avatar.path

            # Проверяем, через default_storage есть ли там файл и удаляем, если есть
            if default_storage.exists(old_avatar_path):
                default_storage.delete(old_avatar_path)

        # Сохраняем новый аватар
        student.avatar = avatar
        student.save()

        request.session['last_avatar_update_time'] = timezone.now().isoformat()

        return JsonResponse({
            "status": "success",
            "message": "avatar is changed"
        })
    else:
        redirect("education_platform:home")


@login_required(login_url="education_platform:home")
def update_personal_data_ajax(request):
    if request.method == "POST":
        # Проверка, когда последний раз пользователь обновлял данные
        last_update_time = request.session.get('last_update_personal_data')
        if last_update_time:
            since_update_time = timezone.now() - timezone.datetime.fromisoformat(last_update_time)
            if since_update_time.total_seconds() < 60:
                return JsonResponse({
                    "status": "time_error",
                    "message": "Слишком часто. Попробуйте обновить через две минуты."
                })

        user = request.user

        # Проверка, есть ли еще лимит на изменение персональных данных
        if not user.student.edit_limit > 0:
            return JsonResponse({
                "status": "edit_limit_error",
                "message": "Лимит изменений персональных данных исчерпан"
            })

        # Преобразуем полученные данные в словарь
        form_data_dict = request.POST.dict()


        # Сохраним текущие данные, чтобы сделать финальную проверку,
        # изменилось ли хоть одно поле?
        old_user_first_name = request.user.first_name
        old_user_last_name = request.user.last_name
        old_user_email = request.user.email

        # Сравниваем полученные данные с данными в полях user
        # Если отличаются, то обновляем
        if (form_data_dict['email']).lower() != user.email:
            if len(form_data_dict['email']) < 1:
                return JsonResponse({
                    "status": "email-error",
                    "message": f"Поле не может быть пустым."
                })
            if not User.objects.filter(email=(form_data_dict['email']).lower()).exists():
                user.email = (form_data_dict['email']).lower()
            else:
                return JsonResponse({
                    "status": "email-error",
                    "message": f"Пользователь с такой почтой уже зарегистрирован."
                })
        if form_data_dict['first_name'] != user.first_name:
            user.first_name = form_data_dict['first_name']
        if form_data_dict['last_name'] != user.last_name:
            user.last_name = form_data_dict['last_name']

        # Сравним, поменялись ли данные по итогу

        if (old_user_first_name != user.first_name
                or old_user_last_name != user.last_name
                or old_user_email != user.email):
            user.student.edit_limit -= 1
            user.student.save()
            user.save()

        # Записываем в сессию время последнего редактирования данных
        request.session['last_update_personal_data'] = timezone.now().isoformat()

        return JsonResponse({
            "status": "success",
            "message": "Получен запрос на апдейт личных данных"
        })


def my_courses_view(request):
    """
    Возвращает список курсов, на которые подписан студент,
    а так же список рекомендованных курсов
    """
    if not request.user.is_authenticated:
        return redirect("education_platform:home")
    else:
        student = request.user.student

        # Определим title для списка курсов в зависимости от фильтров
        course_list_title = 'Все мои курсы'

        # Определяем параметр фильтра, если он пришел в request
        filter_param = request.GET.get('filter', False)

        # Если нет параметра filter, то берем за основу коллекцию из всех CourseProgress
        if not filter_param:
            progresses = CourseProgress.objects.filter(student=student).order_by('-last_action')
        else:
            # Проверяем, какое значение в параметре и, в зависимости от этого фильтруем
            if filter_param == 'completed':
                course_list_title = 'Завершенные курсы'
                progresses = CourseProgress.objects.filter(
                    student=student,
                    is_completed=True
                ).order_by('-last_action')
            elif filter_param == 'incompleted':
                course_list_title = 'Незавершенные курсы'
                progresses = CourseProgress.objects.filter(
                    student=student,
                    is_completed=False
                ).order_by('last_action')
            else:
                progresses = CourseProgress.objects.filter(student=student).order_by('-last_action')

        progresses_data = []

        # PK курсов, на которые уже подписан пользователь
        courses_pks_from_progresses = []

        for progress in progresses:
            courses_pks_from_progresses.append(progress.training_course.pk)
            completed_steps = progress.completed_steps.count()
            total_steps = progress.training_course.get_steps_quantity()

            course_complete_in_percent = (completed_steps * 100) / int(total_steps)

            progress = {
                "course_title": progress.training_course.title,
                "course_image": progress.training_course.image,
                "course_author": progress.training_course.author,
                "course_url": progress.training_course.get_absolute_url(),
                "course_description": progress.training_course.description,
                "course_completed_counter": progress.training_course.completed_counter,
                "course_time_to_study": progress.training_course.time_to_study,
                "course_difficulty": progress.training_course.get_difficulty_display(),
                "course_complete_in_percent": course_complete_in_percent,
                "total_points": progress.training_course.get_points_quantity()[0],
            }

            progresses_data.append(progress)

        recommended_courses = TrainingCourse.objects.exclude(pk__in=courses_pks_from_progresses).filter(published=True)[0:6]
        completed_courses_count = progresses.filter(is_completed=True).count()
        latest_articles_from_blog = Article.objects.filter(published=True)[0:6]
        context = {
            "student": student,
            "progresses_data": progresses_data,
            "completed_courses_count": completed_courses_count,
            "my_courses_total_count": progresses.count(),
            "course_list_title": course_list_title,
            "recommended_courses": recommended_courses,
            "latest_articles": latest_articles_from_blog,
        }

    return render(request, 'education_platform/my_courses.html', context)


def my_certificates(request):
    """
    Возвращает все завершенные CourseProgress для рендера списка сертификатов,
    а так же общую статистику по завершенным курсам и подпискам
    """
    if not request.user.is_authenticated:
        return redirect("education_platform:home")
    else:
        student = request.user.student

    completed_progresses = CourseProgress.objects.filter(student=student, is_completed=True)
    completed_progresses_count = completed_progresses.count()
    total_progresses_count = CourseProgress.objects.filter(student=student).count()

    context = {
        'completed_progresses': completed_progresses,
        'completed_progresses_count': completed_progresses_count,
        'total_progresses_count': total_progresses_count,
        'student': student
    }

    return render(request,
                  template_name='education_platform/my_certificates.html',
                  context=context
                  )
