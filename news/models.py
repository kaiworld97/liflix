from django.db import models
import ast
import json


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
    code = models.CharField(max_length=256)
    similar_news = models.TextField()

    def set_similar_news(self, x):
        self.similar_news = json.dumps(x)

    def get_similar_news(self):
        return ast.literal_eval(json.loads(self.similar_news))

    similar_movie = models.CharField(max_length=256)

    def set_similar_movie(self, x):
        self.similar_movie = json.dumps(x)

    def get_similar_movie(self):
        return ast.literal_eval(json.loads(self.similar_movie))
