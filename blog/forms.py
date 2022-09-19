from django.forms.models import ModelForm

from .models import Post


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'text', 'tags', 'image']
