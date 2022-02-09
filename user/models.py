# user/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from movie.models import MovieModel
from news.models import NewsModel


# Create your models here.
class UserModel(AbstractUser):
    class Meta:
        db_table = "my_user"

    user_birth = models.DateField()
    user_bio = models.CharField(max_length=256, default='')
    user_img = models.FileField(upload_to='uploads/%Y%m%d')
    user_category = models.CharField(max_length=30, default='')
    user_nick = models.CharField(max_length=30, default='')
    user_adult = models.BooleanField(default=False)


class UserNewsModel(models.Model):
    class Meta:
        db_table = "user_news"

    user_id = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    news_id = models.ForeignKey(NewsModel, on_delete=models.CASCADE)
    category = models.CharField(max_length=30, default='')


class UserMovieModel(models.Model):
    class Meta:
        db_table = "user_movie"

    user_id = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    movie_id = models.ForeignKey(MovieModel, on_delete=models.CASCADE)
