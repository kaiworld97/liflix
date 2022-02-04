@echo off
chcp 65001
echo static 을 생성합니다.
mkdir static
cd static
mkdir img

cd..
cls

echo.
echo 앱을 만듭니다.
echo.
echo 유저앱을 만듭니다.
python manage.py startapp user
echo.
echo 트윗앱을 만듭니다.
python manage.py startapp tweet
echo.
echo 뉴스앱을 만듭니다.
python manage.py startapp news
echo.
echo 영화앱을 만듭니다.
python manage.py startapp movie
cls
echo 앱 만들기를 완료했습니다.

echo.
echo 패키지를 설치 합니다.

echo newspaper3k을 설치합니다.

pip install newspaper3k
cls
echo.
echo bs4을 설치합니다.

pip install bs4

cls
echo.
echo pandas을 설치합니다.

pip install pandas

cls
echo.
echo requests을 설치합니다.

pip install requests

cls
echo.
echo schedule을 설치합니다.

pip install schedule

cls
echo.
echo boto3을 설치합니다.

pip install boto3


echo Mecab을 설치합니다.
git clone https://github.com/SOMJANG/Mecab-ko-for-Google-Colab.git
cd 'Mecab-ko-for-Google-Colab'
bash install_mecab-ko_on_colab_light_220111.sh
cd..

echo gensim을 설치합니다.
pip install gensim

cls
echo 설치를 완료했습니다.


@REM 패키지 txt 만들기
@REM pip freeze > requirements.txt

@REM requirements.txt 대로 설치하기
@REM pip install -r requirements.txt