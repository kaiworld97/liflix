from django.shortcuts import render, redirect
from .models import TweetModel, TweetComment
from user.models import UserModel
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, TemplateView

# Create your views here.


def home(request):
    user = request.user.is_authenticated # 사용자가 로그인이 되어있는지 안되어있는지 확인
    if user:
        return redirect('/tweet')
    else:
        return redirect('sign_in')


def tweet(request):
    if request.method == 'GET':
        user = request.user.is_authenticated  # 인증된(로그인된) 사용자 있냐

        if user: # 로그인한 유저가 있다면
            all_tweet = TweetModel.objects.all().order_by('-created_at')
            # TweetModel에 저장한 모든 데이터를 불러온다. 근데 최신순(역순)으로 불러온다! > order_by, 마이너스 붙여준것
            return render(request, 'tweet/tweet_home.html', {'tweet': all_tweet})
        else:
            return redirect('/sign-in')  # 로그인 안되어있을시 singin 페이지로 이동하고, 로그인 되어있으면 board 페이지로 이동.

    elif request.method == 'POST':
        user = request.user  # 지금 로그인 되어있는 사용자의 정보 전체
        content = request.POST.get('content')
        tags = request.POST.get('tag', '').split(',')
        if content == '':
            all_tweet = TweetModel.objects.all().order_by('-created_at')
            return render(request, 'tweet/tweet_home.html', {'error': '글은 공백일 수 없습니다'}, {'tweet': all_tweet})
        else:
            my_tweet = TweetModel.objects.create(author=user, content=content)
            for tag in tags:
                tag = tag.strip()
                if tag != '':  # 태그를 작성하지 않았을 경우에 저장하지 않기 위해서
                    my_tweet.tags.add(tag)
            my_tweet.save()  # 아래 네줄을 2줄로 대체
            return redirect('/tweet')

@login_required
def delete_tweet(request, id):
    my_tweet = TweetModel.objects.get(id=id)
    my_tweet.delete()
    return redirect('/tweet')


@login_required
def detail_tweet(request, id):
    my_tweet = TweetModel.objects.get(id=id)
    tweet_comment = TweetComment.objects.filter(tweet_id=id).order_by('-created_at')  # 댓글 가져오기
    return render(request, 'tweet/tweet_detail.html', {'tweet': my_tweet, 'comment': tweet_comment})


@login_required
def write_comment(request, id):  # tweet의 id
    if request.method == 'POST':
        comment = request.POST.get('comment', '')
        current_tweet = TweetModel.objects.get(id=id)  # 보기 누른 tweet 전체 가져오기
        user = UserModel.objects.get(username=request.user)

        TC = TweetComment()
        TC.comment = comment
        TC.author = user
        TC.tweet = current_tweet
        TC.save()

        return redirect('/tweet/'+str(id))  # comment 작성 후 다시 돌아가게끔!

@login_required
def update_tweet(request, id):
    my_tweet = TweetModel.objects.get(id=id)
    if request.method == "POST":
        my_tweet.content = request.POST['content']
        my_tweet.save()
        return redirect('/tweet/'+str(id))

    else:
        return render(request, 'tweet/tweet_update.html', {'my_tweet': my_tweet})


@login_required
def delete_comment(request, id):  # comment의 id
    comment = TweetComment.objects.get(id=id)
    current_tweet = comment.tweet.id
    comment.delete()
    return redirect('/tweet/'+str(current_tweet))  # 댓글 삭제하면 그 페이지에 머무르게끔


class TagCloudTV(TemplateView):
    template_name = 'taggit/tag_cloud_view.html'


class TaggedObjectLV(ListView):
    template_name = 'taggit/tag_with_post.html'
    model = TweetModel

    def get_queryset(self):
        return TweetModel.objects.filter(tags__name=self.kwargs.get('tag'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs['tag']
        return context



