# from django.http import JsonResponse
# from django.db.models import Count
# from django.shortcuts import get_object_or_404
# from .models import *
# from .serializers import *
# from rest_framework import status
# from rest_framework.permissions import *
# from rest_framework.response import Response
# from rest_framework.decorators import api_view, permission_classes
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# # Create your views here.


# # 전체 문제 
# @api_view(['GET', 'POST'])
# # 인증된 사용자는 모든 요청 가능, 인증되지 않은 사용자는 GET만 가능
# @permission_classes([IsAuthenticatedOrReadOnly])
# def index(request):
#     pass


# # 단일 문제 조회, 수정, 삭제 
# def quiz_detail_update_delete(requset):
#     pass


# # 문제 랜덤으로 나오게함. 
# def start(request):
#     pass  


# # 결과 나옴 
# def result(resquest):
#     pass  
