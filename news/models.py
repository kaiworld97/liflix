from django.db import models

# Create your models here.
# class News(models.Model):
#     title = models.CharField(max_length=200)
#     content = models.TextField()


class NewsModel(models.Model):
    class Meta:
        db_table = "news"
    title = models.CharField(max_length=256)
    content = models.TextField()
    img = models.URLField()