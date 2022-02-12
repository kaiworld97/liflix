from django.urls import path
from . import views

urlpatterns = [
    # //<int:id> 에서 id는 뒤에 함수의 인자로 들어간다
    path('movie/<int:id>', views.movie_view, name='movie'),
    path('movie/detail/<int:id>', views.movie_detail, name='detail_movie'),
    path('liflix/', views.liflix, name='liflix'),
    path('blue/', views.blue, name='blue'),
]