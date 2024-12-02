from os import access

from django.db.models import signals
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from education_platform.cache_models import get_cached_training_course, get_cached_training_course_with_slug
from education_platform.models import TrainingCourse, TrainingCourseBlock, PointForTrainingBlock, StepForPoint, \
    QuestionForStep, AnswerForQuestion, AccessToCourse
from education_platform.tasks import send_telegram_create_access_to_course


# Сигналы для обновления кэша объекта TrainingCourse при изменении связанных с ним объектов или его самого


@receiver(post_save, sender=TrainingCourse)
def update_training_course_cache(sender, instance, **kwargs):
    """
        Обновляет кэш для объекта TrainingCourse при его сохранении или обновлении или
    """
    cache_key = f"training_course_{instance.pk}"
    cache.delete(cache_key)  # Удаляем старый кэш
    get_cached_training_course(instance.pk)  # Перезаписываем кэш get_cached_training_course

    cache_key_with_slug = f"training_course_{instance.slug}"
    cache.delete(cache_key_with_slug)  # Удаляем кэш для get_cached_training_course_with_slug
    get_cached_training_course_with_slug(instance.slug) # Перезаписываем кэш для get_cached_training_course_with_slug


@receiver(post_delete, sender=TrainingCourse)
def clear_training_course_cache_on_delete(sender, instance, **kwargs):
    """
    Очищает кэш для объекта TrainingCourse при его удалении.
    """
    cache_key = f"training_course_{instance.pk}"
    cache.delete(cache_key)  # Удаляем кэш

    cache_key_with_slug = f"training_course_{instance.slug}"
    cache.delete(cache_key_with_slug) # Удаляем кэш для get_cached_training_course_with_slug


@receiver(post_save, sender=TrainingCourseBlock)
@receiver(post_delete, sender=TrainingCourseBlock)
def update_training_course_cache_on_block_change(sender, instance, **kwargs):
    """
        Обновляет кэш для объекта TrainingCourse при сохранении, обновлении или удалении
        объектов TrainingCourseBlock, связанных с ним.
    """
    training_course = instance.training_course

    cache_key = f"training_course_{training_course.pk}"
    cache.delete(cache_key)  # Удаляем старый кэш
    get_cached_training_course(training_course.pk)  # Перезаписываем кэш

    cache_key_with_slug = f"training_course_{training_course.slug}"
    cache.delete(cache_key_with_slug)  # Удаляем кэш для get_cached_training_course_with_slug
    get_cached_training_course_with_slug(training_course.slug)  # Перезаписываем кэш для get_cached_training_course_with_slug


@receiver(post_save, sender=PointForTrainingBlock)
@receiver(post_delete, sender=PointForTrainingBlock)
def update_training_course_cache_on_point_change(sender, instance, **kwargs):
    """
        Обновляет кэш для объекта TrainingCourse при сохранении, обновлении или удалении
        объектов PointForTrainingBlock, связанных с ним.
    """

    training_course = instance.training_course_block.training_course

    cache_key = f"training_course_{training_course.pk}"
    cache.delete(cache_key)  # Удаляем старый кэш
    get_cached_training_course(training_course.pk)  # Перезаписываем кэш

    cache_key_with_slug = f"training_course_{training_course.slug}"
    cache.delete(cache_key_with_slug)  # Удаляем кэш для get_cached_training_course_with_slug
    get_cached_training_course_with_slug(
        training_course.slug)  # Перезаписываем кэш для get_cached_training_course_with_slug


@receiver(post_save, sender=StepForPoint)
@receiver(post_delete, sender=StepForPoint)
def update_training_course_cache_on_step_change(sender, instance, **kwargs):
    """
        Обновляет кэш для объекта TrainingCourse при сохранении, обновлении или удалении
        объектов StepForPoint, связанных с ним.
    """
    training_course = instance.point_for_training_block.training_course_block.training_course

    cache_key = f"training_course_{training_course.pk}"
    cache.delete(cache_key)  # Удаляем старый кэш
    get_cached_training_course(training_course.pk)  # Перезаписываем кэш

    cache_key_with_slug = f"training_course_{training_course.slug}"
    cache.delete(cache_key_with_slug)  # Удаляем кэш для get_cached_training_course_with_slug
    get_cached_training_course_with_slug(
        training_course.slug)  # Перезаписываем кэш для get_cached_training_course_with_slug


@receiver(post_save, sender=QuestionForStep)
@receiver(post_delete, sender=QuestionForStep)
def update_training_course_cache_on_question_change(sender, instance, **kwargs):
    """
        Обновляет кэш для объекта TrainingCourse при сохранении, обновлении или удалении
        объектов QuestionForStep, связанных с ним.
    """
    training_course = instance.step.point_for_training_block.training_course_block.training_course

    cache_key = f"training_course_{training_course.pk}"
    cache.delete(cache_key)  # Удаляем старый кэш
    get_cached_training_course(training_course.pk)  # Перезаписываем кэш

    cache_key_with_slug = f"training_course_{training_course.slug}"
    cache.delete(cache_key_with_slug)  # Удаляем кэш для get_cached_training_course_with_slug
    get_cached_training_course_with_slug(
        training_course.slug)  # Перезаписываем кэш для get_cached_training_course_with_slug


@receiver(post_save, sender=AnswerForQuestion)
@receiver(post_delete, sender=AnswerForQuestion)
def update_training_course_cache_on_answer_change(sender, instance, **kwargs):
    """
        Обновляет кэш для объекта TrainingCourse при сохранении, обновлении или удалении
        объектов AnswerForQuestion, связанных с ним.
    """
    training_course = instance.question.step.point_for_training_block.training_course_block.training_course

    cache_key = f"training_course_{training_course.pk}"
    cache.delete(cache_key)  # Удаляем старый кэш
    get_cached_training_course(training_course.pk)  # Перезаписываем кэш

    cache_key_with_slug = f"training_course_{training_course.slug}"
    cache.delete(cache_key_with_slug)  # Удаляем кэш для get_cached_training_course_with_slug
    get_cached_training_course_with_slug(
        training_course.slug)  # Перезаписываем кэш для get_cached_training_course_with_slug


@receiver(post_save, sender=AccessToCourse)
def send_telegram_message_on_create_access(sender, instance, **kwargs):
    course_access = {
        "user_email": instance.student.user.email,
        "training_course": instance.training_course.title,
    }
    send_telegram_create_access_to_course.delay(course_access)



