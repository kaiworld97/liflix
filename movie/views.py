from django.shortcuts import render
from .models import MovieModel
import pandas as pd
# Create your views here.


def movie_view(request, id):

    return render(request, 'movie/list.html')


def movie_detail(request, id):
    movie = MovieModel.objects.get(code=id)
    return render(request, 'movie/detail.html', {'movie': movie})
