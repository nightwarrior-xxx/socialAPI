from rest_framework import serializers
from api.models import UserProfile

from accounts.drfapi.serializers import UserSerializer

class UserProfileSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'user',
            'uri',
            'title',
            'dob',
            'address',
            'city',
            'zip',
            'country'
        ]

    def get_uri(self, obj):
        return '/api/userprofile/{id}'.format(id=obj.id)
