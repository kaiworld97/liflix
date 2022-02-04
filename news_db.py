import os
import django
import csv
import sys

# 프로젝트 이름.settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "liflix.settings")
django.setup()

from news.models import *  # django.setup() 이후에 임포트해야 오류가 나지 않음

# csv파일 경로
CSV_PATH_PRODUCTS = 'news_data.csv'
with open(CSV_PATH_PRODUCTS, encoding='UTF8') as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)  # 출력시 함께 출력되는 맨첫줄을 제외하고 출력하기 위함
    for row in data_reader:
        newsModel = NewsModel()
        newsModel.img = row[0]
        newsModel.title = row[1]
        newsModel.content = row[3]
        newsModel.code = row[4]
        newsModel.similar = row[2]
        newsModel.save()

# json화 된 파일 불러오기
# def view_movie_data():
#     hi = MovieModel.objects.get(code=171539)
#     print(hi.get_actor())
#     print(hi.get_genre())
# view_movie_data()