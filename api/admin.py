from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

@admin.register(Partner)
class PartnerAdmin(UserAdmin):
    model = Partner
    list_display = ["username",  "email", "position", "is_staff"]
    search_fields = ["username", "email", "full_name"]
    ordering = ["username"]

    # Поля для добавления нового пользователя
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("full_name", "image", "biography", "position")}),
    )

    # Поля для отображения в админке
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("full_name", "image", "biography", "position")}),
    )

admin.site.register(Award)
admin.site.register(AwardPartner)
admin.site.register(Decision)
admin.site.register(SocialLink)