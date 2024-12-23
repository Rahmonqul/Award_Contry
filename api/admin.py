from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from modeltranslation.admin import TranslationAdmin
from .models import *
from modeltranslation.translator import translator, TranslationOptions


# Регистрация моделей
# admin.site.register(Award)
admin.site.register(AwardPartner)
# admin.site.register(Decision)
admin.site.register(SocialLink)
# admin.site.register(AboutCountryAward)

# Регистрация переводов для модели Partner
class PartnerTranslationOptions(TranslationOptions):
    fields = ('full_name', 'biography', 'position')

translator.register(Partner, PartnerTranslationOptions)


@admin.register(Partner)
class PartnerAdmin(TranslationAdmin,UserAdmin):

    model = Partner

    # Поля для отображения в админке
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("full_name", "image", "biography", "position")}),
    )
    class Media:
            js = (
                'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
                'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
                'modeltranslation/js/tabbed_translation_fields.js',
            )
            css = {
                'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
            }
