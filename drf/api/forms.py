from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['user', 'title', 'dob', 'address', 'city', 'country', 'zip', 'image']
