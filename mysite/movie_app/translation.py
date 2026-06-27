from .models import Genre, Country, Film, Series, Season, Cartoon
from modeltranslation.translator import TranslationOptions,register

@register(Genre)
class GenreTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Country)
class CountryTranslationOptions(TranslationOptions):
    fields = ('country',)

@register(Film)
class FilmTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(Series)
class SeriesTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(Season)
class SeasonTranslationOptions(TranslationOptions):
    fields = ('title', )

@register(Cartoon)
class CartoonTranslationOptions(TranslationOptions):
    fields = ('title', 'description')







