import requests
import pandas as pd
from newspaper import Article
from bs4 import BeautifulSoup
from datetime import datetime


# Create your views here.
# 네이버 뉴스 페이지에서, 각각의 뉴스가 가진 URL을 리스트 형태로 만들어서 저장함
def make_urllist(page_num, code, date):
    urllist = []

    for i in range(1, page_num + 1):
        url = f'https://news.naver.com/main/list.naver?mode=LSD&mid=sec&sid1={code}&date={date}&page={i}'

        # 헤더를 붙여서
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
        }
        # 리퀘스트 요청을 보냄
        news = requests.get(url, headers=headers)

        # html 파싱을 위한 객체 생성
        soup = BeautifulSoup(news.content, 'html.parser')

        # ul 태그가 2개인데 그 중에 첫번째 것을 select
        news_list = soup.select('.type06_headline li dl')
        # 두번째 것을 select
        news_list.extend(soup.select('.type06 li dl'))

        # urllist 에 a 태그 내부의 href 내용 (기사 별 url 링크) 을 추가!
        for line in news_list:
            urllist.append(line.a.get('href'))
    return urllist


idx2word = {'100': '정치', '101': '경제', '102': '사회', '103': '생활/문화', '104': '세계', '105': 'IT/과학'}


def make_data(urllist, code):
    text_list = []
    title_list = []

    # 각 기사 별 Url 이 urllist 에 담겨있으니,
    # Article 이라는 newspaper3k 내부 함수를 이용해서 크롤링 진행
    for url in urllist:
        article = Article(url, language='ko')
        article.download()
        article.parse()
        # article.text 는 본문 // 제목을 가져오고 싶다면 article.title
        text_list.append(article.text)
        title_list.append(article.title)

    # news 라는 열에다가 기사 본문을 추가해서 데이터프레임 생성
    df = pd.DataFrame({'headline': title_list, 'news': text_list})
    # code 라는 열에다가는 기사 카테고리 추가
    df['code'] = idx2word[str(code)]
    return df


# code_list 로 카테고리 리스트를 만들어서,
# 카테고리 별로 크롤링을 진행하기 위한 함수
def make_total_data(page_num, code_list, date):
    df = None

    for code in code_list:
        urllist = make_urllist(page_num, code, date)
        df_temp = make_data(urllist, code)

        if df is not None:  # df가 채워져있나요? 물어보는 것
            # 채워져있으면, 이전 데이터프레임과 결합
            df = pd.concat([df, df_temp])
        else:
            # 채워져있지않으면, 지금 만들어진 데이터프레임을 그냥 df 라고 할당한다
            df = df_temp
    return df


# 1시간마다 크롤링 한 결과를 csv 파일로 저장
today = datetime.today().strftime("%Y%m%d")
code_list = [100, 101, 102, 103, 104, 105]
df = make_total_data(5, code_list, today)
df.to_csv('news_data.csv', index=False)
