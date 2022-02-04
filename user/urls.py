from django.urls import path
from . import views

urlpatterns = [
    path('sign_up/', views.sign_up_view, name='sign_up'),
    path('sign_in/', views.sign_in_view, name='sign_in'),
    path('logout/', views.logout, name='logout'),
<<<<<<< Updated upstream
    path('active/<str:uid64>/<str:token>/', views.active, name="activate"),
]
=======

    path('', views.sign_in_view, name='sign_in'),
]
>>>>>>> Stashed changes
