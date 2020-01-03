from django.urls import path, include
from .views import ListSearchAPIView, OthersAPIVIew

from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from accounts.drfapi.views import RegisterAuthAPI, AuthAPIView

app_name = 'api'

urlpatterns = [
    path('userprofile/', ListSearchAPIView.as_view(), name='list'),
    path('userprofile/<int:pk>', OthersAPIVIew.as_view(), name='update'),
    path('auth/', obtain_jwt_token, name='jwtToken'),
    path('auth-rest/', include('rest_auth.urls')),
    path('auth/refresh/', refresh_jwt_token, name='jwtRefreshToken'),
    path('auth/verify/', verify_jwt_token, name='verifyRefreshToken'),
    path('register/', RegisterAuthAPI.as_view(), name='apiRegister'),
    path('login/', AuthAPIView.as_view(), name='apiAuth')
]
