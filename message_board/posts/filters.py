from django_filters import FilterSet, ModelChoiceFilter, DateTimeFilter, \
  DateFilter, CharFilter, ChoiceFilter
from django.contrib.auth.models import User
from django.forms import DateInput, DateTimeInput

from .models import Response, Post


class ResponseFilter(FilterSet):
    response_author = ModelChoiceFilter(
        field_name='response_author',
        queryset=User.objects.all(),
        label='Автор статьи',
        empty_label='любой',
    )

    from_response_creation_time = DateTimeFilter(
        field_name='response_creation_time',
        label='С даты',
        lookup_expr='gte',
        widget=DateTimeInput(attrs={'type': 'date'})
    )

    to_response_creation_time = DateFilter(
        field_name='response_creation_time',
        label='До даты',
        lookup_expr='lte',
        widget=DateTimeInput(attrs={'type': 'date'})
    )

    response_text = CharFilter(
        field_name='response_text',
        label='Текст отклика содержит',
        lookup_expr='icontains',
    )

    # response_post = ModelChoiceFilter(
    #     field_name='response_post',
    #     queryset=Post.objects.all(),
    #     label='Объявление',
    #     empty_label='любое',
    # )

    class Meta:
        model = Response
        fields = [
            'response_text',
            'response_author',
            'from_response_creation_time',
            'to_response_creation_time',
            # 'response_post'
        ]