from django.core.exceptions import ValidationError
from django.forms.fields import IntegerField
from django.forms.models import ModelForm, construct_instance, model_to_dict
from django.forms.widgets import Textarea, HiddenInput

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
    id = IntegerField(
        widget=HiddenInput,
        required=False,
    )

    class Meta:
        model = Comment
        fields = ['id', 'annotation']
        widgets = {
            'annotation': Textarea(attrs={'cols': 40, 'rows': 5}),
        }


class CommentCollection(FormCollection):
    min_siblings = 0
    extra_siblings = 0
    comment = CommentForm()
    add_label = "Add comment"

    def model_to_dict(self, main_object):
        opts = CommentForm._meta
        return [{'comment': model_to_dict(comment, fields=opts.fields)} for comment in main_object.comments.all()]

    def construct_instance(self, main_object, cleaned_data):
        for data in cleaned_data:
            try:
                comment_object = main_object.comments.get(id=data['comment']['id'])
            except (KeyError, Comment.DoesNotExist):
                comment_object = Comment(post=main_object)
            form_class = self.declared_holders['comment'].__class__
            form = form_class(data=data['comment'], instance=comment_object)
            if form.is_valid():
                if form.marked_for_removal:
                    comment_object.delete()
                else:
                    construct_instance(form, comment_object)
                    form.save()


class PostCollection(FormCollection):
    default_renderer = FormRenderer(field_css_classes='mb-3')
    post = PostForm()
    comments = CommentCollection()
