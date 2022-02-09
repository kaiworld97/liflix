from django.shortcuts import render, redirect
from .models import NewsModel
from movie.models import MovieModel
from user.models import UserModel, UserNewsModel
from django.http import HttpResponse
import requests
import random
import json
import ast
from itertools import chain


def news_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            user_object = UserModel.objects.get(username=request.user)
            if UserNewsModel.objects.filter(user_id=user_object.id):
                news_list = UserNewsModel.objects.filter(user_id=user_object.id).values_list('news_id',
                                                                                             flat=True).distinct()
                similar_list = [NewsModel.objects.get(id=i).get_similar_news() for i in news_list]
                head_news = []
                for i in random.sample(list(chain.from_iterable(similar_list)), 9):
                    get_news = NewsModel.objects.filter(title=i)[0]
                    similar_movie = []
                    try:
                        for j in random.sample(get_news.get_similar_movie(),3):
                            similar_movie.append(MovieModel.objects.get(code=j))
                        get_news.similar_movie = similar_movie
                        head_news.append(get_news)
                    except:
                        continue
            else:
                head_news = []
                for i in NewsModel.objects.all().order_by('-hit'):
                    if len(head_news) == 9:
                        break
                    similar_movie = []
                    try:
                        for k in random.sample(i.get_similar_movie(), 3):
                            similar_movie.append(MovieModel.objects.get(code=k))
                        i.similar_movie = similar_movie
                        head_news.append(i)
                    except:
                        continue
            cate = list(set(NewsModel.objects.values_list('code', flat=True)))
            news_list = {}
            for i in cate:
                news_cate = []
                for j in random.sample(list(NewsModel.objects.filter(code=i)), 9):
                    similar_movie = []
                    try:
                        for k in random.sample(j.get_similar_movie(), 3):
                            similar_movie.append(MovieModel.objects.get(code=k))
                        j.similar_movie = similar_movie
                        news_cate.append(j)
                    except:
                        continue
                news_list[i] = news_cate
            return render(request, 'news/main.html', {'head_news': head_news, 'news_list': news_list, 'cate': cate})
        else:
            return redirect('/sign_in')


def category_news_view(request, category):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            num = {100: '정치', 101: '경제', 102: '사회', 103: '생활/문화', 104: '세계', 105: 'IT/과학'}
            code = num[category]
            politics_news = list(NewsModel.objects.filter(code=code).order_by('-hit'))
            head_news = []
            for i in politics_news:
                if len(head_news) == 9:
                    break
                similar_movie = []
                try:
                    for k in random.sample(i.get_similar_movie(), 3):
                        similar_movie.append(MovieModel.objects.get(code=k))
                    i.similar_movie = similar_movie
                    head_news.append(i)
                except:
                    continue
            politics_newss = []
            for i in random.sample(politics_news, 20):
                similar_movie = []
                try:
                    for k in random.sample(i.get_similar_movie(), 3):
                        similar_movie.append(MovieModel.objects.get(code=k))
                    i.similar_movie = similar_movie
                    politics_newss.append(i)
                except:
                    continue
            return render(request, 'news/category_news.html',
                          {'head_news': head_news, 'politics_news': politics_newss, 'code': code})
        else:
            return redirect('/sign_in')
    elif request.method == 'POST':
        user = UserModel.objects.get(username=request.user)
        news = NewsModel.objects.get(id=category)
        news_user = UserNewsModel.objects.filter(news_id=news, user_id=user)
        if not news_user:
            UserNewsModel.objects.create(news_id=news, user_id=user, category=news.code)
            news.hit += 1

            news.save()
        return HttpResponse('save')
