from django.contrib.auth.models import User
from blog.models import Article
from django.db import models


class CommentForArticle(models.Model):
    text = models.TextField(verbose_name="Текст сообщения")
    author = models.CharField(max_length=50, verbose_name="Имя")
    published = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    article = models.ForeignKey(to=Article, on_delete=models.CASCADE, related_name="comments")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name="answers", blank=True, null=True)

    class Meta:
        verbose_name = "Комментарий к статье"
        verbose_name_plural = "Комментарий к статьям"
        ordering = ['-published']

    def __str__(self):
        return f"{self.id}. Комментарий к статье {self.article.title} от {self.author}. Parent: {self.parent}"

