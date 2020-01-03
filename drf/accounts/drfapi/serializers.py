from api.models import UserProfile

from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from django.contrib.auth.models import User
from django.utils import timezone

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
expiration_time = api_settings.JWT_REFRESH_EXPIRATION_DELTA


class UserSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id',
            'uri',
            'username'
    ]

    def get_uri(self, obj):
        return 'api/user/{id}'.format(id=obj.id)


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input-type": "password"}, write_only=True)
    password2 = serializers.CharField(style={"input-type": "password"}, write_only=True)
    token = serializers.SerializerMethodField(read_only=True)
    expires = serializers.SerializerMethodField(read_only=True)
    response = serializers.SerializerMethodField(read_only=True)
    message = serializers.SerializerMethodField(read_only=True)


    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'password2',
            'response',
            'expires',
            'token',
            'message'
        ]

    def get_token(self, obj):
        user = obj
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token


    def get_expires(self, data):
        return timezone.now() + expiration_time


    def get_response(self, data):
        user = data
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        context = self.context
        request = context['request']
        response = jwt_response_payload_handler(token, user=user, request=request)
        return response
    

    def get_message(self, data):
        return 'Thanks for registration. Please verify your email'


    def validate_username(self, data):
        user = User.objects.filter(username__iexact=data)
        if user.exists():
            raise serializers.ValidationError('Username already taken')
        return data


    def validate_email(self, data):
        email = User.objects.filter(email__iexact=data)
        if email.exists():
            raise serializers.ValidationError('Email already taken')
        return data

    def validate(self, data):
        password = data.get('password')
        password2 = data.pop('password2')
        if password != password2:
            raise serializers.ValidationError('Password doesnt match')
        return data


    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        password = validated_data.get('password')
        userObj = User(username=username, email=email)
        userObj.set_password(password)
        userObj.is_active=False
        userObj.save()
        return userObj
 