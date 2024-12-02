from datetime import timedelta

from django.contrib import admin
from django.utils import timezone
import nested_admin

from education_platform.admin_forms import TrainingCourseForm, QuestionForStepForm, StepForPointForm, \
    CoursePackForm, PromoCodeAdminForm
from education_platform.models import Student, TrainingCourse, AccessToCourse, TrainingCourseBlock, \
    QuestionForStep, AnswerForQuestion, StepForPoint, TrainingCourseCategory, TrainingCourseSubCategory, \
    PointForTrainingBlock, Tag, WhatWillYouLearnItem, CourseProgress, CoursePack, PromoCode, PromoInDashboard, \
    Transaction


class WhatWillYouLearnItemInline(nested_admin.NestedStackedInline):
    model = WhatWillYouLearnItem
    extra = 1


class AnswerInline(nested_admin.NestedTabularInline):
    model = AnswerForQuestion
    extra = 1


class QuestionForStepInline(nested_admin.NestedStackedInline):
    model = QuestionForStep
    extra = 0
    inlines = [AnswerInline]
    form = QuestionForStepForm

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.max_num = 1  # Устанавливаем максимальное количество форм
        return formset


class StepForPointInline(nested_admin.NestedStackedInline):
    model = StepForPoint
    extra = 0
    inlines = [QuestionForStepInline]
    form = StepForPointForm


class PointForTrainingBlockInline(nested_admin.NestedStackedInline):
    model = PointForTrainingBlock
    extra = 0
    inlines = [StepForPointInline]


class TrainingCourseBlockAdmin(nested_admin.NestedModelAdmin):
    model = TrainingCourseBlock
    extra = 0
    inlines = [PointForTrainingBlockInline]
    list_display = ['pk', 'title', 'training_course']
    search_fields = ['training_course__pk']
    list_display_links = ['pk', 'title']


class TrainingCourseAdmin(nested_admin.NestedModelAdmin):
    model = TrainingCourse
    inlines = [WhatWillYouLearnItemInline]
    extra = 0
    form = TrainingCourseForm
    list_display = ['pk', 'title', 'is_free', 'image_tag', 'published']
    search_fields = ['pk', 'title']
    list_filter = ['is_free']
    list_display_links = ['pk', 'title']
    list_editable = ['published']


admin.site.register(TrainingCourse, TrainingCourseAdmin)
admin.site.register(TrainingCourseBlock, TrainingCourseBlockAdmin)
admin.site.register(Student)
admin.site.register(TrainingCourseCategory)
admin.site.register(TrainingCourseSubCategory)
admin.site.register(Tag)
admin.site.register(CourseProgress)

@admin.register(AccessToCourse)
class AccessToCourseAdmin(admin.ModelAdmin):
    list_display = ['pk', 'student', 'training_course']
    list_display_links = ['pk', 'student']
    search_fields = ['training_course']
    list_filter = ['student']



@admin.register(CoursePack)
class CoursePackAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'price', 'published']
    list_display_links = ['pk', 'title']
    list_editable = ['price', 'published']
    form = CoursePackForm


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'sale_value', 'course', 'validity_period')
    form = PromoCodeAdminForm

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj is None:
            form.base_fields['code'].initial = PromoCode().generate_code()
            form.base_fields['validity_period'].initial = timezone.now() + timedelta(days=30)
        return form

    def save_model(self, request, obj, form, change):
        if not obj.code:
            obj.code = PromoCode().generate_code()
        super().save_model(request, obj, form, change)


@admin.register(PromoInDashboard)
class PromoInDashboardAdmin(admin.ModelAdmin):
    list_display = ['title', 'link', 'image_tag', 'published']
    list_display_links = ['title', 'link']
    list_editable = ['published']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['payment_id','amount', 'status',
                    'created_at', 'product_type', 'product_id',
                    'user', 'promo_code']







