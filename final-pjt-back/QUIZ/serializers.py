from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()


class QuizItemSerializer(serializers.ModelSerializer):
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('pk', 'username',)

    write_quiz_item_user = UserSerializer(read_only=True)

    class Meta:
        model = QuizItem
        fields = '__all__'


class QuizSerializer(serializers.ModelSerializer):
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('pk', 'username',)

    write_quiz_user = UserSerializer(read_only=True)
    items = QuizItemSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = "__all__"
        depth = 1


class UserQuizAttemptSerializer(serializers.ModelSerializer):
    quiz = QuizSerializer(read_only=True)  # 퀴즈에 대한 정보를 포함
    user = serializers.StringRelatedField(
        read_only=True)  # 사용자 이름 또는 기타 문자열 표현

    class Meta:
        model = UserQuizAttempt
        fields = ['user', 'quiz', 'answered_correctly']
