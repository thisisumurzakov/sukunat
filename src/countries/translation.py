from modeltranslation.translator import register, TranslationOptions
from .models import Country


@register(Country)
class CountryTranslationOptions(TranslationOptions):
    fields = ('name', 'code')
