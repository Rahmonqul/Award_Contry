from django.urls import  path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns=[
    path("awards/", AwardView.as_view(), name="apiawards"),
    path("awards/<int:pk>/", AwardDetailView.as_view(), name="apidetailawards"),
    path("awards/<int:id>/<int:year>/decision/", AwardDetailYearDecisionAPIView.as_view(), name="apidecision"),
    path('decision-user/<int:id>/<int:year>/<int:award_id>/', DecisionUserAwardAPIView.as_view(), name="apidecisionuser"),
    path('search-user/', SearchUserApiView.as_view(), name='apisearchuser'),
    path('user/<int:pk>/', DetailUserApiView.as_view(), name='apidetail'),
    path('user-filter/', PartnerFilterAPIView.as_view(), name='apifilter'),
    path("social-link/", SocilaLinksApiView.as_view(), name="sociallink"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    # path('auth/dj-rest-auth/user/', CustomUserDetailsView.as_view(), name='user-details'),


]