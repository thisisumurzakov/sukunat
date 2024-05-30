from modeltranslation.translator import register, TranslationOptions
from .models import Category, Article


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(Article)
class ArticleTranslationOptions(TranslationOptions):
    fields = ("title", "description")
