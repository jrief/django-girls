from django.core.exceptions import ValidationError
from django.forms.models import ModelForm
from django.forms.fields import CharField
from django.forms.widgets import Textarea

from formset.widgets import UploadedFileInput, SelectizeMultiple

from .models import Post


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'text', 'tags', 'image']
        widgets = {
            'image': UploadedFileInput,
            'tags': SelectizeMultiple,
            'text': Textarea(attrs={'cols': 40, 'rows': 5}),
        }

    def clean_tags(self):
        if not self.cleaned_data['tags']:
            raise ValidationError("Please classify your post")
        return self.cleaned_data['tags']


class CommentForm(ModelForm):
    text = CharField()
