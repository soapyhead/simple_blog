from django.conf import settings
from django.db import models


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField(default='', blank=True)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-created_at',]


class LikeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='likes')
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    objects = LikeManager()

    class Meta:
        unique_together = (('user', 'post'),)
