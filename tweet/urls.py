# tweet/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # 127.0.0.1:8000 과 views.py 폴더의 home 함수 연결 (기본 url)
    path('tweet/', views.board, name='board'),  # 127.0.0.1:8000/board 과 views.py 폴더의 board 함수 연결
    path('tweet/delete/<int:id>', views.delete_tweet, name='delete-tweet'),
    path('tweet/update/<int:id>', views.update_tweet, name='update-tweet'),
    path('tweet/<int:id>', views.detail_tweet, name='detail-tweet'),
    path('tweet/comment/<int:id>', views.write_comment, name='write-comment'),
    path('tweet/comment/delete/<int:id>', views.delete_comment, name='delete-comment'),
    path('tag/', views.TagCloudTV.as_view(), name='tag_cloud'),
    path('tag/<str:tag>/', views.TaggedObjectLV.as_view(), name='tagged_object_list'),

]

