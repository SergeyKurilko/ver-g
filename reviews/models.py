from django.db import models
from django.contrib.auth.models import User
from pytils.translit import slugify
from django.urls import reverse


class Review(models.Model):
    slug = models.SlugField(max_length=200, unique=True)
    service = models.CharField(max_length=250, verbose_name="Название услуги")
    text = models.TextField(verbose_name="Текст отзыва", blank=True, null=True)
    image = models.ImageField(verbose_name="Изображение", upload_to='reviews/images/%Y/%m/%d/')

    def __str__(self):
        return f"{self.id}. Отзыв на услугу {self.service}"

    def get_absolute_url(self):
        return reverse('reviews:review_detail', args=[self.slug, ])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.service)
        super().save(*args, **kwargs)


    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

