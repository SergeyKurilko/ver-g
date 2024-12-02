from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from blog.models import Article, Category
from education_platform.models import TrainingCourse, CoursePack
from service.models import Service, ServiceCategory
from portfolio.models import Project


class ArticleSitemap(Sitemap):
    def items(self):
        return Article.objects.filter(published=True)


class CategorySitemap(Sitemap):
    def items(self):
        return Category.objects.all()


class ServiceCategorySitemap(Sitemap):
    def items(self):
        return ServiceCategory.objects.all()


class TrainingCoursesSitemap(Sitemap):
    def items(self):
        return TrainingCourse.objects.filter(published=True)


class CoursePacksSitemap(Sitemap):
    def items(self):
        return CoursePack.objects.filter(published=True)


class ProjectsSitemap(Sitemap):
    def items(self):
        return Project.objects.all()

class StaticViewSitemap(Sitemap):
    def items(self):
        return ['blog:about_us', 'blog:contacts', 'blog:policy']

    def location(self, item):
        return reverse(item)
