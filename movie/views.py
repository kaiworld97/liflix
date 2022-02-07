from django.shortcuts import render
from .models import MovieModel
from news.models import NewsModel
import pandas as pd
import ast
import requests
import json
# Create your views here.


def movie_view(request, id):
    news = NewsModel.objects.get(id=id)
    news_similar_movie = [i for i in news.get_similar_movie()]
    movie_list = []
    for i in news_similar_movie:
        movie_info = {}
        movie = MovieModel.objects.get(code=i)
        movie_info['code'] = movie.code
        movie_info['title'] = movie.title
        movie_info['poster'] = movie.poster
        movie_list.append(movie_info)
    return render(request, 'movie/list.html', {'movie_list': movie_list})


def movie_detail(request, id):
    headers = {
        'authority': 'movie.naver.com',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
        'x-requested-with': 'XMLHttpRequest',
        'scheme': 'https',
        'charset': 'utf-8',
        'accept-encoding': 'gzip, deflate, br',
        'sec-ch-ua-model': '',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded; charset=utf-8',
        'accept': '*/*',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-dest': 'empty',
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': '_gcl_au=1.1.8403800.1643134254; NM_THUMB_PROMOTION_BLOCK=Y; _ga=GA1.2.1355247506.1642947339; _ga_7VKFYR6RV1=GS1.1.1643565950.12.0.1643565950.60; NM_VIEWMODE_AUTO=wide;'
    }

    movie = MovieModel.objects.get(code=id)
    movie.genre = movie.get_genre()
    movie.actor = movie.get_actor()
    similar_list = []
    for similar in movie.get_similar():
        similar_movie = MovieModel.objects.get(code=similar)
        similar_list.append(similar_movie)
    movie.similar = similar_list
    response = requests.get(f'https://movie.naver.com/movie/bi/mi/videoInfoJson.naver?mid={movie.trailer}', headers=headers)
    videoId = response.json()['videoId']
    videoInKey = response.json()['videoInKey']
    coverImage = response.json()['coverImage']

    trailer = f'https://movie.naver.com//movie/bi/mi/videoPlayer.naver?code={movie.code}&type=movie&videoId={videoId}&videoInKey={videoInKey}&coverImage={coverImage}&mid={movie.trailer}&autoPlay=true&playerSize=640x480'
    movie.trailer = trailer

    return render(request, 'movie/detail.html', {'movie': movie})
