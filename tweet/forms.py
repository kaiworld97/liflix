from django.forms import ModelForm

from .models import *


class TweetForm(ModelForm):
    class Meta:
        model = TweetModel
        fields = ['author', 'content', 'tags']