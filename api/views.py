from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Count, Q
from django.core.cache import cache
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response

from comments.models import CommentForArticle
from education_platform.models import TrainingCourse, PromoCode
from api.serializers import TrainingCourseSerializer, PromoCodeSerializer
from api.authentication import VergAuthentication





class TrainingCourseViewSet(viewsets.ModelViewSet):
    """
    Принимает только GET, проверяет условия VergAuthentication (ключ api)
    Возвращает список объектов TrainingCourse.objects.filter(is_free=False, discount=0)
    """
    queryset = TrainingCourse.objects.filter(is_free=False, discount=0)
    serializer_class = TrainingCourseSerializer
    authentication_classes = [VergAuthentication]
    http_method_names = ['get']


class CreatePromoFromTelegramBot(APIView):
    """
    Принимает только POST, проверяет условия VergAuthentication (ключ api)
    Возвращает список объектов созданный объект и статус 201 (CREATED)
    """
    http_method_names = ['post']
    authentication_classes = [VergAuthentication]

    def post(self, request, format=None):
        print('Дошли до пост')
        course_pk = request.data.get('course_pk')
        sale_value = request.data.get('sale_value')
        validity_period = request.data.get('validity_period')

        try:
            course = TrainingCourse.objects.get(pk=course_pk)
        except TrainingCourse.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
        promo_code = PromoCode(
            sale_value=sale_value,
            course=course
        )
        if validity_period is not None:
            promo_code.validity_period = validity_period

        promo_code.code = PromoCode.generate_code(promo_code)
        promo_code.save(from_api=True)
        serializer = PromoCodeSerializer(promo_code)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class CheckPromoCodeApiView(APIView):
    """
    Принимает только POST, проверяет условия VergAuthentication (ключ api).
    Так же проверяет формат данных в request.data.get('code') - длина строки
    должна быть 8 символов.
    Возвращает сериализованный объект PromoCode и статус 200, если объект найден,
    в противном случае возвращает 404.
    """
    http_method_names = ['post']
    authentication_classes = [VergAuthentication]

    def post(self, request):
        code = request.data.get('code')

        if not code or len(str(code)) != 8:
            return Response("Некорректный запрос",
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            promo_code = PromoCode.objects.get(code=code)
        except PromoCode.DoesNotExist:
            return Response({"error": "Промокод не найден"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PromoCodeSerializer(promo_code)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class EducationPlatformReport(APIView):
    authentication_classes = [VergAuthentication]
    http_method_names = ['get']

    def get(self, request):

        # Время 12 часов назад
        twelve_hours_ago = timezone.now() - timezone.timedelta(hours=12)

        # Проверяем кэш
        users_stats = cache.get("user_stats_cache")

        # Если кэша нет, то извлекаем данные из БД и сохраняем в кэш на час
        if users_stats is None:
            # total_users_number - общее количество пользователей
            # last_12_hours_registrations - количество зарегистрировавшихся за последние 12 часов
            users_stats = User.objects.filter(is_superuser=False).aggregate(
                total_users_number=Count("id"),
                last_12_hours_registrations=Count("id", filter=Q(date_joined__gt=twelve_hours_ago))
            )

            cache.set("user_stats_cache", users_stats, timeout=60 * 60)

        courses_stats = cache.get("courses_stats_cache")
        if courses_stats is None:
            # total_courses_number - всего курсов
            # total_free_courses_number - всего бесплатных курсов
            # total_paid_courses_number - всего платных курсов
            # total_published_courses_number - всего опубликованных курсов
            courses_stats = TrainingCourse.objects.aggregate(
                total_courses_number=Count("id"),
                total_free_courses_number=Count("id", filter=Q(is_free=True)),
                total_paid_courses_number=Count("id", filter=Q(is_free=False)),
                total_published_courses_number=Count("id", filter=Q(published=True))
            )
            cache.set("courses_stats_cache", courses_stats, 60 * 60)

        report_data = {
            "total_users_number": users_stats["total_users_number"],
            "last_12_hours_registrations": users_stats["last_12_hours_registrations"],
            "total_courses_number": courses_stats["total_courses_number"],
            "total_free_courses_number": courses_stats["total_free_courses_number"],
            "total_paid_courses_number": courses_stats["total_paid_courses_number"],
            "total_published_courses_number": courses_stats["total_published_courses_number"],
        }

        return Response(report_data, status=status.HTTP_200_OK)


class CommentForArticleDelete(APIView):
    http_method_names = ['delete']
    authentication_classes = [VergAuthentication]

    def delete(self, request, *args, **kwargs):
        comment_id = request.query_params.get("comment_id")

        if not comment_id:
            return Response("Некорректный запрос",
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                CommentForArticle.objects.get(pk=comment_id).delete()
            except CommentForArticle.DoesNotExist:
                return Response(data={"error": "Comment not found"},
                                status=status.HTTP_404_NOT_FOUND)

            return Response(data={"success": "Комментарий успешно удален"},
                            status=status.HTTP_200_OK)

