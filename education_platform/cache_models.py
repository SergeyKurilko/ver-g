from django.core.cache import cache
from education_platform.models import TrainingCourse, PromoInDashboard


def get_cached_training_course_with_slug(course_slug):
    """
    Пытается извлечь из кэша объект TrainingCourse, используя slug.
    Если в кэше (redis) его нет, то извлечь из БД и сохранить в кэш.
    """
    # Устанавливаем ключ кэша на основе slug объекта TrainingCourse
    cache_key = f"training_course_{course_slug}"

    # Получаем объект из кэша, если он там есть
    training_course = cache.get(cache_key)

    if training_course is None:
        # Если в кэше нет объекта, то делаем запрос в БД
        training_course =  (TrainingCourse.objects.
                            prefetch_related('blocks__points__steps__questions__answers').
                            get(slug=course_slug))

        # Сохраняем объект в кэше на 1 неделю (устанавливаем timeout в секундах)
        cache.set(cache_key, training_course, timeout=60 * 60 * 24 * 7)  # 1 неделя

    return training_course



def get_cached_training_course(course_pk):
    """
    Пытается извлечь из кэша объект TrainingCourse.
    Если в кэше (redis) его нет, то извлечь из БД и сохранить в кэш.
    """
    # Устанавливаем ключ кэша на основе pk объекта TrainingCourse
    cache_key = f"training_course_{course_pk}"

    # Получаем объект из кэша, если он там есть
    training_course = cache.get(cache_key)

    if training_course is None:
        # Если в кэше нет объекта, то делаем запрос в БД
        training_course =  (TrainingCourse.objects.
                            prefetch_related('blocks__points__steps__questions__answers').
                            get(pk=course_pk))

        # Сохраняем объект в кэше на 1 неделю (устанавливаем timeout в секундах)
        cache.set(cache_key, training_course, timeout=60 * 60 * 24 * 7)  # 1 неделя

    return training_course


def get_cached_step_comments(step):
    """
    Извлекает комментарии к шагу 'step', если они там есть,
    если нет, то сохраняет в кэш
    """
    cache_key = f"step_comments_{step.pk}"
    comments = cache.get(cache_key)

    if comments is None:
        # Если в кэше нет списка комментариев, то запрос в бд
        comments = (step.comments
                    .select_related('author__student', 'parent')
                    .prefetch_related('answers')
                    .all())

        cache.set(cache_key, comments, timeout=60)

    return comments


def get_cached_promo_in_dashboard():
    """
    Сохраняет в кэш queryset PromoInDashboard.objects.filter(published=True)
    Если в кеше есть этот query, то возвращает из кэша, если нет то сохраняет.
    """
    cache_key = "promo_in_dashboard"
    promo_in_dashboard = cache.get(cache_key)

    if promo_in_dashboard is None:
        promo_in_dashboard = PromoInDashboard.objects.filter(published=True)
        cache.set(cache_key, promo_in_dashboard, timeout=1) # кэш на три часа

    return promo_in_dashboard




