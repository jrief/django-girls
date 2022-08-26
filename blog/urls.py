from django.urls import path
from . import views


urlpatterns = [
    path('new/', views.post_new, name='post_new'),
    path('<pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('', views.post_list, name='post_list'),
]
