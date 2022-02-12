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

# csv 파일을 데이터 프레임 형식으로 읽어 온다
movie_df = pd.read_table('movie_movie.csv', sep=',')
tokens = []
# 위에서 읽어온 파일에서 키워드와 장르를 더해서 tokens에 append한다
# 위의 두개는 csv로 저장하면서 문자열이 된 리스트라서 ast.literal_eval()로 리스트로 바꾸어서 더해준다
for i in range(0, len(movie_df['movie_genre'])):
    token = ast.literal_eval(movie_df['story_keyword'][i]) + ast.literal_eval(movie_df['movie_genre'][i])
    tokens.append(token)
movie_vec_tokens = []
# csv파일의 문자로 된 벡터리스트를 ast.literal_eval()와 np.array로 그냥 벡터 리스트로 바꾸어서 movie_vec_tokens에 append한다
for i in range(0, len(movie_df['movie_code'])):
    movie_vec_tokens.append(np.array(ast.literal_eval(movie_df['vec_token'][i])))
# model = FastText.load('fasttext_movie.model')
# FastText 모델을 위의 tokens로 학습시킨다 이건 서버 켜질때 훈련시키는 듯하다 이거 쓰고 서버켜지는 속도가 느려졌다
model2 = FastText(min_count=1, sentences=tokens)


# 뉴스 모달창에서 더브기를 클릭했을때 나오는 페이지
# id는 urls에서 movie/뒤에 붙어있는 그것이 맞다
def movie_view(request, id):
    if request.method == 'GET':
        user = request.user.is_authenticated
        # 로그인 상태가 아니면 로그인 창으로 redirect
        if user:
            # id는 뉴스의 아이디가 들어와서 뉴스 모델에서 해당 오브젝트를 get한다
            news = NewsModel.objects.get(id=id)
            # 해당 오브젝트의 similar_movie 영화코드 리스트를 가져와서 리스트에 담는다
            news_similar_movie = [i for i in news.get_similar_movie()]
            movie_list = []
            # 영화 코드를 하나씩 돌리면서 영화 오브젝트를 가져와서 영화 코드와 제목과 포스터를 json 형식으로 담아 movie_list에 담아준다
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


# 영화 포스터를 클릭하면 나오는 페이지를  render한다
def movie_detail(request, id):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            # request.user를 하면 username이 나오더라 그것을 사용해서 user object를 get
            user_id = UserModel.objects.get(username=request.user)
            # url에 쳐진 id를 가져와서 movie object를 가져 온다
            movie_id = MovieModel.objects.get(code=id)
            # UserMovieModel에서 movie_id와 user_id가 있는 것을 검색해본다
            movie_user = UserMovieModel.objects.filter(movie_id=movie_id, user_id=user_id)
            # 없으면 UserMovieModel를 생성한다
            if not movie_user:
                UserMovieModel.objects.create(movie_id=movie_id, user_id=user_id)
            # 영화 트레일러를 가져오기 위한 헤더
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
                'cookie': ''
            }
            # movie object를 가져온다
            movie = MovieModel.objects.get(code=id)
            # get_으로 문자열이 된 리스트를 리스트로 바꾼다
            movie.genre = movie.get_genre()
            movie.actor = movie.get_actor()
            similar_list = []
            # similar movie를 object로 가져온다 similar를 movie object list로 바꾼다
            for similar in movie.get_similar():
                similar_movie = MovieModel.objects.get(code=similar)
                similar_list.append(similar_movie)
            movie.similar = similar_list
            # 트레일러의 videoId, videoInKey, coverImage를 얻기 위해서 get 요청을 보낸다
            response = requests.get(f'https://movie.naver.com/movie/bi/mi/videoInfoJson.naver?mid={movie.trailer}',
                                    headers=headers)
            videoId = response.json()['videoId']
            videoInKey = response.json()['videoInKey']
            coverImage = response.json()['coverImage']
            # trailer 주소를 완성한다 이대로 iframe의 src에 넣기만 하면 된다
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
        # request.POST[''] 하면  post로 보내온 내용이 보인다
        post = request.POST['blue'].split(' ')
        user_object = UserModel.objects.get(username=request.user)
        # 쓸모없는 단어들 제거
        if '줄거리가' in post:
            post.remove('줄거리가')
        elif '내용이' in post:
            post.remove('내용이')
        post.remove('줘')
        post.remove('추천해')
        content = []
        # 영화가 포함되어 있으면
        if '영화' in post:
            post.remove('영화')
            # content_type 을 영화로 바꾼다 이건 html 한 개에서 둘 다 처리하기 위함
            content_type = '영화'
            # user가 본 영화가 있나 확인하고 있으면 비슷한 영화를 추천하기 위해 불러온다
            user_movie = UserMovieModel.objects.filter(user_id=user_object.id)
            # 위에서 다 제거하고 len이 0이면 그냥 영화 추천해달라는 말이기 때문에 유저가 본 영화 와 비슷한 영화를 추천해준다
            if len(post) == 0 and user_movie:
                movie_list = user_movie.values_list('movie_id', flat=True).distinct()
                similar_list = [MovieModel.objects.get(id=i).get_similar() for i in movie_list]
                _movie = []
                for i in random.sample(list(chain.from_iterable(similar_list)), 9):
                    content.append(MovieModel.objects.get(code=i))
            # len이 0이 아니면 키워드가 남았기 때문에 그 키워드를 모델에 돌려서 비슷한 영화를 얻어 온다
            elif len(post) != 0 and user_movie:
                for i in get_movie(post):
                    content.append(MovieModel.objects.get(code=i))
            # UserMovieModel에 없으면 랜덤으로 영화를 추천해 준다
            else:
                content.append(random.sample(list(MovieModel.objects.all()), 9))
        else:
            if '뉴스' in post:
                post.remove('뉴스')
            elif '기사' in post:
                post.remove('기사')
            content_type = '뉴스'
            # 넘어오는 카테고리 값마다 다른 추천을 보여주기 위함
            # 유저가 본 뉴스가 있으면 본 것과 비슷한 뉴스 없으면 랜덤 뉴스
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
                    # 카테고리 값이 없으면 그냥 랜덤 뉴스 추천
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


# 카테고리 별 본 뉴스와 비슷한 뉴스를 가져오는 함수
def news_content(data, user_id):
    # 만약 카테고리가 없으면 전체에서 가져온다
    if data == 'hi':
        news_list = UserNewsModel.objects.all().values_list('news_id', flat=True).distinct()
    else:
        # 카테고리가 있으면 해당 카테고리로 필터링해서 가져온다
        news_list = UserNewsModel.objects.filter(user_id=user_id, category=data).values_list('news_id',
                                                                                             flat=True).distinct()
    # news_list 에서 news_id로 NewsModel에서 object를 가져와서 비슷한 뉴스를 가져온다
    similar_list = [NewsModel.objects.get(id=i).get_similar_news() for i in news_list]
    _news = []
    # 가져온 비슷한 리스트에서 9개를 랜덤으로 뽑는다
    # chain.from_iterable()은 이중리스트를 flat하게 만들어준다
    for i in random.sample(list(chain.from_iterable(similar_list)), 9):
        #0을 붙힌 이유 똑같은 제목의 뉴스가 많아서...
        get_news = NewsModel.objects.filter(title=i)[0]

        similar_movie = []
        # try쓴 이유 뉴스에 비슷한 영화에 영화 코드가 아니라 영화 오브젝트가 들어가 있는 경우가 있어서 에러가 나기때문이다
        try:
            for j in random.sample(get_news.get_similar_movie(), 3):
                similar_movie.append(MovieModel.objects.get(code=j))
            get_news.similar_movie = similar_movie
            _news.append(get_news)
        except:
            continue
    return _news


# 카테고리 별 랜덤 뉴스를 가져오는 함수
def news_content1(data):
    _news = []
    if data == 'hi':
        # order_by는 정렬하는 것 앞에 -를 붙히면 역순이다 큰 것부터 작은 것으로~
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

# 밑에 두 함수는 벡터 평균을 구하는 함수이다
def l2_norm(x):
    return np.sqrt(np.sum(x ** 2))


def div_norm(x):
    norm_value = l2_norm(x)
    if norm_value > 0:
        return x * (1.0 / norm_value)
    else:
        return x


def get_movie(data):
    # 0으로된 100개짜리 배열을 만든다 밑에 값을 더하기 위해서
    avg_list = np.zeros(100)
    for j in data:
        # 평균 값으 더해준다
        avg_list += div_norm(model2.wv[j])
    # 평균값의 평균을 낸다
    vec_token = avg_list / len(data)
    # 위의 movie_vec_tokens에 넣는다
    movie_vec_tokens.append(vec_token)
    # df를 만든다
    movie_vec_df = pd.DataFrame(np.array(movie_vec_tokens))
    # 코사인 유사도를 구한다
    movie_cosine = cosine_similarity(movie_vec_df, movie_vec_df)
    # 그걸 데이터 프레임화한다
    movie_cosine = pd.DataFrame(movie_cosine, index=movie_vec_df.index, columns=movie_vec_df.index)
    # 마지막이 1266번째라 1266번재에 더한 마지막것의 비슷한 영화를 10개 구한다
    similar = movie_cosine[1266].sort_values(ascending=False)[:10].index.tolist()
    del similar[0]
    similar_code = []
    # 그 영화들 index를 영화 코드로 바꿔서 리스트를 리턴한다
    for j in similar:
        similar_code.append(movie_df.loc[j, 'movie_code'])
    movie_vec_tokens.pop()
    return similar_code
