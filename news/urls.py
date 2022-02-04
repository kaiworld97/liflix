from django.urls import path
from . import views

urlpatterns = [
    path('news/', views.news_view, name='news-view'),
]
