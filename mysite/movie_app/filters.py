from django_filters import FilterSet
from .models import Film

class FilmFilter(FilterSet):
    class Meta:
        model = Film
        fields = {
            'year': ['gt', 'lt'],
            'country': ['exact'],
            'genres': ['exact']
        }