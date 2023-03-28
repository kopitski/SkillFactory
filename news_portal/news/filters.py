from django_filters import FilterSet, DateFilter
from .models import Post
from django import forms


class PostFilter(FilterSet):
    publish_time = DateFilter(widget=forms.DateInput(attrs={'type': 'date'}),
                              lookup_expr='gt',
                              label='Published after'
                              )

    class Meta:
        model = Post
        fields = {'title': ['icontains'],
                  'text': ['icontains'],
                  }