from rest_framework import serializers
from education_platform.models import TrainingCourse, PromoCode
from comments.models import CommentForArticle


class TrainingCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingCourse
        fields = ['id', 'title', 'slug']

class PromoCodeSerializer(serializers.ModelSerializer):
    course_title = serializers.SerializerMethodField()
    course_absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = PromoCode
        fields = ['sale_value', 'validity_period', 'course', 'code', 'course_title', 'course_absolute_url']

    # Метод для получения title объекта course
    def get_course_title(self, obj):
        return obj.course.title

    # Метода для получения результата course.get_absolute_url()
    def get_course_absolute_url(self, obj):
        return obj.course.get_absolute_url()


class CommentForArticleSerializr(serializers.ModelSerializer):
    class Meta:
        model = CommentForArticle
        fields = ['text', 'author', 'article']