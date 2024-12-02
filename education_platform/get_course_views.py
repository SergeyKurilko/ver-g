from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.formats import date_format

from education_platform.cache_models import get_cached_training_course
from education_platform.models import TrainingCourse, AccessToCourse, CourseProgress, CoursePack, Transaction, PromoCode


def get_course_ajax_view(request, course_pk):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if not request.user.is_authenticated:
            return JsonResponse({
                'success': f'not_authenticated'
            })
        if request.user.is_authenticated:
            course = get_cached_training_course(course_pk)
            if course.is_free:
                student = User.objects.get(pk=request.user.pk).student
                if not AccessToCourse.objects.filter(student=student, training_course=course).exists():
                    new_access = AccessToCourse.objects.create(student=student, training_course=course)
                    new_progress = CourseProgress.objects.create(student=student,
                                                  training_course=course,
                                                  current_step=course.blocks.first().points.first().steps.first()
                                                  )
                    return JsonResponse({
                        'success': f'access_to_course_is_created',
                    })
                else:
                    return JsonResponse({
                        'success': 'access_to_course_already_exist'
                    })
            if not course.is_free:
                return JsonResponse({
                    'success': 'course_is_paid',
                    'url_for_get_paid_course': reverse(
                        'education_platform:get_paid_course', args=[course_pk]
                    )
                })
    else:
        return redirect('education_platform:home')


def get_paid_course_ajax_view(request, course_pk):
    if (request.method == 'GET' and
            request.headers.get('x-requested-with') == 'XMLHttpRequest'):
        course = get_cached_training_course(course_pk)
        context = {
            "product_type": "course",
            "product_id": course_pk,
            "amount": course.price,
            "course_title": course.title,
            "user_email": request.user.email,
        }
        if course.discount > 0:
            context['discount_price'] = course.price - ((course.price * course.discount) / 100)

        modal_content = render_to_string(
            template_name='education_platform/incl/modal_for_get_paid_course.html',
            context=context,
            request=request)

        return JsonResponse({
            "success": "payment_course_form",
            "payment_course_form_modal": modal_content
        })


def payment_successful_view(request, product_type, product_id):
    # Функция вызывается в момент возврата пользователя со страницы оплаты yookassa
    # В возвратном url можно указать параметр. Например (get_course_pk) и уже в
    # этой вьюхе найти транзакцию, курс и т.д.
    context = {}

    context["product_type"] = product_type

    try:
        transaction = Transaction.objects.get(
            product_type=product_type,
            product_id=product_id,
            user=request.user
        )
    except Transaction.DoesNotExist:
        transaction = None

    if transaction:
        # Если транзакция есть и платеж подтвержден
        if transaction.status == "succeeded":
            context["payment_confirmed"] = True

        elif transaction.status != "succeeded":
            context["payment_confirmed"] = False
            context["check_payment_url"] = reverse(
                "education_platform:check_payment_status",
                args=[transaction.payment_id]
            )


        # Независимо от того, подтвержден ли платеж,
        # передаем в шаблон контекст о курсе или пакете курсов
        if product_type == "course":
            course = get_cached_training_course(course_pk=product_id)
            context["course"] = course

        elif product_type == "course_pack":
            course_pack = get_object_or_404(
                CoursePack, id=product_id
            )
            context["course_pack"] = course_pack

        return render(request,
                      'education_platform/course_payment_successful_page.html',
                      context)

    else:
        # Транзакции нет.
        # Запрос ошибочный. Делаем редирект
        return redirect("education_platform:home")


def use_promo_code_view(request):
    if request.method == 'POST':
        promo_code = request.POST.get('promoInput', None)
        course_pk = request.POST.get('course_pk', None)
        try:
            promo_obj = PromoCode.objects.select_related('course').get(code=promo_code)
        except ObjectDoesNotExist:
            return JsonResponse({
                "status": "error",
                "error_message": "Промокод недействителен"
            })

        # Проверка, подходит ли этот промокод к курсу, который нужно получить/купить
        if promo_obj.course.pk != int(course_pk):
            return JsonResponse({
                "status": "error",
                "error_message": "Промокод недействителен"
            })

        # Проверка срока действия validity_period промокода. Если срок закончился, то удаление
        # объекта промокода
        validity_period = None

        if promo_obj.validity_period:
            if not promo_obj.validity_period > timezone.now().date():
                # Если при попытке применения, срок истек, то сообщаем об этом и удаляем его
                promo_obj.delete()
                return JsonResponse({
                    "status": "error",
                    "error_message": "Срок промокода истек"
                })
            else:
                validity_period = 'Действует до ' + date_format(promo_obj.validity_period, 'd E Y') + 'г.'
        else:
            validity_period = 'Бессрочный.'

        course_price = promo_obj.course.price
        new_price = course_price - ((course_price * promo_obj.sale_value) / 100)

        json_response = {
            'status': 'ok',
            'new_price': new_price,
            'promo_code_pk': promo_obj.pk,
            'old_price': course_price,
            'validity_period': validity_period
        }

        # Проверка, после применения промокода, получилась ли стоимость > 0
        if new_price > 0:
            json_response['type_of_access'] = 'discounted'
        else:
            json_response['type_of_access'] = 'is_free'
            json_response['url_for_get_course_free_with_promo'] \
                = reverse('education_platform:ajax_get_course_free_with_promo')


        return JsonResponse(json_response)
    else:
        return redirect('education_platform:home')


def ajax_get_course_free_with_promo(request):
    """
    Приходит запрос, если при применении promo code стоимость
    равна 0
    """
    if (request.method == 'POST' and
            request.headers.get('x-requested-with') == 'XMLHttpRequest'):

        promo_code_pk = request.POST.get('promo_code')
        course_pk = request.POST.get('product_id')

        promo_code = PromoCode.objects.get(pk=promo_code_pk)
        course = get_cached_training_course(course_pk)

        student = User.objects.get(pk=request.user.pk).student
        if not AccessToCourse.objects.filter(student=student, training_course=course).exists():
            new_access = AccessToCourse.objects.create(student=student, training_course=course)
            new_progress = CourseProgress.objects.create(student=student,
                                                         training_course=course,
                                                         current_step=course.blocks.first().points.first().steps.first()
                                                         )

            promo_code.delete()

            context = {
                "course_title": course.title,
                "course_url": course.get_absolute_url(),
                "course_image_url": course.image.url
            }

            html_for_render = render_to_string(
                template_name='education_platform/incl/free_course_with_promo.html',
                context=context,
                request=request)

            # При успешном получении доступа к курсу, возвращаем status = ok
            # и контент для рендера
            return JsonResponse({
                "status": "ok",
                "html_for_render": html_for_render
            })
