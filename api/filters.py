import django_filters
from .models import Partner


class PartnerFilter(django_filters.FilterSet):
    year = django_filters.NumberFilter(method='filter_by_year', label="Фильтрация по году")
    award_code = django_filters.CharFilter(field_name='award_partners__award__code', lookup_expr='exact')  # Фильтрация по коду награды
    # award_name = django_filters.CharFilter(field_name='award_partners__award__name', lookup_expr='icontains')  # Фильтрация по имени награды (поиск по подстроке)
    award_id = django_filters.NumberFilter(field_name='award_partners__award__id', lookup_expr='exact')  # Фильтрация по ID награды

    class Meta:
        model = Partner
        fields = ['year', 'award_code', 'award_id']

    def filter_by_year(self, queryset, name, value):
        return queryset.filter(award_partners__date__year=value)



