from django_filters.rest_framework import FilterSet, DateFromToRangeFilter

from .models import Like


class LikesFilter(FilterSet):
    date = DateFromToRangeFilter(field_name='liked_on',
                                 label='Date Range')

    class Meta:
        model = Like
        fields = ['date']


