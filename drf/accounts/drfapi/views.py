from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Q

from .serializers import UserRegisterSerializer
from .permissions import AnonymousPermission

from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings




jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
expiration_time = api_settings.JWT_REFRESH_EXPIRATION_DELTA


class AuthAPIView(APIView):
    permission_classes = [AnonymousPermission]

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({"detail": "User already authenticated", "status": 400})
        username = request.data.get("username")
        password = request.data.get("password")
        qs = User.objects.filter(
            Q(username__iexact=username) | \
            Q(email__iexact=username)
        )
        if qs.count() == 1:
            user = qs.first()
            if user.check_password(password):
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                response = jwt_response_payload_handler(token, user=user, request=request)
                return Response(response)
        return Response({"detail": "Invalid Credentials"})
        

class RegisterAuthAPI(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()
    permission_classes = [AnonymousPermission]

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}