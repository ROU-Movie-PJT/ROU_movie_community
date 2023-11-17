from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomRegisterSerializer(RegisterSerializer):
  profile_image = serializers.ImageField(use_url=True)
  region = serializers.CharField(max_length=50)

  class Meta:
    model = User
    fields = ('region', 'profile_image',)

  def get_cleaned_data(self):
    data = super().get_cleaned_data()
    data['profile_image'] = self.validated_data.get('profile_image', '')
    data['region'] = self.validated_data.get('region', '')
    return data
  