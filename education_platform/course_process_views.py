from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse

from education_platform.cache_models import get_cached_training_course, get_cached_step_comments, \
    get_cached_promo_in_dashboard
from education_platform.models import CourseProgress, Student, TrainingCourse, AccessToCourse, StepForPoint, \
    PointForTrainingBlock, QuestionForStep


def course_progress_dashboard_view(request, student_pk, course_pk):
    student = Student.objects.get(pk=student_pk)
    course = get_cached_training_course(course_pk)
    course_progress, created = CourseProgress.objects.get_or_create(student=student, training_course=course)
    promo_banners = get_cached_promo_in_dashboard()

    # Если объект был только что создан, то устанавливаем первоначальные состояния для
    # current_block, current_point и current_step
    if created:
        current_block = course.blocks.first()
        course_progress.current_block = current_block

        current_point = current_block.points.first()
        course_progress.current_point = current_point

        current_step = current_point.steps.first()
        course_progress.current_step = current_step
        course_progress.save()

    total_steps_in_course = 0

    for block in course.blocks.all():
        for point in block.points.all():
            total_steps_in_course += point.steps.count()

    completed_steps = course_progress.completed_steps.all().count()

    if completed_steps > 0:
        completed_course_in_percent = (completed_steps * 100) / total_steps_in_course
    else:
        completed_course_in_percent = 0

    blocks = course.blocks.all()
    blocks_data = []

    for block in blocks:
        points_data = []
        completed_steps_in_points_in_block = 0
        total_steps_in_points_in_block = 0

        for point in block.points.all():
            total_steps_in_point = point.steps.count()
            total_steps_in_points_in_block += total_steps_in_point
            completed_steps_in_point = point.steps.filter(id__in=course_progress.completed_steps.values('id')).count()
            completed_steps_in_points_in_block += completed_steps_in_point
            points_data.append({
                'point': point,
                'total_steps_in_point': total_steps_in_point,
                'completed_steps_in_point': completed_steps_in_point,
                'completed_steps_in_point_in_percent':
                    (completed_steps_in_point * 100) / total_steps_in_point if total_steps_in_point > 0 else 0
            })
        blocks_data.append({
            'block': block,
            'completed_steps_in_points_in_block': completed_steps_in_points_in_block,
            'completed_steps_in_points_in_block_in_percent':
                (completed_steps_in_points_in_block * 100) / total_steps_in_points_in_block
                if total_steps_in_points_in_block > 0 else 0,
            'total_steps_in_points_in_block': total_steps_in_points_in_block,
            'points_data': points_data,
        })

    context = {
        'course_progress': course_progress,
        'completed_course_in_percent': completed_course_in_percent,
        'blocks_data': blocks_data,
        'promo_banners': promo_banners
    }
    return render(request, 'education_platform/course_progress_dashboard.html', context=context)


# def continue_lesson_view(request, point_pk):
#     # Если пользователь не авторизован, то редирект на дом. страницу
#     # TODO: написать Json ответ с рендером ошибки
#     if not request.user.is_authenticated:
#         return redirect('education_platform:home')
#
#     # Получаем объект point
#     try:
#         point = PointForTrainingBlock.objects.get(pk=point_pk)
#     except ObjectDoesNotExist:
#         return redirect(reverse('education_platform:home'))
#
#     # Получаем его TrainingCourse
#     course = TrainingCourse.objects.get(pk=point.training_course_block.training_course.pk)
#
#     # Проверка доступа к курсу у пользователя
#     student = request.user.student
#     access_to_course = AccessToCourse.objects.get(student=student, training_course=course)
#
#     if not access_to_course:
#         # Если у пользователя нет доступа к курсу, то редирект на дом. страницу
#         # TODO: написать Json ответ с рендером ошибки
#         return redirect(reverse('education_platform:home'))
#     else:
#         progress = CourseProgress.objects.get(student=student, training_course=course)
#
#         if progress.is_completed:
#             return course_completed_view(request, progress)
#
#         # Проверка, содержит ли шаг вопрос, если да, то True, если нет - False
#         has_question = True if progress.current_step.questions.count() > 0 else False
#
#         # Если содержит вопрос, то проверка, есть ли только один верный ответ, или верных ответов несколько
#         if has_question:
#             # Если больше одного правильного ответа у вопроса, то True, else False
#             has_many_correct_answers = True if progress.current_step.questions.first().answers.filter(
#                 is_true=True).count() > 1 else False
#
#         # Если нет вопроса у шага, то в переменной has_many_answers = None
#         else:
#             has_many_correct_answers = None
#
#         context = {
#             'progress': progress,
#             'training_course': course,
#             'current_point': point,
#             'next_step_ajax_url': reverse('education_platform:next_step_ajax'),
#             'has_question': has_question,
#             'has_many_correct_answers': has_many_correct_answers,
#         }
#
#         return render(request, 'education_platform/point_detail.html', context=context)


def next_step_ajax_view(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        current_step_pk = request.GET.get('current_step', None)
        if current_step_pk:
            current_step = StepForPoint.objects.get(pk=current_step_pk)
            student = request.user.student
            course = current_step.point_for_training_block.training_course_block.training_course
            current_step.mark_completed(student=student, course=course)
            return JsonResponse({
                'status': 'ok',
                "message": "Шаг обновлен"
            })
        else:
            return JsonResponse({
                'status': 'ok',
                "message": "Не обнаружен шаг"
            })


def get_step_detail_view(request, course_pk, step_pk):
    if not request.user.is_authenticated:
        return HttpResponse('Пользователь не зарегистрирован')

    student = request.user.student

    # Проверяем доступ к курсу
    if AccessToCourse.objects.filter(student=student, training_course__pk=course_pk).exists():
        # Загружаем прогресс с `prefetch_related` для завершенных шагов и шагов текущего блока
        progress = CourseProgress.objects.select_related('current_point').prefetch_related(
            'completed_steps',
        ).get(student=student, training_course__pk=course_pk)

        # Получаем course со всеми связанными таблицами из кэша
        course = get_cached_training_course(course_pk)

        # Поиск текущего шага в уже загруженной таблице из course
        step = next(
            (step for block in course.blocks.all()
             for point in block.points.all()
             for step in point.steps.all()
             if step.pk == step_pk),
            None
        )

        # Получаем комментарии к шагу из кэша:
        step_comments = get_cached_step_comments(step)


        # Обновляем прогресс одним вызовом `save` с использованием `update_fields`
        progress.current_step = step
        progress.current_point = step.point_for_training_block
        progress.current_block = step.point_for_training_block.training_course_block
        progress.save(update_fields=['current_step', 'current_point', 'last_action', 'current_block'])

        # Навигация по шагам: используем подгруженные завершенные шаги и шаги текущего блока
        step_list = [
            {
                "url": nav_step.get_absolute_url(),
                "is_completed": nav_step.is_completed(progress),
                "pk": nav_step.pk,
                "number": nav_step.number
            }
            for nav_step in progress.current_point.steps.all()
        ]


        # Данные для бокового меню "Содержание" с `prefetch_related` для блоков и пунктов
        data_for_points_list = []


        # course_blocks = progress.training_course.blocks.all().prefetch_related('points__steps')
        course_blocks = course.blocks.all()

        # Определяем переменную для вычисления общего количества шагов в курсе
        total_steps_in_course = 0

        for block in course_blocks:
            points_list = []

            for point in block.points.all():
                points_list.append({
                    "title": point.title,
                    "number": point.number,
                    "url": point.get_absolute_url(),
                    "completed": point.is_completed(progress),
                    "is_current": point == progress.current_point
                })

                total_steps_in_course += point.steps.count()

            data_for_points_list.append({
                "block_title": block.title,
                "block_number": block.number,
                "points_list": points_list
            })

        # Определяем прогресс в курсе
        completed_steps = progress.completed_steps.count()
        completed_course_in_percent = (completed_steps * 100) / total_steps_in_course if completed_steps else 0


        # Формируем контекст
        context = {
            "step": step,
            "step_comments": step_comments,
            "progress": progress,
            "url_for_make_step_is_completed": reverse("education_platform:ajax_make_step_is_completed"),
            "total_steps_in_course": total_steps_in_course,
            "step_is_completed": step.is_completed(progress),
            "course": course,
            "data_for_points_list": data_for_points_list,
            "completed_course_in_percent": completed_course_in_percent,
            "step_list": step_list,
            "next_step_pk": step.get_next_step_pk(progress),
            "previous_step_pk": step.get_previous_step_pk(progress)
        }

        # Проверка завершения курса
        progress.check_and_make_course_completed(total_steps_in_course)


        # Вопросы
        if step.has_questions():
            question = step.questions.first()
            if not progress.is_completed:
                context["question_has_many_correct_answers"] = question.answers.filter(is_true=True).count() > 1
                context["ajax_check_answer_for_question_url"] = reverse("education_platform:ajax_check_answer_for_question")
                context["correct_answers"] = question.answers.filter(is_true=True)
            else:
                context["correct_answers"] = question.answers.filter(is_true=True)


        return render(request, "education_platform/step_detail.html", context)
    else:
        return HttpResponse("У студента нет доступа к курсу")


def ajax_check_answer_for_question(request):
    """
    Проверка ответов на вопрос через ajax
    """
    if request.method == "POST":
        # Определяем объект вопроса и список правильных ответов
        question_pk = request.POST.get("question_pk")
        progress_pk = request.POST.get("progress_pk")
        question = QuestionForStep.objects.get(pk=question_pk)
        correct_answers_pks = question.answers.values_list("pk", flat=True).filter(is_true=True)

        # Если правильный ответ один
        if not correct_answers_pks.count() > 1:
            answer_pk_from_form = request.POST.get("answer")
            correct_answer = correct_answers_pks[0]

            # Если полученный ответ правильный
            if correct_answer == int(answer_pk_from_form):
                progress = CourseProgress.objects.get(pk=progress_pk)
                progress.completed_steps.add(progress.current_step)
                progress.save()

                # Проверка, не завершился ли курс на этом ответе (шаге)?
                course = progress.training_course

                total_steps_in_course = request.POST.get("total_steps_in_course")
                progress.check_and_make_course_completed(int(total_steps_in_course))

                # Если курс не завершен, то стандартное поведение
                if not progress.is_completed:
                    return JsonResponse({
                        "status": "correct_answer",
                    })

                # Если курс завершен, то возвращаем ответ скрипту, который отрендерит
                # Окно с информацией о завершении курса, а так же прибавим в
                # course.completed_counter += 1
                else:
                    course.completed_counter += 1
                    course.save()

                    context = {
                        "progress_pk": progress.pk
                    }
                    modal_content = render_to_string(
                        'education_platform/incl/modal_for_course_completed.html',
                        request=request,
                        context=context
                    )

                    return JsonResponse({
                        "status": "course_is_competed",
                        "modal_for_course_completed": modal_content
                    })

            # Если полученный ответ неправильный
            else:
                return JsonResponse({
                    "status": "incorrect_answer",
                    "message": "Получен неправильный ответ"
                })

        # Если правильный ответ не один
        else:
            # Извлекаем ответы из формы и создаем список pk полученных ответов
            answers_pks_from_form = request.POST.getlist("answer")
            int_answers_pks_from_form = [int(pk) for pk in answers_pks_from_form]

            # Если set списка полученных ответов и set списка правильных ответов совпадают
            if set(int_answers_pks_from_form) == set(correct_answers_pks):

                progress = CourseProgress.objects.select_related('training_course').get(pk=progress_pk)
                progress.completed_steps.add(progress.current_step)
                progress.save()

                # Проверка, не завершился ли курс на этом шаге?
                total_steps_in_course = request.POST.get("total_steps_in_course")
                progress.check_and_make_course_completed(int(total_steps_in_course))

                # Если курс не завершен, то стандартное поведение
                if not progress.is_completed:
                    return JsonResponse({
                        "status": "correct_answers",
                        "message": "Получены верные ответы"
                    })

                # Если курс завершен, то возвращаем ответ скрипту, который отрендерит
                # Окно с информацией о завершении курса, а так же прибавим в
                # course.completed_counter += 1

                else:
                    course = progress.training_course
                    course.completed_counter += 1
                    course.save()

                    context = {
                        "progress_pk": progress.pk
                    }
                    modal_content = render_to_string(
                        'education_platform/incl/modal_for_course_completed.html',
                        request=request,
                        context=context
                    )

                    return JsonResponse({
                        "status": "course_is_competed",
                        "modal_for_course_completed": modal_content
                    })

            # Если полученные ответы неправильные
            else:
                return JsonResponse({
                    "status": "incorrect_answers",
                    "message": "Получены неверные ответы"
                })

    # Если пришел неверный запрос
    return JsonResponse({
        "status": "success",
        "message": "ERROR"
    })


def ajax_make_step_is_completed(request):
    if request.method == "POST":
        progress_pk = request.POST.get("progress_pk")
        total_steps_in_course = request.POST.get("total_steps_in_course")
        student = request.user.student
        progress = CourseProgress.objects.get(pk=progress_pk)
        course = progress.training_course

        if progress.student == student:
            progress.completed_steps.add(progress.current_step)
            progress.save()

            # Проверка, не является ли курс уже завершенным?
            if not progress.is_completed:
                # Проверка, не пора ли завершить курс на этом шаге?
                progress.check_and_make_course_completed(int(total_steps_in_course))

                # Если курс не завершился, то далее обычное поведение
                if not progress.is_completed:
                    return JsonResponse({
                        "status": "step_is_completed"
                    })
                # Если курс завершился на этом шаге, то отправляем шаблон модального окна
                # которое будет вставлено js скриптом в подготовленный блок и вызвано после этого
                # так же увеличиваем course.completed_counter += 1
                else:
                    course.completed_counter += 1
                    course.save()

                    context = {
                        "progress_pk": progress.pk
                    }
                    modal_content = render_to_string(
                        'education_platform/incl/modal_for_course_completed.html',
                        request=request,
                        context=context
                    )

                    return JsonResponse({
                        "status": "course_is_competed",
                        "modal_for_course_completed": modal_content
                    })

            # Если курс уже был завершен, до этого шага, то обычное поведение шага
            else:
                return JsonResponse({
                    "status": "step_is_completed"
                })
