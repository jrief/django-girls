from django.forms.models import ModelForm
from django.forms.fields import CharField

from formset.widgets import UploadedFileInput, SelectizeMultiple

from .models import Post


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'text', 'tags', 'image']
        widgets = {
            'image': UploadedFileInput,
            'tags': SelectizeMultiple,
        }


class CommentForm(ModelForm):
    text = CharField()
