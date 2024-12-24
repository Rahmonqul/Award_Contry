# myapp/translation.py
from modeltranslation.translator import translator, TranslationOptions
from .models import Partner, Award, SocialLink, AboutCountryAward, Decision, AwardPartner
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin


class AwardTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

# class SocialLinkTranslationOptions(TranslationOptions):
#     fields = ('name',)

class AboutCountryAwardTranslationOptions(TranslationOptions):
    fields = ('text',)

class DecisionTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(Award, AwardTranslationOptions)
# translator.register(SocialLink, SocialLinkTranslationOptions)
translator.register(AboutCountryAward, AboutCountryAwardTranslationOptions)
translator.register(Decision, DecisionTranslationOptions)


class AwardAdmin(TranslationAdmin):
    model = Award
    # list_display = ('name', 'description')  # Отображение переведенных полей

    # Добавление Media для использования вкладок
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',  # Скрипт для вкладок
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),  # Стили для вкладок
        }
class DecisionAdmin(TranslationAdmin):
    model = Decision
    # list_display = ('name',)  # Отображение переведенных полей

    # Добавление Media для использования вкладок
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',  # Скрипт для вкладок
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),  # Стили для вкладок
        }

class AboutCountryAwardAdmin(TranslationAdmin):
    model = AboutCountryAward
    # list_display = ('text',)  # Отображение переведенных полей

    # Добавление Media для использования вкладок
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',  # Скрипт для вкладок
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),  # Стили для вкладок
        }
# Регистрируем модели в админке
admin.site.register(Award, AwardAdmin)
admin.site.register(AboutCountryAward, AboutCountryAwardAdmin)
admin.site.register(Decision, DecisionAdmin)

