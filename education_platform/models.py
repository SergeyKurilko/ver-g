import secrets
import string
from datetime import datetime

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Count, Sum, DateTimeField
from django.utils import timezone
from django.utils.html import format_html
from pycparser.ply.yacc import default_lr
from pytils.translit import slugify

from education_platform.tasks import send_telegram_promo


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(verbose_name='Обложка', upload_to=f'education_platform/student/avatars/',
                               blank=True,
                               null=True)
    edit_limit = models.PositiveIntegerField(
        verbose_name='Количество редактирований',
        default=2
    )

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}. ({self.user.username}). e-mail: {self.user.email}'

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'


class TrainingCourseCategory(models.Model):
    title = models.CharField(max_length=255, verbose_name='Категория курсов')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория курсов обучения'
        verbose_name_plural = 'Категории курсов обучения'


class TrainingCourseSubCategory(models.Model):
    title = models.CharField(max_length=255, verbose_name='Подкатегория курсов')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Подкатегория курсов обучения'
        verbose_name_plural = 'Подкатегории курсов обучения'


class Tag(models.Model):
    title = models.CharField(max_length=150, verbose_name='Тег')

    def __str__(self):
        return self.title


class TrainingCourse(models.Model):
    DIFFICULTY_CHOICES = [
        ('1', 'Начальный уровень'),
        ('2', 'Средний уровень'),
        ('3', 'Высокий уровень'),
    ]

    title = models.CharField(max_length=255, unique=True, verbose_name='Название курса')
    meta_description = models.CharField(max_length=255, verbose_name="Description meta tag")
    slug = models.SlugField(max_length=255)
    priority = models.PositiveIntegerField(verbose_name='Приоритет очереди', default=1)
    description = models.TextField(verbose_name='Краткое описание курса обучения')
    full_description = models.TextField(verbose_name='Полное описание курса обучения')
    who_is_this_course_for = models.TextField(verbose_name='Для кого этот курс')
    author = models.CharField(max_length=255, verbose_name='Автор курса')
    author_title = models.TextField(max_length=155, default="Преподаватель", verbose_name="Должность")
    signature = models.FileField(upload_to='media/education_platform/images/signatures/',
                                 verbose_name="Подпись автора")
    about_author = models.TextField(verbose_name='Об авторе курса')
    category = models.ForeignKey(to=TrainingCourseCategory,
                                 on_delete=models.CASCADE,
                                 related_name='courses',
                                 verbose_name='Категория',
                                 blank=True,
                                 null=True)
    sub_category = models.ForeignKey(to=TrainingCourseSubCategory,
                                     on_delete=models.CASCADE,
                                     related_name='courses',
                                     verbose_name='Подкатегория',
                                     blank=True,
                                     null=True)
    tags = models.ManyToManyField(to=Tag, related_name='Теги')
    image = models.ImageField(verbose_name='Обложка', upload_to='media/education_platform/images/')
    students = models.ManyToManyField(to=Student, related_name='courses', through='AccessToCourse', blank=True,
                                      null=True)
    is_free = models.BooleanField(verbose_name='Бесплатный', default=False)
    price = models.DecimalField(max_digits=8,
                                decimal_places=2,
                                verbose_name='Стоимость',
                                blank=True,
                                null=True,
                                default=0)
    discount = models.DecimalField(max_digits=8,
                                   decimal_places=2,
                                   verbose_name='Скидка в процентах',
                                   blank=True,
                                   null=True,
                                   default=0)
    time_to_study = models.PositiveIntegerField(verbose_name='Время для изучения', default=0)
    completed_counter = models.PositiveIntegerField(verbose_name='Прошли обучение', default=0)
    difficulty = models.CharField(max_length=1, choices=DIFFICULTY_CHOICES,
                                  default="2", verbose_name="Уровень сложности")
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    published = models.BooleanField(verbose_name='Опубликовать', default=False)

    def image_tag(self):
        """
        Возвращает рендер картинки, используется в админке
        """
        if self.image:
            return format_html('<img src="{}" style="max-width:80px; max-height:80px;" />',
                               self.image.url)
        else:
            return "No Image"

    image_tag.short_description = 'Image'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.pk}. Курс: {self.title}'

    def get_absolute_url(self):
        return reverse('education_platform:course_detail', args=[self.slug])

    def get_blocks_quantity(self):
        block_counter = self.blocks.all().count()

        def get_blocks_declension(number):
            if 11 <= number % 100 <= 19:
                return "модулей"
            last_digit = number % 10
            if last_digit == 1:
                return "модуль"
            elif 2 <= last_digit <= 4:
                return "модуля"
            else:
                return "модулей"

        return [block_counter, get_blocks_declension(block_counter)]

    def get_points_quantity(self):
        blocks_with_points_query = self.blocks.annotate(points_count=Count('points'))
        total_points = blocks_with_points_query.aggregate(total_points=Sum('points_count'))['total_points'] or 0

        def get_point_declension(number):
            if 11 <= number % 100 <= 19:
                return "уроков"
            last_digit = number % 10
            if last_digit == 1:
                return "урок"
            elif 2 <= last_digit <= 4:
                return "урока"
            else:
                return "уроков"

        return [total_points, get_point_declension(total_points)]

    def get_steps_quantity(self):
        steps_counter = StepForPoint.objects.filter(
            point_for_training_block__training_course_block__training_course=self
        ).count()

        return steps_counter

    def get_questions_quantity(self):
        question_counter = QuestionForStep.objects.filter(
            step__point_for_training_block__training_course_block__training_course=self
        ).count()

        def get_question_declension(number):
            if 11 <= number % 100 <= 19:
                return "тестов"
            last_digit = number % 10
            if last_digit == 1:
                return "тест"
            elif 2 <= last_digit <= 4:
                return "теста"
            else:
                return "тестов"

        return [question_counter, get_question_declension(question_counter)]

    class Meta:
        verbose_name = 'Курс обучения'
        verbose_name_plural = 'Курсы обучения'
        ordering = ['-priority']


class CoursePack(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название пакета курсов', unique=True)
    meta_description = models.CharField(max_length=255, verbose_name="Description meta tag")
    description = models.TextField(verbose_name='Краткое описание пакета курсов')
    slug = models.SlugField(max_length=255, verbose_name='slug')
    image = models.ImageField(verbose_name='Обложка', upload_to='media/education_platform/images/')
    price = models.DecimalField(max_digits=8,
                                decimal_places=2,
                                verbose_name='Стоимость',
                                blank=True,
                                null=True,
                                default=0)
    courses = models.ManyToManyField(to=TrainingCourse)
    published = models.BooleanField(verbose_name='Опубликовать', default=False)

    class Meta:
        verbose_name = 'Пакет курсов'
        verbose_name_plural = 'Пакеты курсов'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def total_time_to_study(self):
        """
        Подсчитывает суммарное время изучения всех курсов, входящих в пакет.
        """
        total_time_to_study = 0
        for course in self.courses.all():
            total_time_to_study += course.time_to_study
        return total_time_to_study

    def get_absolute_url(self):
        return reverse('education_platform:course_pack_detail',
                       args=[self.slug])


class AccessToCourse(models.Model):
    student = models.ForeignKey(to=Student, on_delete=models.CASCADE)
    training_course = models.ForeignKey(to=TrainingCourse, on_delete=models.CASCADE)

    def __str__(self):
        return f'Студент {self.student} имеет доступ к курсу {self.training_course.title}.'

    class Meta:
        verbose_name = 'Доступ к курсу'
        verbose_name_plural = 'Доступы к курсам'


class AccessToCoursePack(models.Model):
    student = models.ForeignKey(to=Student, on_delete=models.CASCADE)
    course_pack = models.ForeignKey(to=CoursePack, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Доступ к пакету курсов'
        verbose_name_plural = 'Доступы к пакетам курсов'


class TrainingCourseBlock(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок блока')
    number = models.IntegerField(verbose_name='Порядковый номер')
    training_course = models.ForeignKey(to=TrainingCourse,
                                        on_delete=models.CASCADE,
                                        related_name='blocks',
                                        verbose_name='Курс обучения')

    def get_next_block(self, progress):
        """
        Через progress находим training_course, обращаемся к коллекции blocks, применяя фильтр,
        получаем объекты block, у которых number больше, чем у self.number, методом first() получаем первый
        объект коллекции. Если условия фильтра не выполнены, то возвращается None
        """
        next_blocks = progress.training_course.blocks.filter(number__gt=self.number)
        if next_blocks.exists():
            return next_blocks.first()
        else:
            return None

    def __str__(self):
        return f'{self.pk}. Модуль №{self.number} для курса {self.training_course}.'

    class Meta:
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'
        ordering = ['number']


class PointForTrainingBlock(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название урока')
    image = models.ImageField(verbose_name='Обложка',
                              upload_to='media/education_platform/images/points_logo/',
                              blank=True,
                              null=True)
    number = models.PositiveIntegerField(verbose_name='Номер урока')
    training_course_block = models.ForeignKey(to=TrainingCourseBlock,
                                              on_delete=models.CASCADE,
                                              related_name='points',
                                              verbose_name='Пункт обучения')
    time_to_study = models.PositiveIntegerField(verbose_name='Время для изучения', default=0)

    # views_counter = models.PositiveIntegerField(verbose_name='Количество просмотревших урок', default=0)
    # completed_counter = models.PositiveIntegerField(verbose_name='Количество прошедших урок', default=0)

    def get_absolute_url(self):
        """
        Возвращает ссылку на первый шаг в поинте
        """
        first_step_in_point = self.steps.first()
        return first_step_in_point.get_absolute_url()

    def is_completed(self, progress: 'CourseProgress') -> bool:

        completed_steps_set = set(progress.completed_steps.all())

        # Затем проверяем, что все шаги в текущем point также находятся в completed_steps
        return all(step in completed_steps_set for step in self.steps.all())

    def get_next_point(self, progress: "CourseProgress"):
        """
        Через self обращаемся к родительскому training_course_block, получаем коллекцию points этого block,
        применяя фильтр, ищем все points у которых number больше, чем у self.number. Методом first() возвращаем
        первый объект коллекции. Если условия фильтра не удовлетворены, то возвращаем None.
        """
        next_points = progress.current_block.points.filter(number__gt=self.number)
        if next_points.exists():
            return next_points.first()
        else:
            return None

    def total_steps_in_point(self):
        return self.steps.count()

    def __str__(self):
        return (f'Урок №{self.number} для модуля № {self.training_course_block.number} '
                f'курса {self.training_course_block.training_course.title}.')

    class Meta:
        verbose_name = 'Урок модуля обучения'
        verbose_name_plural = 'Уроки модулей обучения'
        ordering = ['number']


class StepForPoint(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название шага')
    number = models.PositiveIntegerField(verbose_name='Номер шага')
    point_for_training_block = models.ForeignKey(to=PointForTrainingBlock,
                                                 on_delete=models.CASCADE,
                                                 related_name='steps',
                                                 verbose_name='Урок обучения')
    text = models.TextField(verbose_name='Текст шага')
    # video_url = models.URLField(verbose_name='Ссылка на видео', blank=True, null=True)
    video = models.FileField(verbose_name='Загрузить видео', upload_to='education_platform/video/', blank=True,
                             null=True)

    def get_absolute_url(self):
        return reverse('education_platform:get_step_detail_view',
                       args=[self.point_for_training_block.
                       training_course_block.
                       training_course.pk, self.pk])

    def has_questions(self):
        return True if self.questions.all().count() > 0 else False

    def is_completed(self, progress: 'CourseProgress') -> bool:
        """
        Метод проверяет, завершен ли шаг в данном прогрессе? Принимает объект CourseProgress
        """
        return self in progress.completed_steps.all()

    def get_next_step_pk(self, progress: 'CourseProgress'):
        """
        Возвращает pk следующего шага курса
        """
        next_step = progress.current_point.steps.filter(pk__gt=self.pk)
        if next_step.exists():
            return next_step.first().pk
        else:
            # Если следующего шага нет, то пытаемся получить следующий point и его первый шаг
            next_point = progress.current_point.get_next_point(progress)
            if next_point:
                next_step = next_point.steps.all().first()
                return next_step.pk
            else:
                next_block = progress.current_block.get_next_block(progress)
                if next_block:
                    next_step = next_block.points.first().steps.first()
                    return next_step.pk
                else:
                    return None

    def get_previous_step_pk(self, progress):
        """
        Возвращает pk предыдущего шага
        """
        previous_steps = progress.current_point.steps.filter(pk__lt=self.pk)
        if previous_steps.exists():
            previous_step_pk = previous_steps.last().pk
            return previous_step_pk
        else:
            return None

    def __str__(self):
        return f'Шаг №{self.number} для урока {self.point_for_training_block}'

    class Meta:
        verbose_name = 'Шаг для урока обучения'
        verbose_name_plural = 'Шаги для уроков обучения'
        ordering = ['number']


class QuestionForStep(models.Model):
    text = models.TextField(verbose_name='Текст вопроса')
    step = models.ForeignKey(to=StepForPoint,
                             on_delete=models.CASCADE,
                             related_name='questions',
                             verbose_name='Вопрос для шага')

    def __str__(self):
        return f'Вопрос для шага {self.step}.'

    class Meta:
        verbose_name = 'Вопрос к шагу'
        verbose_name_plural = 'Вопрос к шагу'


class AnswerForQuestion(models.Model):
    text = models.TextField(verbose_name='Текст ответа')
    is_true = models.BooleanField(verbose_name='Это правильный ответ')
    question = models.ForeignKey(to=QuestionForStep,
                                 on_delete=models.CASCADE,
                                 related_name='answers')

    def __str__(self):
        return f'Ответ к вопросу {self.question}. Правильный = {self.is_true}.'

    class Meta:
        verbose_name = 'Ответ к вопросу'
        verbose_name_plural = 'Ответы к вопросам'


class WhatWillYouLearnItem(models.Model):
    item_title = models.CharField(max_length=255, verbose_name='Чему вы научитесь?')
    training_course = models.ForeignKey(to=TrainingCourse,
                                        on_delete=models.CASCADE,
                                        related_name='what_will_you_learn_items')

    class Meta:
        verbose_name = 'Строка для списка "Чему вы научитесь?"'
        verbose_name_plural = 'Строки для списка "Чему вы научитесь?"'


class CourseProgress(models.Model):
    student = models.ForeignKey(to=Student, on_delete=models.CASCADE)
    training_course = models.ForeignKey(to=TrainingCourse, on_delete=models.CASCADE)
    completed_date = models.DateField(blank=True, null=True, default=None)

    completed_blocks = models.ManyToManyField(to=TrainingCourseBlock, blank=True)
    completed_points = models.ManyToManyField(to=PointForTrainingBlock, blank=True)
    completed_steps = models.ManyToManyField(to=StepForPoint, blank=True)
    current_block = models.ForeignKey(to=TrainingCourseBlock,
                                      on_delete=models.SET_NULL,
                                      blank=True,
                                      null=True,
                                      related_name='current_blocks')

    current_point = models.ForeignKey(to=PointForTrainingBlock,
                                      on_delete=models.SET_NULL,
                                      blank=True,
                                      null=True,
                                      related_name='current_points')

    current_step = models.ForeignKey(to=StepForPoint,
                                     on_delete=models.SET_NULL,
                                     blank=True,
                                     null=True,
                                     related_name='current_steps')

    is_completed = models.BooleanField(default=False, verbose_name='Завершено')
    last_action = models.DateTimeField(auto_now=True, verbose_name='Последняя активность')

    def check_and_make_course_completed(self, total_steps_in_course: int):
        """
        Проверка, завершен ли курс.
        Подсчитываем количество выполненных steps в progress.completed_steps с общим количеством
        steps в объекте TrainingCourse
        Если курс завершен, то сохраняем в поле is_completed значение True
        """
        if not self.is_completed:
            if total_steps_in_course == self.completed_steps.all().count():
                self.completed_date = timezone.now()
                self.is_completed = True
                self.save()

    def block_is_completed(self, block_pk):
        return True if block_pk in self.completed_blocks.values_list('pk', flat=True).all() else False

    def point_is_completed(self, point_pk):
        return True if point_pk in self.completed_points.values_list('pk', flat=True).all() else False

    def __str__(self):
        return f'Прогресс студента {self.student} по курсу {self.training_course.title}'

    class Meta:
        verbose_name = 'Прогресс курса'
        verbose_name_plural = 'Прогресс курсов'


class CommentForStep(models.Model):
    author = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name="Автор",
        related_name="comments"
    )
    step = models.ForeignKey(to=StepForPoint,
                             on_delete=models.CASCADE,
                             verbose_name="Шаг",
                             related_name="comments")
    text = models.TextField(verbose_name="Текст комментария")
    published = models.DateTimeField(auto_now_add=True, verbose_name="Опубликовано")
    updated = models.DateTimeField(auto_now=True, verbose_name="Отредактировано")
    parent = models.ForeignKey('self', on_delete=models.CASCADE,
                               related_name="answers",
                               blank=True,
                               null=True)

    class Meta:
        ordering = ['-published']

    def __str__(self):
        return f"Комментарий pk={self.pk} к шагу {self.step}"


class Transaction(models.Model):
    """
    Модель для хранения информации о платежах, совершенных пользователями.

    Поля:
    - user: Связь с пользователем, совершившим платеж.
    - amount: Сумма платежа.
    - payment_id: Уникальный идентификатор платежа, предоставленный ЮKassa.
    - status: Статус платежа (например, 'pending', 'succeeded', 'failed').
    - created_at: Время создания платежа.
    - product_type: Тип продукта, за который был совершен платеж (курс или пакет курсов).
    - product_id: Идентификатор продукта, за который был совершен платеж.
    - promo_code: Промокод примененный к покумке

    Методы:
    - __str__: Возвращает строковое представление объекта платежа.

    Метаданные:
    - verbose_name: Название модели в единственном числе.
    - verbose_name_plural: Название модели во множественном числе.
    """
    PRODUCT_TYPE_CHOICES = [
        ('course', 'Курс'),
        ('course_pack', 'Пакет курсов')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Пользователь')
    amount = models.DecimalField(max_digits=9, decimal_places=2,
                                 verbose_name='Сумма платежа')
    payment_id = models.CharField(max_length=100, unique=True,
                                  verbose_name='ID платежа от yookassa')
    status = models.CharField(max_length=50, verbose_name='Статус платежа')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Время создания платежа')
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPE_CHOICES,
                                    verbose_name='Тип продукта')
    product_id = models.PositiveIntegerField(verbose_name='ID продукта')
    promo_code = models.ForeignKey(to="PromoCode",
                                   on_delete=models.CASCADE,
                                   verbose_name='Промокод',
                                   related_name='promo_codes',
                                   blank=True,
                                   null=True,
                                   default=None)

    def __str__(self):
        return (f'Платеж от {self.user} за {self.product_type} - ID {self.product_id}.'
                f'Статус платежа {self.status}')

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'


class PromoCode(models.Model):
    code = models.CharField(verbose_name='code', max_length=8)
    sale_value = models.PositiveIntegerField(
        verbose_name='Скидка в процентах',
    )
    validity_period = models.DateField(verbose_name="Срок действия", blank=True, null=True, default=None)
    course = models.ForeignKey(to=TrainingCourse, on_delete=models.CASCADE, related_name='promo_codes')

    class Meta:
        verbose_name = 'Промо код'
        verbose_name_plural = 'Промо коды'

    def generate_code(self):
        chars = string.ascii_letters + string.digits
        new_code = ''.join([secrets.choice(chars) for _ in range(8)])
        return new_code

    def clean(self):
        if self.sale_value is None:
            raise ValidationError("Ты забыл указать скидку!")
        if self.sale_value < 1 or self.sale_value > 100:
            raise ValidationError("Скидка должна быть от 1% до 100%")

    def save(self, *args, from_api=False, **kwargs):
        """
        В момент сохранения объекта формируется словарь для
        отправки ботом сообщения.
        Аргумент from_api=True приходит, если сохранение происходит
        через обращение к api ботом.
        """
        promo_data = {
            'code': self.code,
            'sale_value': self.sale_value,
            'validity_period': self.validity_period,
            'course_title': self.course.title,
            'course_absolute_url': self.course.get_absolute_url(),
        }
        if from_api is True and promo_data['validity_period'] is not None:
            promo_data['validity_period'] = datetime.strptime(promo_data['validity_period'], '%Y-%m-%d').date()
        send_telegram_promo.delay(promo=promo_data)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.code


class PromoInDashboard(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название баннера')
    image = models.ImageField(upload_to='media/education_platform/images/promo_in_dashboard/',
                              verbose_name="Фото")
    text = models.TextField(verbose_name="Основной текст")
    link = models.CharField(max_length=350, verbose_name="Ссылка")
    published = models.BooleanField(verbose_name="Опубликовано", default=False)

    def image_tag(self):
        """
        Возвращает рендер картинки, используется в админке
        """
        if self.image:
            return format_html('<img src="{}" style="max-width:80px; max-height:80px;" />', self.image.url)
        else:
            return "No Image"

    image_tag.short_description = 'Image'

    class Meta:
        verbose_name = "Реклама в содержании курса"
        verbose_name_plural = "Рекламы в содержании курса"
