from django.shortcuts import render, redirect
from .models import UserModel
from django.http import HttpResponse
from django.contrib.auth import get_user_model  # 사용자가 데이터베이스 안에 있는지 확인하는 함수
from django.contrib import auth
from django.contrib.auth.decorators import login_required
# 메일인증을 위한 것들
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token


# Create your views here.
def sign_up_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'user/signup.html')
    elif request.method == 'POST':

        username = request.POST.get('email', '')  # 유저네임이 필수라 이메일로 받지만 유저네임으로 저장
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        bio = request.POST.get('bio', '')

        if password != password2:
            # 패스워드가 다르다고 알람
            return render(request, 'user/signup.html', {'error': '패스워드를 확인 해 주세요!'})

        else:
            if username == '' or password == '':
                return render(request, 'user/signup.html', {'error': '이메일과,패스워드는 필수 입력 입니다.'})
            exist_user = get_user_model().objects.filter(username=username)
            if exist_user:
                return render(request, 'user/signup.html', {'error': '사용자가 존재합니다'})
            else:
                img_file = request.FILES.get('file')
                user = UserModel.objects.create_user(password=password, bio=bio, Img=img_file, username=username)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                # localhost:8000
                message = render_to_string('user/active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                mail_title = "계정 활성화 확인 이메일"
                mail_to = request.POST.get("email")
                print(mail_to)
                email = EmailMessage(mail_title, message, to=[mail_to])
                email.send()

                return redirect('/sign-in')


def active(request, uid64, token):
    uid = force_str(urlsafe_base64_decode(uid64))
    user = UserModel.objects.get(pk=uid)

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user)
        return redirect("home")
    else:
        return render(request, 'home.html', {'error': '계정 활성화 오류'})


def sign_in_view(request):
    if request.method == 'POST':
        username = request.POST.get('email', '')  # 유저네임이 필수라 이메일이름으로 받지만 유저네임으로 저장
        password = request.POST.get('password', '')

        me = auth.authenticate(request, username=username, password=password)
        if me is not None:
            auth.login(request, me)
            return redirect('/')
        else:
            return render(request, 'user/signin.html', {'error': '이메일 혹은 패스워드를 확인 해 주세요.'})
    elif request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'user/signin.html')


@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')
