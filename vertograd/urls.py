"""vertograd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.conf import settings
from debug_toolbar.toolbar import debug_toolbar_urls
from blog.sitemaps import ArticleSitemap, CategorySitemap, \
    ServiceCategorySitemap, StaticViewSitemap, TrainingCoursesSitemap, ProjectsSitemap, CoursePacksSitemap
from comments.views import api_comment_delete

sitemaps = {
    'posts': ArticleSitemap,
    'category': CategorySitemap,
    'uslugi': ServiceCategorySitemap,
    'static': StaticViewSitemap,
    'potfolio': ProjectsSitemap,
    'academy_courses': TrainingCoursesSitemap,
    'academy_course_packs': CoursePacksSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    path('robots.txt', TemplateView.as_view(template_name="blog/robots.txt", content_type='text/plain')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('blog.urls', namespace='blog')),
    path('my_orders/', include('order.urls', namespace='order')),
    path('portfolio/', include('portfolio.urls', namespace='portfolio')),
    path('uslugi/', include('service.urls', namespace='service')),
    path('otzivi/', include('reviews.urls', namespace='reviews')),
    path('comments/', include('comments.urls', namespace='comments')),
    path('academy/', include('education_platform.urls', namespace='education_platform')),
    path('api/', include("api.urls", namespace="api"))
]

# API = [
#     path('api/blog_comment_delete<int:comment_id>/from_<str:tele_id>', api_comment_delete)
# ]
#
# urlpatterns += API

urlpatterns += debug_toolbar_urls()


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
