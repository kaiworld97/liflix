import os
import django
import csv
import sys

# 프로젝트 이름.settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "liflix.settings")
django.setup()

from news.models import *  # django.setup() 이후에 임포트해야 오류가 나지 않음

# csv파일 경로
# CSV_PATH_PRODUCTS = 'news_news.csv'
# with open(CSV_PATH_PRODUCTS, encoding='UTF8') as in_file:
#     data_reader = csv.reader(in_file)
#     next(data_reader, None)  # 출력시 함께 출력되는 맨첫줄을 제외하고 출력하기 위함
#     for row in data_reader:
#         newsModel = NewsModel()
#         newsModel.img = row[0]
#         newsModel.title = row[1]
#         newsModel.content = row[5]
#         newsModel.code = row[6]
#         newsModel.set_similar_news(row[2])
#         newsModel.set_similar_movie(row[3])
#         newsModel.save()

# json화 된 파일 불러오기
# def view_news_data():
#     hi = NewsModel.objects.get(id=1)
#     for i in hi.get_similar_movie():
#         print(type(i))
# view_news_data()