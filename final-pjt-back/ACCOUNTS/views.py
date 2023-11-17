from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import ProfileSerializer

User = get_user_model()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete(request):
  request.user.delete()
  return Response({'message':f'사용자 {request.user} 탈퇴 완료!'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile(request, user_pk):
  user = get_object_or_404(User, pk=user_pk)
  if request.method == 'GET':
    serializer = ProfileSerializer(user)
    return Response(serializer.data)
  elif request.method == 'PUT':
    if request.user == user:
      serializer = ProfileSerializer(instance=user, data=request.data, partial=True)
      if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)