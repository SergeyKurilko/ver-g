from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from education_platform.models import TrainingCourseBlock, TrainingCourse, \
    QuestionForStep, StepForPoint, CoursePack, PromoCode


class PromoCodeAdminForm(forms.ModelForm):
    class Meta:
        model = PromoCode
        fields = ('code', 'sale_value', 'course', 'validity_period')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = TrainingCourse.objects.filter(is_free=False, discount=0)


class TrainingCourseForm(forms.ModelForm):
    title = forms.CharField(max_length=35, label='Название курса',
                            help_text="Максимум 35 символов")
    meta_description = forms.CharField(max_length=150, label="meta description",
                                       help_text="Максимум 150 символов",
                                       required=True)
    description = forms.CharField(widget=CKEditorUploadingWidget(), label='Короткое описание курса')
    full_description = forms.CharField(widget=CKEditorUploadingWidget(), label='Полное описание курса')
    about_author = forms.CharField(widget=CKEditorUploadingWidget(), label='Об авторе')
    priority = forms.IntegerField(label="Приоритет в очереди",
                                  min_value=1,
                                  help_text="Чем больше число, тем выше в списке курсов."
                                                         "Должно быть больше нуля.", initial=1)
    is_free = forms.BooleanField(label="Бесплатный",
                                 help_text="Если указана стоимость, то нужно снять галочку.",
                                 required=False)
    price = forms.DecimalField(label="Стоимость",
                               help_text='Если стоит галочка "Бесплатный", то оставить 0!',
                               initial=0)
    time_to_study = forms.IntegerField(label="Время для изучения", min_value=1,
                                       help_text="Указывается в часах. Должно быть больше нуля.",
                                       initial=1)
    completed_counter = forms.IntegerField(label="Прошли обучение",
                                           help_text="Количество человек, завершивших курс."
                                                     "Изначально = 0", initial=0)

    signature = forms.FileField(label="Подпись автора",
                                 help_text="Формат svg! "
                                           "Высота: 115px, Ширина 115-125px.")



    class Meta:
        model = TrainingCourse
        fields = ['title','image', 'difficulty', 'priority', 'description',
                  'full_description', 'who_is_this_course_for',
                  'author', 'author_title', 'signature', 'about_author',
                  'category', 'tags', 'is_free', 'price', 'discount',
                  'time_to_study', 'completed_counter', 'published']

class CoursePackForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget(),
                                  label='Короткое описание пакета курсов')

    class Meta:
        model = CoursePack
        fields = ['title', 'image', 'price', 'courses', 'description']


class QuestionForStepForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget(), label='Текст вопроса')

    class Meta:
        model = QuestionForStep
        fields = '__all__'


class StepForPointForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget(), label='Текст шага')

    class Meta:
        model = StepForPoint
        fields = '__all__'