from django.shortcuts import render, get_object_or_404, redirect
from django.http.response import HttpResponseRedirect, HttpResponseForbidden
from django.views.generic import DetailView
from django.utils import timezone

from .models import Post, Comment
from .forms import PostForm, CommentForm


def post_list(request):
    posts = Post.objects.order_by('published_date')
    context = {
        'posts': posts,
    }
    return render(request, 'blog/post_list.html', context)


def post_new(request):
    if request.method == "POST":
        form = PostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.created_date = timezone.now()
            post.save()
            form.save_m2m()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(data=request.POST, files=request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


# class PostDetailView(DetailView):
#     model = Post
#     template_name = 'blog/post_detail.html'
#
#     def post(self, request, **kwargs):
#         form = CommentForm(request.POST)
#         if request.user.is_authenticated and form.is_valid():
#             post = self.get_object()
#             Comment.objects.create(
#                 post=post,
#                 text=form.cleaned_data['text'],
#                 author=request.user,
#             )
#             return HttpResponseRedirect(redirect_to=request.path)
#         return HttpResponseForbidden()
