from django.core.exceptions import ValidationError
from django.forms.models import ModelForm, construct_instance, model_to_dict
from django.forms.widgets import Textarea

from formset.collection import FormCollection
from formset.renderers.bootstrap import FormRenderer
from formset.widgets import UploadedFileInput, SelectizeMultiple

from .models import Post, Comment


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
    class Meta:
        model = Comment
        fields = ['annotation']
        widgets = {
            'annotation': Textarea(attrs={'cols': 40, 'rows': 5}),
        }

    def model_to_dict(self, main_object):
        if comment_object := main_object.comments.first():
            return model_to_dict(comment_object, CommentForm._meta.fields, CommentForm._meta.exclude)
        return {}

    def construct_instance(self, main_object, data):
        comment_object = main_object.comments.first()
        if not comment_object:
            comment_object = Comment(post=main_object)
        form = CommentForm(data=data, instance=comment_object)
        if form.is_valid():
            construct_instance(form, comment_object)
            form.save()


class PostCollection(FormCollection):
    default_renderer = FormRenderer(field_css_classes='mb-3')

    post = PostForm()

    comment = CommentForm()
