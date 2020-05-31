from django_filters.rest_framework import FilterSet, DateTimeFilter

from .models import Like


class LikesFilter(FilterSet):
    date_from = DateTimeFilter(field_name='liked_on',
                               lookup_expr='gte',
                               label='Start date')
    date_to = DateTimeFilter(field_name='liked_on',
                             lookup_expr='lte',
                             label='End date')

    class Meta:
        model = Like
        fields = ['date_from', 'date_to']

