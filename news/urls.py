from django.urls import path
from . import views

urlpatterns = [
    path('', views.news_view, name='news_view'),
    path('<int:category>/', views.category_news_view, name='category_view'),
]
