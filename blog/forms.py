from django.forms.models import ModelForm
from django.forms.fields import CharField

from .models import Post


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'text', 'tags', 'image']


class CommentForm(ModelForm):
    text = CharField()