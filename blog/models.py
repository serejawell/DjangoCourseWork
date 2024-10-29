from django.db import models
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length=200,verbose_name='заголовок')
    content = models.TextField(verbose_name='содержимое статьи')  #
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True,verbose_name='изображение')
    views = models.PositiveIntegerField(default=0,verbose_name='просмотры')
    published_at = models.DateTimeField(default=timezone.now,verbose_name='дата публикации')

    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'посты'

    def __str__(self):
        return self.title
