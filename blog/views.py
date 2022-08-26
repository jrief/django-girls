from django.contrib.auth.decorators import login_required
from django.forms import Form, fields
from django.shortcuts import render
from django.http.response import HttpResponseRedirect, HttpResponseForbidden
from django.views.generic import DetailView
from django.utils import timezone
from django.utils.safestring import mark_safe

from .models import Post, Comment
from .forms import PostForm, CommentForm


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    context = {
        'posts': posts,
    }
    return render(request, 'blog/post_list.html', context)


def post_new(request):
    form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def post(self, request, **kwargs):
        form = CommentForm(request.POST)
        if request.user.is_authenticated and form.is_valid():
            post = self.get_object()
            Comment.objects.create(
                post=post,
                text=form.cleaned_data['text'],
                author=request.user,
            )
            return HttpResponseRedirect(redirect_to=request.path)
        return HttpResponseForbidden()
