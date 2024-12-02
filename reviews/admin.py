from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from reviews.models import Review


class ReviewAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget(),
                           label='Текст',
                           required=False)

    class Meta:
        model = Review
        fields = ['service', 'image', 'text']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    form = ReviewAdminForm

