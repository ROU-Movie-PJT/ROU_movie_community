from django.shortcuts import render
from .models import *
from .serializers import *
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import *
from django.db.models import Count
from django.shortcuts import get_object_or_404
User = get_user_model()

# 전체 퀴즈 조회
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def index(request):
    quizzes = Quiz.objects.all()
    serializer = QuizSerializer(quizzes, many=True)
    return Response(serializer.data)


# 단일 퀴즈 조회
@api_view(['GET', 'PUT', 'DELETE', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def quiz_detail(request, quiz_pk):
    quizzes = Quiz.objects.annotate(correct_count=Count('correct_quiz_users', distinct=True))

    quiz = get_object_or_404(quizzes, pk=quiz_pk)

    if request.method == 'GET':
        return quiz_detail()
    elif request.method == 'POST':
        return quiz_create()
    elif request.method == 'PUT':
        if request.user == quiz.write_quiz_user:
            return quiz_update()
    elif request.method == 'DELETE':
        if request.user == quiz.write_quiz_user:
            return quiz_delete()

    def quiz_detail():
        serializer = QuizSerializer(quiz)
        return Response(serializer.data)
    
    def quiz_create():
        serializer = QuizSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        
    def quiz_update():
        if request.user == quiz.write_quiz_user:
            serializer = QuizSerializer(quiz, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)

    def quiz_delete():
        if request.user == quiz.write_quiz_user:
            quiz.delete()
            data = {
                'delete': f'퀴즈 {quiz_pk}번이 삭제되었습니다.'
            } 
        return Response(data, status=status.HTTP_204_NO_CONTENT)  

# 퀴즈 아이템 view 작성
@api_view(['GET', 'PUT', 'DELETE', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def quiz_item_detail(request, quiz_pk):
    quiz = get_object_or_404(Quiz, pk=quiz_pk)            
    
    if request.method == 'GET':
        return quiz_detail()
    elif request.method == 'POST':
        return quiz_create()
    elif request.method == 'PUT':
        if request.user == quiz.write_quiz_user:
            return quiz_update()
    elif request.method == 'DELETE':
        if request.user == quiz.write_quiz_user:
            return quiz_delete()
        
    def quiz_item_list():
        serializer = QuizSerializer(quiz)
        return Response(serializer.data, )
            