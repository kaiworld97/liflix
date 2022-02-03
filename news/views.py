from django.shortcuts import render, redirect
import requests


def news_view(request):
    # user = request.user.is_authenticated
    # if user:
    return render(request, 'base.html')
    # else:
    #     return redirect('/sign_in')