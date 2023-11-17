from django.urls import path
from . import views

urlpatterns = [
    # 회원 탈퇴(POST)
    path('delete/', views.delete),
    # 회원 정보 조회(GET)/수정(PUT)
    path('profile/<int:user_pk>/', views.profile),
]