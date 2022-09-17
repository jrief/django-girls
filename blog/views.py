from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone

from formset.views import EditCollectionView

from .models import Post
from .forms import PostForm, PostCollection


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


class PostEditView(LoginRequiredMixin, EditCollectionView):
    model = Post
    collection_class = PostCollection
    template_name = 'blog/post_edit.html'
    extra_context = {'add_post': False}

    def get_object(self, queryset=None):
        if self.extra_context['add_post'] is False:
            return super().get_object(queryset)

    def form_collection_valid(self, form_collection):
        if self.extra_context['add_post'] is True:
            self.object = self.model(author=self.request.user)
        form_collection.cleaned_data['comment'].update(created_by=self.request.user)
        return super().form_collection_valid(form_collection)

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk})
