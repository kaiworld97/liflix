from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('sign_up/', views.sign_up, name='sign_up'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('logout/', views.logout, name='logout'),
    path('activate/<str:uid64>/<str:token>/', views.activate, name="activate"),
   ]

