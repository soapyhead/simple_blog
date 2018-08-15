from django.conf import settings
from django.db import models
from webpreview import web_preview


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField(default='', blank=True)

    def get_likes(self):
        return self.likes.filter(active=True)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-created_at', ]


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

    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'
        unique_together = (('user', 'post'),)
        ordering = ['-created_at', ]


def generate_filename(instance, filename):
    dirname = instance.post.id
    return f'{dirname}/{filename}'


class MediaFile(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='media_files')
    file = models.FileField(max_length=255,
                            upload_to=generate_filename)
    filename = models.CharField(max_length=255)


class Link(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='links')
    link = models.CharField(max_length=255)
    title = models.CharField(max_length=255, blank=True, null=True, default='')
    desc = models.CharField(max_length=255, blank=True, null=True, default='')
    image = models.CharField(max_length=255, blank=True, null=True, default='')

    @staticmethod
    def web_preview_link(link):
        return web_preview(link)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # wait for 10 seconds maximum
        try:
            self.title, self.desc, self.image = self.web_preview_link(self.link)
        except TimeoutError:
            print(f"{self.link} preview timeout")
        finally:
            super().save(force_insert, force_update, using, update_fields)
            if not self.title:
                print('GO CELERY')
