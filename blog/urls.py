from django.urls import path

from . import views


urlpatterns = [
    path('post/new/', views.PostEditView.as_view(add=True), name='post_new'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/edit', views.PostEditView.as_view(), name='post_edit'),
    path('', views.post_list, name='post_list'),
]
