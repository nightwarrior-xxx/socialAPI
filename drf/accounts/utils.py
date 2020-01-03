from django.utils import timezone
from rest_framework_jwt.settings import api_settings


expiration_time = api_settings.JWT_REFRESH_EXPIRATION_DELTA

def jwt_response_payload_handler(token, user=None, request=None):
    return {
        "token": token,
        "user": user.username,
        "expiration_time": timezone.now() + expiration_time
    }
# class Meta:
#         model = User
#         fields = [
#             "username",
#             "email",
#             "password",
#             "password2",
#             "token",
#             "expires",
#             "response",
#             "message"

#         ]

#         extra_kwargs = {"password": {"write_only": True}}

#     def get_message(self, data):
#         return "Thanks for registering. Please verify your email to confirm your registration."

#     def get_token(self, obj):
#         user = obj
#         payload = jwt_payload_handler(user)
#         token = jwt_encode_handler(payload)
#         return token

#     def get_expires(self, data):
#         return timezone.now() + expiration_time

#     def get_response(self, data):
#         user = data
#         payload = jwt_payload_handler(user)
#         token = jwt_encode_handler(payload)
#         context = self.context
#         request = context["request"]
#         response = jwt_response_payload_handler(token, user, request=request)
#         return response

#     def validate_username(self, data):
#         qs = User.objects.filter(username__iexact=data)
#         if qs.exists():
#             raise serializers.ValidationError("Username already taken !!")
#         return data

#     def validate_email(self, data):
#         qs = User.objects.filter(email__iexact=data)
#         if qs.exists():
#             raise serializers.ValidationError("Email is already taken !!")
#         return data

#     def validate(self, data):
#         pass1 = data.get("password")
#         pass2 = data.pop("password2")
#         if pass1 != pass2:
#             raise serializers.ValidationError("Password does not match")
#         return data

#     def create(self, validated_data):
#         username = validated_data.get("username")
#         email = validated_data.get("email")
#         password = validated_data.get("password")
#         userObj = User(username=username, email=email)
#         userObj.set_password(password)
#         userObj.is_active = False
#         userObj.save()
#         return userObj