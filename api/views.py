from rest_framework.response import Response
from rest_framework import status

from config.settings import LANGUAGES
from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from django.core.paginator import Paginator
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PartnerFilter
from .permissions import IsAuthorOrReadOnly
from rest_framework.permissions import *
from dj_rest_auth.views import UserDetailsView
from rest_framework.exceptions import PermissionDenied, NotFound
from django.utils import translation

class AwardView(APIView):
    permission_classes = []

    def get(self, request, lang, *args, **kwargs):
        try:
            if lang not in dict(LANGUAGES):
                return Response({"detail": "Invalid language code."}, status=status.HTTP_400_BAD_REQUEST)

            translation.activate(lang)

            awards = Award.objects.all()

            paginator = AwardPagination()

            result_page = paginator.paginate_queryset(awards, request)
            serializer = AwardSerializer(result_page, many=True)

            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class AwardDetailView(RetrieveAPIView):
    queryset = Award.objects.all()
    serializer_class = AwardDetailSerializer

    def get(self, request, lang, *args, **kwargs):
        if lang not in dict(LANGUAGES):
            return Response({"detail": "Invalid language code."}, status=status.HTTP_400_BAD_REQUEST)

        # Активируем указанный язык
        translation.activate(lang)

        # Получаем объект награды
        try:
            instance = self.get_object()
            print(f"Retrieved Award: {instance}")
        except Award.DoesNotExist:
            print("Award not found.")
            return Response({"detail": "Award not found."}, status=status.HTTP_404_NOT_FOUND)

        # Сериализация объекта
        serializer = self.get_serializer(instance)
        print(f"Serialized Data: {serializer.data}")
        return Response(serializer.data)



class AwardDetailYearDecisionAPIView(APIView):
    def get(self, request, id, year, lang):
        try:

            if lang not in dict(LANGUAGES):
                return Response({"detail": "Invalid language code."}, status=status.HTTP_400_BAD_REQUEST)

            translation.activate(lang)

            awards = AwardPartner.objects.filter(
                award_id=id,
                date__year=year
            )

            if not awards.exists():
                return Response(
                    {"detail": "No awards found matching the criteria."},
                    status=status.HTTP_404_NOT_FOUND
                )
            decisions = Decision.objects.filter(
                award_partners__award_id=id,
                award_partners__date__year=year
            ).distinct()

            paginator = DecisionPagination()
            result_page = paginator.paginate_queryset(decisions, request)

            # Сериализация решений с пагинацией
            decision_serializer = DecisionSerializer(result_page, many=True)

            # translation.deactivate()

            return paginator.get_paginated_response(decision_serializer.data)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class DecisionUserAwardAPIView(APIView):
    def get(self, request, id, year, award_id):
        try:
            # Фильтруем по id (решение), year (год), и award_id (ID награды)
            awards = AwardPartner.objects.filter(
                decision_id=id,  # ID решения
                date__year=year,  # Год вручения
                award_id=award_id  # ID награды
            )

            if not awards.exists():
                return Response(
                    {"detail": "No awards found matching the criteria."},
                    status=status.HTTP_404_NOT_FOUND
                )

            paginator = AwardPagination()
            result_page = paginator.paginate_queryset(awards, request)

            serializer = AwardPartnerDetailSerializer(result_page, many=True, context={'request': request})
            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            return Response(
                {"detail": f"An error occurred: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )


        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SearchUserApiView(ListAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerSearchSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ['full_name']

    def get_serializer_context(self):
        # Получаем язык из параметра URL
        lang = self.kwargs.get('lang', 'uz')  # По умолчанию 'uz', если язык не передан
        translation.activate(lang)  # Активируем язык

        context = super().get_serializer_context()
        context['lang'] = lang  # Добавляем язык в контекст для сериализатора
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        lang = self.kwargs.get('lang', 'uz')  # Получаем язык из параметра URL

        # Используем модель перевода для поля full_name, чтобы найти записи на указанном языке
        search_term = self.request.query_params.get('search', '')  # Получаем строку поиска

        if search_term:
            # Строим фильтр для поля, например, 'full_name_<lang>'
            search_field = f'full_name_{lang}'  # Имя поля для поиска в нужном языке
            queryset = queryset.filter(**{search_field + '__icontains': search_term})

        return queryset

class DetailUserApiView(ListAPIView):
    # permission_classes = [IsAuthorOrReadOnly]
    queryset = Partner.objects.all()
    serializer_class = PartnerDetailSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        lang = self.kwargs.get('lang', 'uz')
        translation.activate(lang)
        context['lang'] = lang
        return context

    def get(self, request, *args, **kwargs):
        partner = self.get_object()
        serializer = self.get_serializer(partner)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        return self.patch(request, *args, **kwargs)


class PartnerFilterAPIView(ListAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerDetailSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PartnerFilter

    def get_serializer_context(self):
        context = super().get_serializer_context()
        lang = self.kwargs.get('lang', 'uz')
        translation.activate(lang)
        context['lang'] = lang
        return context

class SocilaLinksApiView(ListAPIView):
    queryset = SocialLink.objects.all()
    serializer_class = SocialLinkSerializer


class CustomUserDetailsView(UserDetailsView):
    serializer_class = CustomUserDetailsSerializer

    def get(self, request, *args, **kwargs):
        user = self.get_object()

        return Response(self.serializer_class(user).data)


class CountryAwardApiview(APIView):


    def get(self, request, lang, *args, **kwargs):

        translation.activate(lang)


        countryaward = AboutCountryAward.objects.all()

        serializer = CountryAwardSerializer(countryaward, many=True)
        response = Response(serializer.data, status=status.HTTP_200_OK)

        # translation.deactivate()

        return response