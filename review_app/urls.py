from django.urls import path
from . import views

urlpatterns = [
    path('', views.anime, name='anime'),
    path('anime-detail/<int:pk>/', views.anime_detail, name='anime_detail'),
    path('anime/comment/<int:pk>/', views.add_comment, name='add_comment'),
    path('comment/approve/<int:pk>/', views.comment_approve, name='comment_approve'),
    path('comment/remove/<int:pk>/', views.comment_remove, name='comment_remove'),
    path('comment/comment_not_found/', views.comment_not_found, name='comment_not_found')
]