from django.shortcuts import render

# Create your views here.


def movie_view(request):
    return render(request, 'movie/list.html')

def movie_detail(request):
    return render(request, 'movie/detail.html')