import json
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from yookassa import Configuration, Payment
from yookassa.domain.common import SecurityHelper

from education_platform.cache_models import get_cached_training_course
from education_platform.models import Transaction, TrainingCourse, AccessToCourse, CourseProgress, CoursePack, \
    AccessToCoursePack, PromoCode
import uuid

Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY

def get_user_ip(request):
    """
    Функция для получения ip
    """
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
    if ip_address:
        ip_address = ip_address.split(',')[0]
    else:
        ip_address = request.META.get('REMOTE_ADDR')
    return ip_address


@csrf_exempt
def create_transaction_view(request):
    """
    Создает транзакцию и инициирует платеж через ЮKassa.
    Данные получаются из формы на странице оплаты.

    Параметр запроса:
    - product_type: Тип продукта (курс или пакет курсов).
    - product_id: Идентификатор продукта.
    - amount - сумма платежа.

    Возвращает:
    - JSON с URL для редиректа на страницу оплаты ЮKassa.
    """

    if request.method == 'POST':
        product_type = request.POST.get('product_type')
        product_id = request.POST.get('product_id')
        amount = request.POST.get('amount')
        promo_code_pk = request.POST.get('promo_code')

        if promo_code_pk:
            promo_code = PromoCode.objects.get(pk=promo_code_pk)
        else:
            promo_code = None


        # TODO: Перед созданием транзакции проверить, есть ли promo_code_pk
        # Если есть, то сохранить в транзакции ссылку на promocode
        # Далее, при получении callback от юкасса, удалить промокод
        promo_code_pk = request.POST.get('promo_code', None)
        user = request.user


        amount = amount.replace(',', '.')
        idempotence_key = str(uuid.uuid4())

        if product_type == 'course':
            course_title = request.POST.get('course_title')
            product_description = "курсу"

            return_url = (
                reverse("education_platform:course_payment_successful",
                        args=[product_type, product_id]))

            payment = Payment.create({
                "amount": {
                    "value": amount,
                    "currency": "RUB"
                },
                "confirmation": {
                    "type": "redirect",
                    # TODO: поменять на корректный
                    "return_url":
                        f"{settings.YOOKASSA_RETURN_URL}{product_type}/{product_id}/"
                },
                "customer": {
                    # TODO поменять на корректный email
                    "email": "kurservlad@yandex.ru",
                    "full_name": f"{user.first_name} {user.last_name}"
                },
                "items": {
                    "description": course_title,
                    "amount": {
                        "value": amount,
                        "currency": "RUB"
                    }
                },
                "capture": True,
                "description": f'Оплата доступа к {product_description}'
                               f' "{course_title}"'
                               f' для {user.first_name} {user.last_name}'
            }, idempotency_key=idempotence_key)

            if payment.status == "pending":
                transaction, created = Transaction.objects.get_or_create(
                    user=user,
                    amount=amount,
                    # payment_id=payment.id,
                    # status=payment.status,
                    product_type=product_type,
                    product_id=product_id,
                    promo_code=promo_code
                )

                # Если транзакция новая, то добавляем актуальные данные из payment
                if created:
                    transaction.status = payment.status
                    transaction.payment_id = payment.id
                    transaction.save()

                # Если транзакция уже создавалась, то актуализируем данные из payment
                else:
                    transaction.status = payment.status
                    transaction.payment_id = payment.id
                    transaction.save()

                return redirect(payment.confirmation.confirmation_url)
            else:
                return JsonResponse({
                    "error": "Ошибка при создании платежа"}
                    , status=500)

        elif product_type == 'course_pack':
            course_pack_title = request.POST.get('course_pack_title')
            product_description = "пакету курсов"

            return_url = (
                reverse("education_platform:course_payment_successful",
                        args=[product_type, product_id]))

            payment = Payment.create({
                "amount": {
                    "value": amount,
                    "currency": "RUB"
                },
                "confirmation": {
                    "type": "redirect",
                    # TODO: поменять на корректный!!!
                    "return_url":
                        f"{settings.YOOKASSA_RETURN_URL}{product_type}/{product_id}/"
                },
                "customer": {
                    # TODO поменять на корректный email
                    "email": "kurservlad@yandex.ru",
                    "full_name": f"{user.first_name} {user.last_name}"
                },
                "items": {
                    "description": course_pack_title,
                    "amount": {
                        "value": amount,
                        "currency": "RUB"
                    }
                },
                "capture": True,
                "description": f'Оплата доступа к {product_description}'
                               f' "{course_pack_title}"'
                               f' для {user.first_name} {user.last_name}'
            }, idempotency_key=idempotence_key)

            if payment.status == "pending":
                transaction, created = Transaction.objects.get_or_create(
                    user=user,
                    amount=amount,
                    # payment_id=payment.id,
                    # status=payment.status,
                    product_type=product_type,
                    product_id=product_id
                )

                # Если транзакция новая, то добавляем актуальные данные из payment
                if created:
                    transaction.status = payment.status
                    transaction.payment_id = payment.id
                    transaction.save()

                # Если транзакция уже создавалась, то актуализируем данные из payment
                else:
                    transaction.status = payment.status
                    transaction.payment_id = payment.id
                    transaction.save()

                return redirect(payment.confirmation.confirmation_url)
            else:
                return JsonResponse({
                    "error": "Ошибка при создании платежа"}
                    , status=500)
    return JsonResponse({"error": "Неверный метод запроса"}, status=400)


@csrf_exempt
def transaction_callback(request):
    """
    Обрабатывает уведомление от ЮKassa о статусе платежа.

    Параметры запроса:
    - event: Тип события (например 'payment.succeeded')
    - payment_id: Идентификатор платежа от ЮKassa.

    Возвращает:
    - JSON с сообщением об успешной обработке платежа.
    """
    if request.method == "POST":
        # Если хотите убедиться, что запрос пришел от ЮКасса, добавьте проверку:
        ip = get_user_ip(request)  # Получите IP запроса
        if not SecurityHelper().is_ip_trusted(ip):
            return HttpResponse(status=400)
        data = json.loads(request.body)
        event = data.get('event')
        payment_id = data.get('object', {}).get('id')

        if event == "payment.succeeded":
            try:
                transaction = Transaction.objects.get(payment_id=payment_id)
                transaction.status = "succeeded"
                transaction.save()

                student = transaction.user.student

                if transaction.product_type == 'course':
                    course = get_cached_training_course(transaction.product_id)

                    # Если у транзакции был промокод, то удаляем его (объект промокод)
                    if transaction.promo_code:
                        transaction.promo_code.delete()

                    AccessToCourse.objects.create(student=student, training_course=course)
                    CourseProgress.objects.create(student=student,
                                                  training_course=course,
                                                  current_step=course.blocks.first().points.first().steps.first()
                                                  )

                elif transaction.product_type == 'course_pack':
                    course_pack = CoursePack.objects.get(id=transaction.product_id)
                    access_to_course_pack = AccessToCoursePack.objects.create(
                        student=student,
                        course_pack=course_pack
                    )
                    for course in course_pack.courses.all():
                        if not AccessToCourse.objects.filter(student=student, training_course=course).exists():
                            AccessToCourse.objects.create(student=student, training_course=course)
                            CourseProgress.objects.create(student=student,
                                                          training_course=course,
                                                          current_step=course.blocks.first().points.first().steps.first()
                                                          )
            except Transaction.DoesNotExist:
                pass

            return HttpResponse(status=200)  # Сообщаем кассе, что все хорошо

    return JsonResponse({
        "error": "Неверный метод запроса"
    }, status=400)


def check_payment_status(request, payment_id):
    """
    Функция для проверки статуса платежа.
    Вызывается через ajax из скрипта
    """
    payment = Payment.find_one(payment_id)

    if payment.status == 'succeeded':
        return JsonResponse({
            "status": "succeeded"
        })
    else:
        return JsonResponse({
            "status": "not_succeeded"
        })

