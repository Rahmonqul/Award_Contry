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
            if lang not in dict(LANGUAGES):  # Проверяем, что переданный язык допустим
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
            # Проверка валидности кода языка
            if lang not in dict(LANGUAGES):
                return Response({"detail": "Invalid language code."}, status=status.HTTP_400_BAD_REQUEST)

            # Активируем указанный язык
            translation.activate(lang)

            # Фильтруем записи AwardPartner по награде и году
            awards = AwardPartner.objects.filter(
                award_id=id,
                date__year=year
            )

            if not awards.exists():
                return Response(
                    {"detail": "No awards found matching the criteria."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Получаем уникальные решения, связанные с наградой
            decisions = Decision.objects.filter(
                award_partners__award_id=id,
                award_partners__date__year=year
            ).distinct()

            # Применяем пагинацию
            paginator = DecisionPagination()
            result_page = paginator.paginate_queryset(decisions, request)

            # Сериализация решений с пагинацией
            decision_serializer = DecisionSerializer(result_page, many=True)

            # Деактивация перевода после ответа
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

            # Используем пагинатор
            paginator = AwardPagination()
            result_page = paginator.paginate_queryset(awards, request)

            # Сериализация наград с пагинацией
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


class DetailUserApiView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Partner.objects.all()
    serializer_class = PartnerDetailSerializer

    def get(self, request, *args, **kwargs):
        partner = self.get_object()  # Получаем объект партнера по id
        serializer = self.get_serializer(partner)
        return Response(serializer.data)


# class DetailUserApiView(APIView):
#     permission_classes = [IsAuthorOrReadOnly]
#
#     def get_queryset(self):
#         return Partner.objects.all()
#
#     def get_object(self, pk):
#         try:
#             return self.get_queryset().get(pk=pk)
#         except Partner.DoesNotExist:
#             raise NotFound({"detail": "Partner not found."})
#
#     def get(self, request, *args, **kwargs):
#         partner = self.get_object(kwargs['pk'])
#         serializer = PartnerDetailSerializer(partner, context={'request': request})  # Передаем request
#         return Response(serializer.data)
#
#     def patch(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return Response({"detail": "Authentication credentials were not provided."}, status=401)
#
#         partner = self.get_object(kwargs['pk'])
#
#         # Проверяем, что ID партнера совпадает с ID текущего пользователя
#         if partner.user.id != request.user.id:
#             raise PermissionDenied({"detail": "You do not have permission to modify this data."})
#
#         serializer = PartnerDetailSerializer(partner, data=request.data, partial=True, context={'request': request})  # Передаем request
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)

    def put(self, request, *args, **kwargs):
        return self.patch(request, *args, **kwargs)

class PartnerFilterAPIView(ListAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerDetailSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PartnerFilter  # Применяем фильтр


class SocilaLinksApiView(ListAPIView):
    queryset = SocialLink.objects.all()
    serializer_class = SocialLinkSerializer


class CustomUserDetailsView(UserDetailsView):
    serializer_class = CustomUserDetailsSerializer

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        # Дополнительная логика, если нужно
        return Response(self.serializer_class(user).data)


class CountryAwardApiview(APIView):


    def get(self, request, lang, *args, **kwargs):
        # Активируем язык из URL
        translation.activate(lang)

        # Получаем все статьи
        countryaward = AboutCountryAward.objects.all()
        # Сериализуем статьи
        serializer = CountryAwardSerializer(countryaward, many=True)
        response = Response(serializer.data, status=status.HTTP_200_OK)

        # translation.deactivate()

        return response