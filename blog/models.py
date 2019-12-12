from django.conf import settings
from django.db import models
from django.utils import timezone


class Tag(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<Tag: {}>'.format(self.id)        

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name='tags')

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )

    text = models.TextField()

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

    age = models.PositiveIntegerField()

    def __str__(self):
        return str(self.text)
    
    @classmethod
    def cmet(cls):
        print("Class Meth")

    @staticmethod
    def smet():
        print("Static Meth")

class CensoredManager(models.Manager):
    def all(self):
        return self.filter(age__gt=18)

class CensoredComment(Comment):
    class Meta:
        proxy = True

    def __str__(self):
        return str(self.entry_date)
    
    objects = CensoredManager()
