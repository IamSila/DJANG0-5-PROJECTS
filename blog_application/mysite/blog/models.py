from django.db import models
from django.utils import timezone
from django.conf import settings
# Create your models here.
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
    title = models.CharField(max_length=250)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    slug = models.SlugField(max_length=250)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=2,
        choices = Status,
        default = Status.DRAFT
    )
    class Meta:
        ordering = ['-publish']
        indexes = [models.Index(fields=['-publish']),]
    def __str__():
        return self.title
    