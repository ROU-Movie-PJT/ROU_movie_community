from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Count
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from ACCOUNTS.serializers import ProfileSerializer
from .models import *
from .serializers import *

User = get_user_model()


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def index(request):
    print('a')
    if request.method == 'GET':
        # GET 요청 처리 로직
        if request.user.is_authenticated:
            answered_quizzes = UserQuizAttempt.objects.filter(
                user=request.user).values_list('quiz', flat=True)
            quizzes = Quiz.objects.exclude(id__in=answered_quizzes)
        else:
            quizzes = Quiz.objects.all()
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':

        # POST 요청 처리 로직
        if request.user.is_authenticated:
            serializer = QuizSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(write_quiz_user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "인증된 사용자만 퀴즈를 생성할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET', 'PUT', 'DELETE'])
# 인증된 사용자는 모든 요청 가능, 인증되지 않은 사용자는 GET만 가능
@permission_classes([IsAuthenticatedOrReadOnly])
def quiz_detail_or_update_or_delete(request, quiz_pk):
    quiz = get_object_or_404(pk=quiz_pk)

    def quiz_detail():
        serializer = QuizSerializer(quiz)
        return Response(serializer.data)

    def quiz_update():
        if request.user == quiz.write_quiz_user:
            serializer = QuizSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)

    def quiz_delete():
        if request.user == quiz.write_review_user:
            quiz.delete()
            data = {
                'delete': f'퀴즈 {quiz_pk}번이 삭제되었습니다.'
            }
        return Response(data, status=status.HTTP_204_NO_CONTENT)

    if request.method == 'GET':
        return quiz_detail()
    elif request.method == 'PUT':
        if request.user == quiz.write_review_user:
            return quiz_update()
    elif request.method == 'DELETE':
        if request.user == quiz.write_review_user:
            return quiz_delete()


@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def quiz_item_detail(request, quiz_pk, quiz_item_pk):
    """퀴즈 아이템 상세보기 및 관리."""
    quiz = get_object_or_404(Quiz, pk=quiz_pk)
    item = get_object_or_404(QuizItem, pk=quiz_item_pk)

    def _quiz_item_update():
        serializer = QuizItemSerializer(item, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _quiz_item_delete(request, quiz):
        if request.user != quiz.write_quiz_user and not request.user.is_superuser:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        item = get_object_or_404(
            QuizItem, pk=request.query_params.get('item_id', 0))
        item.delete()
        return Response({'delete': 'Quiz item deleted'}, status=status.HTTP_204_NO_CONTENT)

    if request.method == 'PUT':
        return _quiz_item_update(request, quiz)
    elif request.method == 'DELETE':
        return _quiz_item_delete(request, quiz)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_quiz(request, quiz_pk):
    """Processing quiz submissions."""
    quiz = get_object_or_404(Quiz, pk=quiz_pk)

    # Check if the quiz has already been attempted
    if UserQuizAttempt.objects.filter(user=request.user, quiz=quiz).exists():
        return Response({'message': 'This quiz has already been attempted.'}, status=status.HTTP_400_BAD_REQUEST)

    user_answer_id = request.data.get('user_answer')

    try:
        user_answer_item = QuizItem.objects.get(quiz=quiz, pk=user_answer_id)
        is_correct = user_answer_item.is_correct
    except QuizItem.DoesNotExist:
        return Response({'error': 'Invalid answer ID'}, status=status.HTTP_400_BAD_REQUEST)

    UserQuizAttempt.objects.create(
        user=request.user,
        quiz=quiz,
        answered_correctly=is_correct
    )

    return Response({'is_correct': is_correct})


def check_if_correct(quiz, user_answer_id):
    """Check if the user's answer is correct for the given quiz."""
    try:
        user_answer_item = QuizItem.objects.get(quiz=quiz, pk=user_answer_id)
        return user_answer_item.is_correct
    except QuizItem.DoesNotExist:
        raise ValueError("Invalid answer ID")

# @api_view(['GET'])
# @permission_classes([IsAuthenticatedOrReadOnly])
# def index(request):
#     """답변한 퀴즈 필터링하여 조회."""
#     answered_quizzes = UserQuizAttempt.objects.filter(
#         user=request.user).values_list('quiz', flat=True)
#     quizzes = Quiz.objects.exclude(id__in=answered_quizzes)
#     serializer = QuizSerializer(quizzes, many=True)
#     return Response(serializer.data)


def check_if_correct(quiz, user_answer):
    """퀴즈와 사용자의 답변을 기반으로 정답 여부를 확인합니다."""
    return quiz.correct_answer == user_answer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_quiz_attempts(request):
    """사용자의 퀴즈 시도 조회."""
    attempts = UserQuizAttempt.objects.filter(user=request.user)
    serializer = UserQuizAttemptSerializer(attempts, many=True)
    return Response(serializer.data)


# 사용자에게 자동으로 등급 부여
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_correct_quiz_count(request):
    correct_count = UserQuizAttempt.objects.filter(
        user=request.user, answered_correctly=True).count()

    user = request.user
    if correct_count >= 20:
        user.rate_image = 'https://icons8.com/icon/33486/gold-medal'
        user.rank_name = 'Gold'
        user.score = correct_count
    elif correct_count >= 10:
        user.rate_image = 'https://icons8.com/icon/23876/silver-medal'
        user.rank_name = 'Silver'
        user.score = correct_count
    else:
        user.rank_name = 'Bronze'
        user.score = correct_count
    user.save()

    serializer = ProfileSerializer(user)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def quiz_item_list_or_create(request, quiz_pk):
    quiz = get_object_or_404(Quiz, pk=quiz_pk)

    def quiz_item_list():
        serializer = QuizSerializer(quiz)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def quiz_item_create():
        if isinstance(request.data, list):
            items = []
            for item_data in request.data:
                # 'quiz' 필드를 요청 데이터에 추가합니다.
                item_data['quiz'] = quiz_pk
                item_serializer = QuizItemSerializer(data=item_data)
                if item_serializer.is_valid(raise_exception=True):
                    item = item_serializer.save()
                    items.append(item)
            return Response(QuizItemSerializer(items, many=True).data, status=status.HTTP_201_CREATED)
        else:
            # 'quiz' 필드를 단일 객체 데이터에 추가합니다.
            request.data['quiz'] = quiz_pk
            serializer = QuizItemSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

    if request.method == 'GET':
        return quiz_item_list()
    elif request.method == 'POST':
        return quiz_item_create()
