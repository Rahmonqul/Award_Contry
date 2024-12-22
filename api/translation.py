# myapp/translation.py
from modeltranslation.translator import translator, TranslationOptions
from .models import Partner, Award, SocialLink, AboutCountryAward, Decision

# class PartnerTranslationOptions(TranslationOptions):
#     fields = ('full_name', 'biography', 'position')  # Добавляем нужные поля

class AwardTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

class SocialLinkTranslationOptions(TranslationOptions):
    fields = ('name',)

class AboutCountryAwardTranslationOptions(TranslationOptions):
    fields = ('text',)

class DecisionTranslationOptions(TranslationOptions):
    fields = ('name',)

# Регистрация переводов
# translator.register(Partner, PartnerTranslationOptions)
translator.register(Award, AwardTranslationOptions)
translator.register(SocialLink, SocialLinkTranslationOptions)
translator.register(AboutCountryAward, AboutCountryAwardTranslationOptions)
translator.register(Decision, DecisionTranslationOptions)
