from django.shortcuts import render, redirect
from .models import MovieModel
from news.models import NewsModel
from user.models import UserModel, UserMovieModel, UserNewsModel
import pandas as pd
import ast
import requests
# import json
from django.http import HttpResponse
from gensim.models import FastText
from itertools import chain
import random
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

movie_df = pd.read_table('movie_movie.csv', sep=',')
tokens = []
for i in range(0, len(movie_df['movie_genre'])):
  token = ast.literal_eval(movie_df['story_keyword'][i]) + ast.literal_eval(movie_df['movie_genre'][i])
  tokens.append(token)
movie_vec_tokens = []
for i in range(0, len(movie_df['movie_code'])):
    movie_vec_tokens.append(np.array(ast.literal_eval(movie_df['vec_token'][i])))
# model = FastText.load('fasttext_movie.model')
model2 = FastText(min_count=1, sentences=tokens)


# Create your views here.


def movie_view(request, id):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
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
        else:
            return redirect('/sign_in')


def movie_detail(request, id):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            user_id = UserModel.objects.get(username=request.user)
            movie_id = MovieModel.objects.get(code=id)
            movie_user = UserMovieModel.objects.filter(movie_id=movie_id, user_id=user_id)
            if not movie_user:
                UserMovieModel.objects.create(movie_id=movie_id, user_id=user_id)
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
            response = requests.get(f'https://movie.naver.com/movie/bi/mi/videoInfoJson.naver?mid={movie.trailer}',
                                    headers=headers)
            videoId = response.json()['videoId']
            videoInKey = response.json()['videoInKey']
            coverImage = response.json()['coverImage']

            trailer = f'https://movie.naver.com//movie/bi/mi/videoPlayer.naver?code={movie.code}&type=movie&videoId={videoId}&videoInKey={videoInKey}&coverImage={coverImage}&mid={movie.trailer}&autoPlay=true&playerSize=640x480'
            movie.trailer = trailer

            return render(request, 'movie/detail.html', {'movie': movie})
        else:
            return redirect('/sign_in')


def liflix(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return render(request, 'movie/liflix.html')
        else:
            return redirect('/sign_in')


def blue(request):
    if request.method == 'POST':
        print(request.POST['blue'])
        post = request.POST['blue'].split(' ')
        user_object = UserModel.objects.get(username=request.user)
        if '줄거리가' in post:
            post.remove('줄거리가')
        elif '내용이' in post:
            post.remove('내용이')
        post.remove('줘')
        post.remove('추천해')
        content = []

        if '영화' in post:
            post.remove('영화')
            content_type = '영화'
            user_movie = UserMovieModel.objects.filter(user_id=user_object.id)
            if len(post) == 0 and user_movie:
                movie_list = user_movie.values_list('movie_id', flat=True).distinct()
                similar_list = [MovieModel.objects.get(id=i).get_similar() for i in movie_list]
                _movie = []
                for i in random.sample(list(chain.from_iterable(similar_list)), 9):
                    content.append(MovieModel.objects.get(code=i))
            elif len(post) != 0 and user_movie:
                for i in get_movie(post):
                    content.append(MovieModel.objects.get(code=i))
            else:
                content.append(random.sample(list(MovieModel.objects.all()), 9))
        else:
            if '뉴스' in post:
                post.remove('뉴스')
            elif '기사' in post:
                post.remove('기사')
            content_type = '뉴스'

            if UserNewsModel.objects.filter(user_id=user_object.id):
                if '과학' in post:
                    content = news_content('IT/과학', user_object.id)
                elif '생활문화' in post:
                    content = news_content('생활/문화', user_object.id)
                elif '정치' in post:
                    content = news_content('정치', user_object.id)
                elif '경제' in post:
                    content = news_content('경제', user_object.id)
                elif '세계' in post:
                    content = news_content('세계', user_object.id)
                elif '사회' in post:
                    content = news_content('사회', user_object.id)
                else:
                    content = news_content('hi', user_object.id)
            else:
                if '과학' in post:
                    content = news_content1('IT/과학')
                elif '생활문화' in post:
                    content = news_content1('생활/문화')
                elif '정치' in post:
                    content = news_content1('정치')
                elif '경제' in post:
                    content = news_content1('경제')
                elif '세계' in post:
                    content = news_content1('세계')
                elif '사회' in post:
                    content = news_content1('사회')
                else:
                    content = news_content1('hi')
        return render(request, 'movie/blue.html', {'content': content, 'type': content_type})


def news_content(data, user_id):
    if data == 'hi':
        news_list = UserNewsModel.objects.all().values_list('news_id', flat=True).distinct()
    else:
        news_list = UserNewsModel.objects.filter(user_id=user_id).values_list('news_id', flat=True).distinct()
    similar_list = [NewsModel.objects.get(id=i).get_similar_news() for i in news_list]
    _news = []
    for i in random.sample(list(chain.from_iterable(similar_list)), 9):
        get_news = NewsModel.objects.filter(title=i)[0]
        similar_movie = []
        try:
            for j in random.sample(get_news.get_similar_movie(), 3):
                similar_movie.append(MovieModel.objects.get(code=j))
            get_news.similar_movie = similar_movie
            _news.append(get_news)
        except:
            continue
    return _news


def news_content1(data):
    _news = []
    if data == 'hi':
        for i in NewsModel.objects.all().order_by('-hit'):
            if len(_news) == 9:
                break
            similar_movie = []
            try:
                for k in random.sample(i.get_similar_movie(), 3):
                    similar_movie.append(MovieModel.objects.get(code=k))
                i.similar_movie = similar_movie
                _news.append(i)
            except:
                continue
    else:
        for i in NewsModel.objects.filter(code=data).order_by('-hit').values_list('news_id', flat=True).distinct():
            if len(_news) == 9:
                break
            similar_movie = []
            try:
                for k in random.sample(i.get_similar_movie(), 3):
                    similar_movie.append(MovieModel.objects.get(code=k))
                i.similar_movie = similar_movie
                _news.append(i)
            except:
                continue
    return _news


def l2_norm(x):
    return np.sqrt(np.sum(x ** 2))


def div_norm(x):
    norm_value = l2_norm(x)
    if norm_value > 0:
        return x * (1.0 / norm_value)
    else:
        return x


def get_movie(data):
    avg_list = np.zeros(100)
    for j in data:
        avg_list += div_norm(model2.wv[j])
    vec_token = avg_list / len(data)
    movie_vec_tokens.append(vec_token)
    movie_vec_df = pd.DataFrame(np.array(movie_vec_tokens))
    movie_cosine = cosine_similarity(movie_vec_df, movie_vec_df)
    movie_cosine = pd.DataFrame(movie_cosine, index=movie_vec_df.index, columns=movie_vec_df.index)
    similar = movie_cosine[1266].sort_values(ascending=False)[:10].index.tolist()
    del similar[0]
    similar_code = []
    for j in similar:
        similar_code.append(movie_df.loc[j, 'movie_code'])
    movie_vec_tokens.pop()
    return similar_code
