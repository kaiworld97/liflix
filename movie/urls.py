from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.movie_view, name='list'),
    path('detail/', views.movie_detail, name='detail'),
]