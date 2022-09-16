from django.conf import settings
from django.db import models
from django.utils import timezone


class Tag(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<{self.__class__.__name__}(pk={self.id}): {self.name}>'


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    title = models.CharField(
        verbose_name="Title",
        max_length=200,
    )

    text = models.TextField(
        verbose_name="Body Text",
    )

    created_date = models.DateTimeField(
        auto_now_add=True,
    )

    published_date = models.DateTimeField(
        verbose_name="Published Date",
        blank=True,
        null=True,
    )

    tags = models.ManyToManyField(
        Tag,
        related_name='tags',
        blank=True,
    )

    image = models.ImageField(
        verbose_name="An Image",
        upload_to='uploads/images/',
        blank=True,
        null=True,
    )

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'<{self.__class__.__name__}(pk={self.id}): {self.title}>'


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )

    annotation = models.TextField(
        verbose_name="annotation",
        null=True,
        blank=True,
    )

    entry_date = models.DateTimeField(
        auto_now=True,
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_DEFAULT,
    )

    def __str__(self):
        return str(self.annotation)
