from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import UpdateView
from django.urls import reverse
from django.utils import timezone

from formset.views import IncompleteSelectResponseMixin, FileUploadMixin, FormViewMixin

from .models import Post
from .forms import PostForm


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
            post.publish()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(data=request.POST, files=request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=True)
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


class PostEditView(IncompleteSelectResponseMixin, FileUploadMixin, FormViewMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_edit_new.html'
    add = False

    def get_object(self, queryset=None):
        if self.add is False:
            return super().get_object(queryset)

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        if self.add:
            form.instance.author = self.request.user
            form.instance.created_date = timezone.now()
            form.instance.save()
        result = super().form_valid(form)
        form.instance.publish()  # TODO: Create extra button in form
        return result
