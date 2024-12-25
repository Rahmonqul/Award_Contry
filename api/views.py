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
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import *
from dj_rest_auth.views import UserDetailsView
from rest_framework.exceptions import PermissionDenied, NotFound
from django.utils import translation
from .paginator import  AwardPagination


#1-api AwardView
class AwardView(APIView):
    permission_classes = []

    accept_language_header = openapi.Parameter(
        'Accept-Language', openapi.IN_HEADER,
        description="Specify the language of the content to be returned. If not provided, the default language will be used.",
        type=openapi.TYPE_STRING
    )

    page_param = openapi.Parameter(
        'page', openapi.IN_QUERY, description="Page number (default is 1)", type=openapi.TYPE_INTEGER, default=1
    )
    page_size_param = openapi.Parameter(
        'page_size', openapi.IN_QUERY, description="Page-size", type=openapi.TYPE_INTEGER,  default=20
    )

    @swagger_auto_schema(manual_parameters=[accept_language_header, page_param, page_size_param, ])
    def get(self, request, *args, **kwargs):
        try:
            user_language = request.headers.get('Accept-Language', 'en')
            translation.activate(user_language)

            awards = Award.objects.all()

            paginator = AwardPagination()
            result_page = paginator.paginate_queryset(awards, request)
            serializer = AwardSerializer(result_page, many=True)

            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)



#2-api AwardViewDetail

class AwardDetailView(RetrieveAPIView):
    queryset = Award.objects.all()
    serializer_class = AwardDetailSerializer

    # Параметры для Swagger
    accept_language_header = openapi.Parameter(
        'Accept-Language', openapi.IN_HEADER,
        description="Specify the language of the content to be returned. If not provided, the default language will be used.",
        type=openapi.TYPE_STRING
    )

    @swagger_auto_schema(manual_parameters=[accept_language_header])
    def get(self, request, *args, **kwargs):
        user_language = request.headers.get('Accept-Language', 'en')
        translation.activate(user_language)

        try:
            instance = self.get_object()
        except Award.DoesNotExist:
            return Response({"detail": "Award not found."}, status=status.HTTP_404_NOT_FOUND)

        # Сериализация объекта
        serializer = self.get_serializer(instance)
        return Response(serializer.data)



#3-api AwardDetailYeardDecision
class AwardDetailYearDecisionAPIView(APIView):
    accept_language_header = openapi.Parameter(
        'Accept-Language', openapi.IN_HEADER,
        description="Specify the language of the content to be returned. If not provided, the default language will be used.",
        type=openapi.TYPE_STRING
    )

    page_param = openapi.Parameter(
        'page', openapi.IN_QUERY, description="Page number (default is 1)", type=openapi.TYPE_INTEGER, default=1
    )
    page_size_param = openapi.Parameter(
        'page_size', openapi.IN_QUERY, description="Page-size", type=openapi.TYPE_INTEGER,  default=20
    )

    @swagger_auto_schema(manual_parameters=[accept_language_header, page_param, page_size_param])
    def get(self, request, id, year):
        try:
            user_language = (
                    request.GET.get('lang') or
                    request.headers.get('X-Language') or
                    request.headers.get('Accept-Language', 'en')
            )
            translation.activate(user_language)

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

            decision_serializer = DecisionSerializer(result_page, many=True)

            return paginator.get_paginated_response(decision_serializer.data)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

#decision api

class DecisionUserAwardAPIView(APIView):
    accept_language_header = openapi.Parameter(
        'Accept-Language', openapi.IN_HEADER,
        description="Specify the language of the content to be returned. If not provided, the default language will be used.",
        type=openapi.TYPE_STRING
    )

    page_param = openapi.Parameter(
        'page', openapi.IN_QUERY, description="Page number (default is 1)", type=openapi.TYPE_INTEGER, default=1
    )
    page_size_param = openapi.Parameter(
        'page_size', openapi.IN_QUERY, description="Page-size", type=openapi.TYPE_INTEGER, default=20
    )

    @swagger_auto_schema(manual_parameters=[accept_language_header, page_param, page_size_param])
    def get(self, request, id, year, award_id):
        try:
            user_language = (
                    request.GET.get('lang') or
                    request.headers.get('X-Language') or
                    request.headers.get('Accept-Language', 'en')
            )
            translation.activate(user_language)

            awards = AwardPartner.objects.filter(
                decision_id=id,  # ID
                date__year=year,  # Year
                award_id=award_id  # Award Id isi
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




# 5-api search
class SearchUserApiView(ListAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerSearchSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ['full_name']

    accept_language_header = openapi.Parameter(
        'Accept-Language', openapi.IN_HEADER,
        description="Specify the language of the content to be returned. If not provided, the default language will be used.",
        type=openapi.TYPE_STRING
    )

    page_param = openapi.Parameter(
        'page', openapi.IN_QUERY,
        description="Page number (default is 1)",
        type=openapi.TYPE_INTEGER,
        default=1
    )

    page_size_param = openapi.Parameter(
        'page_size', openapi.IN_QUERY,
        description="Page size ",
        type=openapi.TYPE_INTEGER,
        default=20
    )

    @swagger_auto_schema(manual_parameters=[accept_language_header, page_param, page_size_param])
    def get(self, request, *args, **kwargs):

        search_term = self.request.query_params.get('search', '')
        lang = self.request.query_params.get('lang', 'en')

        user_language = (
            request.GET.get('lang') or
            request.headers.get('X-Language') or
            request.headers.get('Accept-Language', 'en')
        )
        translation.activate(user_language)

        queryset = self.get_queryset()

        if search_term:
            search_field = f'full_name_{lang}'
            queryset = queryset.filter(**{f'{search_field}__icontains': search_term})

        paginator = self.paginate_queryset(queryset)
        if paginator is not None:
            serializer = self.get_serializer(paginator, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class DetailUserApiView(RetrieveAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerDetailSerializer
    lookup_field = 'pk'

    accept_language_header = openapi.Parameter(
        'Accept-Language', openapi.IN_HEADER,
        description="Specify the language of the content to be returned. If not provided, the default language will be used.",
        type=openapi.TYPE_STRING
    )

    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     lang = self.request.query_params.get('lang', 'en')
    #     translation.activate(lang)
    #     context['lang'] = lang
    #     return context

    @swagger_auto_schema(manual_parameters=[accept_language_header])
    def get(self, request, *args, **kwargs):
        user_language = (
                request.GET.get('lang') or
                request.headers.get('X-Language') or
                request.headers.get('Accept-Language', 'en')
        )
        translation.activate(user_language)
        partner = self.get_object()
        serializer = self.get_serializer(partner)
        return Response(serializer.data)



class AwardPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 20

class PartnerFilterAPIView(APIView):
    accept_language_header = openapi.Parameter(
        'Accept-Language', openapi.IN_HEADER,
        description="Specify the language of the content to be returned. If not provided, the default language will be used.",
        type=openapi.TYPE_STRING
    )

    page_param = openapi.Parameter(
        'page', openapi.IN_QUERY,
        description="Page number (default is 1)",
        type=openapi.TYPE_INTEGER,
        default=1
    )

    page_size_param = openapi.Parameter(
        'page_size', openapi.IN_QUERY,
        description="Page size (default is 20, max is 20)",
        type=openapi.TYPE_INTEGER,
        default=20
    )

    @swagger_auto_schema(
        request_body=PartnerFilterRequestSerializer,
        responses={200: PartnerDetailSerializer(many=True)},
        manual_parameters=[accept_language_header, page_param, page_size_param]
    )
    def post(self, request, *args, **kwargs):

        user_language = request.META.get('HTTP_ACCEPT_LANGUAGE', 'en')
        translation.activate(user_language)
        # Десериализация тела запроса
        serializer = PartnerFilterRequestSerializer(data=request.data)
        if serializer.is_valid():
            award_ids = serializer.validated_data.get('award_ids', [])
            award_code = serializer.validated_data.get('award_code', None)
            date = serializer.validated_data.get('date', None)

            # Фильтрация по полям
            queryset = Partner.objects.all()

            if award_ids:
                queryset = queryset.filter(award_partners__award__id__in=award_ids)
            if award_code:
                queryset = queryset.filter(award_partners__award__code=award_code)
            if date:
                queryset = queryset.filter(award_partners__date=date)

            # Применяем пагинацию вручную
            paginator = AwardPagination()
            result_page = paginator.paginate_queryset(queryset, request)
            if result_page is not None:
                return paginator.get_paginated_response(PartnerDetailSerializer(result_page, many=True, context={'request': request}).data)

            # Если пагинация не требуется
            serializer = PartnerDetailSerializer(queryset, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Если данные запроса некорректны
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SocilaLinksApiView(ListAPIView):
    queryset = SocialLink.objects.all()
    serializer_class = SocialLinkSerializer


class CustomUserDetailsView(UserDetailsView):
    serializer_class = CustomUserDetailsSerializer

    def get(self, request, *args, **kwargs):
        user = self.get_object()

        return Response(self.serializer_class(user).data)



#4-api CountryAwardApiview
class CountryAwardApiview(APIView):
    accept_language_header = openapi.Parameter(
        'Accept-Language', openapi.IN_HEADER,
        description="Specify the language of the content to be returned. If not provided, the default language will be used.",
        type=openapi.TYPE_STRING
    )


    @swagger_auto_schema(manual_parameters=[accept_language_header])
    def get(self, request, *args, **kwargs):
        user_language = (
            request.GET.get('lang') or
            request.headers.get('X-Language') or
            request.headers.get('Accept-Language', 'en')
        )
        translation.activate(user_language)  # Активируем выбранный язык

        countryaward = AboutCountryAward.objects.all()

        serializer = CountryAwardSerializer(countryaward, many=True)
        response = Response(serializer.data, status=status.HTTP_200_OK)

        return response