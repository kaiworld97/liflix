from django.urls import path
from . import views

urlpatterns = [
    path('', views.news_view, name='news_view'),
]
