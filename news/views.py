from django.shortcuts import render, redirect
from .models import NewsModel
import requests
import random
import json
import ast


def news_view(request):
    # user = request.user.is_authenticated
    # if user:
    head_news = random.sample(list(NewsModel.objects.all()), 10)
    cate = list(set(NewsModel.objects.values_list('code', flat=True)))
    news_list = {}
    for i in cate:
        news_cate = []
        for j in random.sample(list(NewsModel.objects.filter(code=i)), 10):

            news_cate.append(j)
        news_list[i] = news_cate
    return render(request, 'news/main.html', {'head_news': head_news, 'news_list': news_list, 'cate':cate})
    # else:
    #     return redirect('/sign_in')


def category_news_view(request, category):
    num = {100: '정치', 101: '경제', 102: '사회', 103: '생활/문화', 104: '세계', 105: 'IT/과학'}
    code = num[category]
    politics_news = list(NewsModel.objects.filter(code=code))
    head_news = random.sample(politics_news, 10)
    return render(request, 'news/category_news.html', {'head_news': head_news, 'politics_news': politics_news, 'code': code})


# def economy_news_view(request):
#     economy_news = list(NewsModel.objects.filter(code='경제'))
#     head_news = random.sample(economy_news, 10)
#     return render(request, 'news/economy_news.html', {'head_news': head_news, 'economy_news': economy_news, 'code': '경제'})
#
#
# def social_news_view(request):
#     social_news = list(NewsModel.objects.filter(code='사회'))
#     head_news = random.sample(social_news, 10)
#     return render(request, 'news/social_news.html', {'head_news': head_news, 'social_news': social_news, 'code': '사회'})
#
#
# def life_culture_news_view(request):
#     life_culture_news = list(NewsModel.objects.filter(code='생활/문화'))
#     head_news = random.sample(life_culture_news, 10)
#     return render(request, 'news/life_culture_news.html', {'head_news': head_news, 'life_culture_news': life_culture_news, 'code': '생활/문화'})
#
#
# def world_news_view(request):
#     world_news = list(NewsModel.objects.filter(code='세계'))
#     head_news = random.sample(world_news, 10)
#     return render(request, 'news/world_news.html', {'head_news': head_news, 'world_news': world_news, 'code': '세계'})
#
#
# def it_science_news_view(request):
#     it_science_news = list(NewsModel.objects.filter(code='IT/과학'))
#     head_news = random.sample(it_science_news, 10)
#     return render(request, 'news/it_science_news.html', {'head_news': head_news, 'it_science_news': it_science_news, 'code': 'IT/과학'})