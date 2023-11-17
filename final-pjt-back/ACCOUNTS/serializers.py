from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth import get_user_model
from MOVIES.models import Genre

User = get_user_model()

class CustomRegisterSerializer(RegisterSerializer):
  region = serializers.CharField(max_length=50)
  birth = serializers.DateField()
  class Meta:
    model = User
    fields = ('region', 'birth',)

  def get_cleaned_data(self):
    data = super().get_cleaned_data()
    data['region'] = self.validated_data.get('region', '')
    data['birth'] = self.validated_data.get('birth', '')
    return data
  
# class ProfileSerializer(UserDetailsSerializer):
#   class GenreSerializer(serializers.ModelSerializer):
#     class Meta:
#       model = Genre
#       fields = '__all__'

#   class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#       model = User
#       fields = ('id',)

#   hate_genres = GenreSerializer(many=True, read_only=True)
#   like_genres = GenreSerializer(many=True, read_only=True)
#   followers = UserSerializer(many=True)

#   class Meta:
#     model = User
#     fields = ('id', 'followers', 'username', 'profile_image', 'region', 'followings', 'hate_genres', 'like_genres', 'birth')