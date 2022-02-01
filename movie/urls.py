from django.urls import path
from . import views

urlpatterns = [
    path('movie/<int:id>', views.movie_view, name='movie'),
    path('movie/detail/<int:id>', views.movie_detail, name='detail_movie'),
]