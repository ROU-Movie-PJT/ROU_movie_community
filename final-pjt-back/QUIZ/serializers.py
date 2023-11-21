# from rest_framework import serializers
# from .models import Quiz, QuizItem

# class QuizItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = QuizItem
#         fields = '__all__'

# class QuizSerializer(serializers.ModelSerializer):
#     items = QuizItemSerializer(many=True, read_only=True)

#     class Meta:
#         model = Quiz
#         fields = "__all__"
#         depth = 1
