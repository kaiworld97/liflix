# tweet/models.py
from django.db import models
from user.models import UserModel  # 유저 앱에 있는 모델 중 UserModel 을 가져와서 쓸거다
from taggit.managers import TaggableManager  # 우리 글에 Tag를 추가 할 수 있게


# Create your models here.
class TweetModel(models.Model):
    class Meta:
        db_table = "tweet"

    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)  # ForeignKey: 다른 db에서 내용(모델)을 가져오겠다 라는 뜻
    content = models.CharField(max_length=256)
    tags = TaggableManager(blank=True) # blank=True: 이게 비어있어도 상관없다 라는 뜻
    created_at = models.DateTimeField(auto_now_add=True)  # auto_now_add=True: 최초 save 시간을 저장
    updated_at = models.DateTimeField(auto_now=True)  # auto_now=True: save 할때마다 현재 시간으로 갱신


class TweetComment(models.Model):
    class Meta:
        db_table = "comment"
    tweet = models.ForeignKey(TweetModel, on_delete=models.CASCADE)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    comment = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)