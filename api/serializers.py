from .models import *
from rest_framework.serializers import ListField, DateField, ModelSerializer, SerializerMethodField, IntegerField, CharField,Serializer
from .paginator import *
from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.utils.translation import get_language
# from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['name'] = user.first_name
        token['username']=user.username

        return token

#1-apiga serializer
class AwardSerializer(ModelSerializer):
    name = SerializerMethodField()
    partner_count=SerializerMethodField()
    class Meta:
        model = Award
        fields = ['id', 'name', 'image', 'code', 'partner_count']

    def get_name(self, obj):
        language = get_language()
        return getattr(obj, f'name_{language}', obj.name)

    def get_partner_count(self, obj):
        return  AwardPartner.objects.filter(award=obj).count()

# Partner api uchun serializer

class PartnerSerializer(ModelSerializer):
    count_award = SerializerMethodField()
    fio = CharField(source='full_name')
    image = SerializerMethodField()

    class Meta:
        model = Partner
        fields = ['id','fio', 'image', 'count_award']

    def get_image(self, obj):

        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

    def get_count_award(self, obj):
        return AwardPartner.objects.filter(partner=obj).count()

#2-api ga serializer
class AwardDetailSerializer(ModelSerializer):
    partners = SerializerMethodField()
    partner_count = SerializerMethodField()
    name = SerializerMethodField()
    description = SerializerMethodField()

    class Meta:
        model = Award
        fields = ['id', 'name', 'image', 'description', 'partner_count', 'partners']

    def get_partners(self, obj):

        award_partners = AwardPartner.objects.filter(award=obj).select_related('partner')
        partners = [ap.partner for ap in award_partners]
        return PartnerSerializer(partners, many=True, context=self.context).data

    def get_partner_count(self, obj):
        return AwardPartner.objects.filter(award=obj).count()

    def get_name(self, obj):
        language = get_language()
        return getattr(obj, f'name_{language}', obj.name)

    def get_description(self, obj):
        language = get_language()
        return getattr(obj, f'description_{language}', obj.description)




class AwardPartnerSerializer(ModelSerializer):
    class Meta:
        model = AwardPartner
        fields = ['id','award_id', 'decision_id', 'date', 'partner_id']


#3-apiga serializer
class DecisionSerializer(ModelSerializer):
    count=SerializerMethodField()
    class Meta:
        model=Decision
        fields=['id', 'name', 'link', 'count']

    def get_count(self, obj):
        return AwardPartner.objects.filter(decision=obj).count()



class AwardPartnerDetailSerializer(ModelSerializer):
    partner = PartnerSerializer()
    award = AwardSerializer()
    decision = SerializerMethodField()

    class Meta:
        model = AwardPartner
        fields = ['id', 'award', 'decision', 'date', 'partner']

    def get_decision(self, obj):
        if obj.decision:
            return {
                "id": obj.decision.id,
                "name": obj.decision.name,
                "link": obj.decision.link,
            }
        return None


# class AwardPartnerDetailSerializer(ModelSerializer):
#     partner = PartnerSerializer()
#     award=AwardSerializer()
#
#     class Meta:
#         model = AwardPartner
#         fields = ['id','award', 'decision_id', 'date', 'partner']  # Поле


class PartnerSearchSerializer(ModelSerializer):
    count_award = SerializerMethodField()
    fio = CharField(source='full_name')
    image = SerializerMethodField()
    awards = SerializerMethodField()

    class Meta:
        model = Partner
        fields = ['id', 'fio', 'image', 'biography', 'position', 'count_award', 'awards']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

    def get_count_award(self, obj):
        return obj.award_partners.count()

    def get_awards(self, obj):
        awards = Award.objects.filter(award_partners__partner=obj)
        paginator = AwardPagination()
        result_page = paginator.paginate_queryset(awards, self.context['request'])
        return paginator.get_paginated_response(AwardSerializer(result_page, many=True, context=self.context).data).data

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     lang = self.context.get('lang', 'en')
    #
    #     for field in ['fio', 'biography', 'position']:
    #         translated_field = f'{field}_{lang}'
    #         if hasattr(instance, translated_field):
    #             representation[field] = getattr(instance, translated_field)
    #
    #     return representation

class PartnerDetailSerializer(ModelSerializer):
    count_award = SerializerMethodField()
    fio = CharField(source='full_name')
    image = SerializerMethodField()
    awards = SerializerMethodField()

    class Meta:
        model = Partner
        fields = ['id', 'fio', 'image', 'biography', 'position', 'count_award', 'awards']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

    def get_count_award(self, obj):
        return obj.award_partners.count()

    def get_awards(self, obj):

        awards = Award.objects.filter(award_partners__partner=obj)

        paginator = AwardPagination()
        result_page = paginator.paginate_queryset(awards, self.context['request'])
        return paginator.get_paginated_response(AwardSerializer(result_page, many=True, context=self.context).data).data


    def get_position(self, obj):
        language = get_language()
        return getattr(obj, f'text_{language}', obj.position)
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #
    #     lang = self.context.get('lang', 'en')
    #     for field in ['fio', 'biography', 'position']:
    #         translated_field = f'{field}_{lang}'
    #         if hasattr(instance, translated_field):
    #             representation[field] = getattr(instance, translated_field)
    #
    #     return representation

class PartnerFilterRequestSerializer(Serializer):
    award_ids = ListField(
        child=IntegerField(),
        required=False,
        allow_empty=True,
        label="List of award IDs"
    )
    award_code = CharField(required=False, label="Award Code")
    date=DateField(required=False, label="Date (e.g., YYYY-MM-DD)", input_formats=['%Y-%m-%d'])


class AwardPartnerFilterSerializer(ModelSerializer):
    fio = SerializerMethodField()
    owner_image = SerializerMethodField()
    awards = SerializerMethodField()

    class Meta:
        model = AwardPartner
        fields = ['id','fio', 'owner_image', 'awards']

    def get_fio(self, obj):
        return obj.partner.full_name

    def get_owner_image(self, obj):

        if obj.partner.image:
            return obj.partner.image.url
        return None

    def get_awards(self, obj):
        return {
            "name": obj.award.name,
            "image": obj.award.image.url if obj.award.image else None,
            "date_awarded": obj.date.strftime('%Y-%m-%d'),
        }

class SocialLinkSerializer(ModelSerializer):
    class Meta:
        model=SocialLink
        fields=['name','link', 'icon']


class CustomUserDetailsSerializer(UserDetailsSerializer):
    partner_info = CharField(source='partner.full_name', read_only=True)

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ('partner_info',)


class CountryAwardSerializer(ModelSerializer):
    text = SerializerMethodField()
    class Meta:
        model = AboutCountryAward
        fields = ['id','text']

    def get_text(self, obj):
        language = get_language()
        return getattr(obj, f'text_{language}', obj.text)
