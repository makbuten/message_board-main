from django import forms
from froala_editor.widgets import FroalaEditor

from .models import *


class PostForm(forms.ModelForm):
    post_text = forms.CharField(widget=FroalaEditor(), label='Текст объявления')
    post_header = forms.CharField(widget=forms.Textarea,
                                  label='Заголовок объявления')
    post_category = forms.ChoiceField(choices=Post.CATEGORY_CHOICE,
                                      label='Категории объявления')

    class Meta:
        model = Post
        fields = [
            'post_category',
            'post_header',
            'post_text',
        ]


class PostEditForm(forms.ModelForm):
    post_text = forms.CharField(widget=FroalaEditor(), label='Текст объявления')
    post_header = forms.CharField(widget=forms.Textarea,
                                  label='Заголовок объявления')
    post_category = forms.ChoiceField(choices=Post.CATEGORY_CHOICE,
                                      label='Категории объявления')


    class Meta:
        model = Post
        fields = [
            'post_category',
            'post_header',
            'post_text',
            'post_author',

        ]


class ResponseForm(forms.ModelForm):
    response_text = forms.CharField(widget=forms.Textarea, label='текст отклика')

    class Meta:
        model = Response
        fields = [
            'response_text',
        ]
