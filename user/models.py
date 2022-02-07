# user/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.
class UserModel(AbstractUser):
    class Meta:
        db_table = "my_user"

    user_birth = models.DateField()
    user_bio = models.CharField(max_length=256, default='')
    user_img = models.FileField(upload_to='uploads/%Y%m%d')
    user_category = models.CharField(max_length=30, default='')
    user_nick = models.CharField(max_length=30, default='')
    user_adult = models.BooleanField (default=False)