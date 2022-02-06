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
