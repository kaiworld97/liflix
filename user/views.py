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
#날짜
from datetime import datetime
from django.utils.dateformat import DateFormat


# Create your views here.
def sign_up(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'user/signup.html')
    elif request.method == 'POST':

        username = request.POST.get('id', '')  # 유저네임이 필수라 이메일로 받지만 유저네임으로 저장
        password = request.POST.get('pw', '')
        password2 = request.POST.get('pw2', '')
        user_bio = request.POST.get('bio', '')
        user_birth = request.POST.get('birth', '')
        user_nick = request.POST.get('nick', '')
        user_img = request.FILES.get('selectFile')
        birth = request.POST.get('birth').split('-')[0]
        today = datetime.today().year

        a = int(today) -int(birth)

        if a >= 20:
            a = True
        else:
            a = False
        user_adult = a




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
                user = UserModel.objects.create_user(user_img=user_img, password=password, user_bio=user_bio,
                                                     user_nick=user_nick, username=username,user_birth=user_birth,
                                                     user_adult=user_adult)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                print(current_site)
                message = render_to_string('user/active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                mail_title = "계정 활성화 확인 이메일"
                mail_to = request.POST.get("id")
                print(mail_to)
                email = EmailMessage(mail_title, message, to=[mail_to])
                email.send()

                return redirect('/sign_in')


def activate(request, uid64, token):
    uid = force_str(urlsafe_base64_decode(uid64))
    user = UserModel.objects.get(pk=uid)

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user)
        return redirect("/")
    else:
        return render(request, 'main.html', {'error': '계정 활성화 오류'})


def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('email', '')  # 유저네임이 필수라 이메일이름으로 받지만 유저네임으로 저장
        password = request.POST.get('pw', '')

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
    return redirect('/sign_in')


@login_required
def update(request):
    if request.method == 'POST':
        user = request.user
        user.nick = request.POST['password']
        user.save()
        return redirect('/')
    return render(request, 'user/update.html')

# from django.contrib import messages
# from django.contrib.auth import update_session_auth_hash
# from django.contrib.auth.forms import PasswordChangeForm
#
# @login_required
# def change_password(request):
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user)  # Important!
#             messages.success(request, 'Your password was successfully updated!')
#             return redirect('/')
#         else:
#             messages.error(request, 'Please correct the error below.')
#     else:
#         form = PasswordChangeForm(request.user)
#     return render(request, 'user/password.html', {
#         'form': form
#     })
#
#
# class UserPasswordResetView(PasswordResetView):
#     template_name = 'password_reset.html' #템플릿을 변경하려면 이와같은 형식으로 입력
#
#     def form_valid(self, form):
#         if UserModel.objects.filter(username=self.request.POST.get("email")).exists():
#             opts = {
#                 'use_https': self.request.is_secure(),
#                 'token_generator': self.token_generator,
#                 'from_email': self.from_email,
#                 'email_template_name': self.email_template_name,
#                 'subject_template_name': self.subject_template_name,
#                 'request': self.request,
#                 'html_email_template_name': self.html_email_template_name,
#                 'extra_email_context': self.extra_email_context,
#             }
#             form.save(**opts)
#             return super().form_valid(form)
#         else:
#             return render(self.request, 'password_reset_done_fail.html')