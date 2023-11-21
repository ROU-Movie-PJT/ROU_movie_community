# # from django.http import JsonResponse
# # from django.db.models import Count
# # from django.shortcuts import get_object_or_404
# # from .models import *
# # from .serializers import *
# # from rest_framework import status
# # from rest_framework.permissions import *
# # from rest_framework.response import Response
# # from rest_framework.decorators import api_view, permission_classes
# # from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# # # Create your views here.


# # # 전체 문제 
# # @api_view(['GET', 'POST'])
# # # 인증된 사용자는 모든 요청 가능, 인증되지 않은 사용자는 GET만 가능
# # @permission_classes([IsAuthenticatedOrReadOnly])
# # def index(request):
# #     pass


# # # 단일 문제 조회, 수정, 삭제 
# # def quiz_detail_update_delete(requset):
# #     pass


# # # 문제 랜덤으로 나오게함. 
# # def start(request):
# #     pass  


# # # 결과 나옴 
# # def result(resquest):
# #     pass  


# from django.shortcuts import render
# from .models import Quiz, QuizItem
# from .serializers import QuizSerializer, QuizItemSerializer
# from django.contrib.auth import get_user_model
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status

# User = get_user_model()

# @api_view(['POST'])
# def create_quiz(request):
#     # 사용자 인증 및 유효성 검사 (간소화된 예시)
#     if not request.user.is_authenticated:
#         return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

#     # 요청 데이터에서 퀴즈 정보 가져오기
#     quiz_data = request.data.get('quiz')
#     if not quiz_data:
#         return Response({"error": "No quiz data provided"}, status=status.HTTP_400_BAD_REQUEST)

#     # Quiz 인스턴스 생성
#     quiz_serializer = QuizSerializer(data=quiz_data)
#     if quiz_serializer.is_valid():
#         quiz_serializer.save(write_quiz_user=request.user)
#     else:
#         return Response(quiz_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     # QuizItem 인스턴스 생성
#     quiz_items_data = request.data.get('items', [])
#     for item_data in quiz_items_data:
#         item_data['quiz'] = quiz_serializer.instance.id
#         quiz_item_serializer = QuizItemSerializer(data=item_data)
#         if quiz_item_serializer.is_valid():
#             quiz_item_serializer.save()
#         else:
#             return Response(quiz_item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     return Response({"message": "Quiz created successfully"}, status=status.HTTP_201_CREATED)
