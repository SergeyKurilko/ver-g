from django.contrib import admin
from comments.models import CommentForArticle


@admin.register(CommentForArticle)
class CommentForArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'published', 'article', 'parent']
    search_fields = ['id']

