from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db.models import Count

User = get_user_model()


# check_if_correct 함수 정의
def check_if_correct(quiz, user_answer):
    # 이 함수는 퀴즈와 사용자의 답변을 기반으로 정답 여부를 확인합니다.
    # 예시 로직: quiz.correct_answer와 user_answer를 비교
    return quiz.correct_answer == user_answer


# 전체 퀴즈 조회
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def index(request):
    if request.user.is_authenticated:
        answered_quizzes = UserQuizAttempt.objects.filter(
            user=request.user).values_list('quiz', flat=True)
        quizzes = Quiz.objects.exclude(id__in=answered_quizzes)
    else:
        quizzes = Quiz.objects.all()

    serializer = QuizSerializer(quizzes, many=True)
    return Response(serializer.data)

# 단일 퀴즈 조회 및 관리


@api_view(['GET', 'PUT', 'DELETE', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def quiz_detail(request, quiz_pk):
    quizzes = Quiz.objects.annotate(
        correct_count=Count('correct_quiz_users', distinct=True))
    quiz = get_object_or_404(quizzes, pk=quiz_pk)

    def quiz_detail():
        serializer = QuizSerializer(quiz)
        return Response(serializer.data)

    def quiz_create():
        quiz = Quiz(question=request.data.get('question'))
        quiz.write_quiz_user = request.user  # Currently logged in user
        quiz.save()

        items_data = request.data.get('items')
        if items_data:
            for item_data in items_data:
                QuizItem.objects.create(quiz=quiz, **item_data)

        serializer = QuizSerializer(quiz)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def quiz_update():
        serializer = QuizSerializer(quiz, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            items_data = request.data.get('items')
            if items_data:
                quiz.items.all().delete()
                for item_data in items_data:
                    QuizItem.objects.create(quiz=quiz, **item_data)
            return Response(serializer.data)

    def quiz_delete():
        quiz.delete()
        data = {'delete': f'퀴즈 {quiz_pk}번이 삭제되었습니다.'}
        return Response(data, status=status.HTTP_204_NO_CONTENT)

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
        return Response(serializer.data)


# 시도를 기록하기 위해 보기 업데이트
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_quiz(request, quiz_pk):
    quiz = get_object_or_404(Quiz, pk=quiz_pk)

    # 이미 시도한 퀴즈인지 확인
    if UserQuizAttempt.objects.filter(user=request.user, quiz=quiz).exists():
        return Response({'message': '이미 시도한 퀴즈입니다'}, status=status.HTTP_400_BAD_REQUEST)

    user_answer = request.data.get('user_answer')

    try:
        is_correct = check_if_correct(quiz, user_answer)
    except Exception as e:
        # 오류 처리
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    UserQuizAttempt.objects.create(
        user=request.user,
        quiz=quiz,
        answered_correctly=is_correct
    )

    return Response({'is_correct': is_correct})


# 답변한 퀴즈를 필터링하기 위해 뷰 업데이트
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def index(request):
    answered_quizzes = UserQuizAttempt.objects.filter(
        user=request.user).values_list('quiz', flat=True)
    quizzes = Quiz.objects.exclude(id__in=answered_quizzes)
    serializer = QuizSerializer(quizzes, many=True)
    return Response(serializer.data)


# 정답 개수 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_correct_quiz_count(request):
    correct_count = UserQuizAttempt.objects.filter(
        user=request.user, answered_correctly=True).count()
    return Response({'correct_quiz_count': correct_count})
