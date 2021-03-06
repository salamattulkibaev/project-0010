from . import views
from django.urls import path

urlpatterns = [
    path('posts', views.add_post, name="addPost"),
    path('<slug:slug>/', views.post_detail, name="detail"),
    path('<slug:slug>/edit/', views.post_update, name="update"),
    path('<slug:slug>/delete/', views.post_delete, name="delete"),
]