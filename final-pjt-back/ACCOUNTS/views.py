from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
def delete(request):
  request.user.delete()
  return Response({'message':f'사용자 {request.user} 탈퇴 완료!'}, status=status.HTTP_204_NO_CONTENT)