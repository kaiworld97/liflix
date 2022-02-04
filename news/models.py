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

    def set_code(self, x):
        self.genre = json.dumps(x)

    def get_code(self):
        return ast.literal_eval(json.loads(self.genre))

    similar = models.CharField(max_length=256)

    def set_similar(self, x):
        self.genre = json.dumps(x)

    def get_similar(self):
        return ast.literal_eval(json.loads(self.genre))
