import django_filters
from .models import Partner


class PartnerFilter(django_filters.FilterSet):
    year = django_filters.NumberFilter(method='filter_by_year', label="Фильтрация по году")
    award_code = django_filters.CharFilter(field_name='award_partners__award__code', lookup_expr='exact')  # Фильтрация по коду награды
    award_id = django_filters.NumberFilter(field_name='award_partners__award__id', lookup_expr='exact')  # Фильтрация по ID награды

    # Фильтрация по переведённым полям
    # full_name = django_filters.CharFilter(method='filter_by_full_name', label="Фильтрация по полному имени партнера")

    class Meta:
        model = Partner
        fields = ['year', 'award_code', 'award_id']

    def filter_by_year(self, queryset, name, value):
        return queryset.filter(award_partners__date__year=value)

    # def filter_by_full_name(self, queryset, name, value):
    #     # Получаем язык из контекста, по умолчанию 'uz'
    #     lang = self.request.GET.get('lang', 'uz')
    #     # Формируем имя поля с учетом языка (например, full_name_uz, full_name_en и т.д.)
    #     field_name = f'full_name_{lang}'
    #     return queryset.filter(**{field_name + '__icontains': value})


