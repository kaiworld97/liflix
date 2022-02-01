import os
import django
import csv
import sys

# 프로젝트 이름.settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "liflix.settings")
django.setup()

from movie.models import *  # django.setup() 이후에 임포트해야 오류가 나지 않음

# csv파일 경로
CSV_PATH_PRODUCTS = 'movie_movie.csv'
with open(CSV_PATH_PRODUCTS, encoding='UTF8') as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)  # 출력시 함께 출력되는 맨첫줄을 제외하고 출력하기 위함
    for row in data_reader:
        movieModel = MovieModel()
        movieModel.code = row[0]
        movieModel.title = row[1]
        movieModel.director = row[3]
        movieModel.poster = row[5]
        movieModel.trailer = row[6]
        movieModel.story = row[8]
        movieModel.set_genre(row[2])
        movieModel.set_actor(row[4])
        movieModel.set_similar(row[7])
        movieModel.save()

# json화 된 파일 불러오기
# def view_movie_data():
#     hi = MovieModel.objects.get(code=171539)
#     print(hi.get_actor())
#     print(hi.get_genre())
# view_movie_data()