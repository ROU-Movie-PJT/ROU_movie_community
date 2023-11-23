from rest_framework import serializers
from .models import *

class QuizItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizItem
        fields = '__all__'

class QuizSerializer(serializers.ModelSerializer):
    items = QuizItemSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = "__all__"
        depth = 1


class UserQuizAttemptSerializer(serializers.ModelSerializer):
    quiz = QuizSerializer(read_only=True)  # 퀴즈에 대한 정보를 포함
    user = serializers.StringRelatedField(read_only=True)  # 사용자 이름 또는 기타 문자열 표현

    class Meta:
        model = UserQuizAttempt
        fields = ['user', 'quiz', 'answered_correctly']