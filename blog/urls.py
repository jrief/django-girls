from django.urls import path

from . import views


urlpatterns = [
    path('post/new/', views.post_new, name='post_new'),
    path('post/new_fs/', views.PostEditView.as_view(add=True), name='post_new_fs'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/edit', views.post_edit, name='post_edit'),
    path('post/<int:pk>/edit_fs', views.PostEditView.as_view(), name='post_edit_fs'),
    path('', views.post_list, name='post_list'),
]
