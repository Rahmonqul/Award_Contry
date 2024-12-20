from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from django.core.paginator import Paginator
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PartnerFilter
from .permissions import IsAuthorOrReadOnly
from dj_rest_auth.views import UserDetailsView

class AwardView(APIView):
    permission_classes = []

    def get(self, request):
        try:
            awards = Award.objects.all()

            # Создаем экземпляр пагинатора
            paginator = AwardPagination()

            # Применяем пагинацию
            result_page = paginator.paginate_queryset(awards, request)

            # Сериализация отфильтрованных данных
            serializer = AwardSerializer(result_page, many=True)

            # Возвращаем ответ с пагинацией
            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AwardDetailView(RetrieveAPIView):
    queryset = Award.objects.all()
    serializer_class = AwardDetailSerializer


class AwardDetailYearDecisionAPIView(APIView):
    def get(self, request, id, year):
        try:
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