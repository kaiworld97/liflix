from django.db import models
import json
import ast

# Create your models here.

class MovieModel(models.Model):
    class Meta:
        db_table = "movie"

    code = models.IntegerField()
    title = models.CharField(max_length=256)
    director = models.CharField(max_length=256)
    actor = models.CharField(max_length=256)

    def set_actor(self, x):
        self.actor = json.dumps(x)

    def get_actor(self):
        return ast.literal_eval(json.loads(self.actor))

    genre = models.CharField(max_length=256)

    def set_genre(self, x):
        self.genre = json.dumps(x)

    def get_genre(self):
        return ast.literal_eval(json.loads(self.genre))

    similar = models.CharField(max_length=256)

    def set_similar(self, x):
        self.similar = json.dumps(x)

    def get_similar(self):
        return ast.literal_eval(json.loads(self.similar))
    trailer = models.URLField(max_length=256)
    poster = models.URLField(max_length=256)
    story = models.TextField()
