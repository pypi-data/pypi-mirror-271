from django_filters.rest_framework import FilterSet
from ...app_models.models import book


class BookFilters(FilterSet):
    class Meta:
        model = book
        fields = {"id": ["exact"], "title": ["icontains"]}
        # fields = {"game_id": ["exact"], "step": ["gt", "lt"], "title": ["icontains"]}
