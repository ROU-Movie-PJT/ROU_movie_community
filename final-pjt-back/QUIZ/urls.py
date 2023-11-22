from django.urls import path
from . import views

app_name = 'QUIZ'


urlpatterns = [
    path('', views.index),  # 모든 퀴즈 조회
    path('<int:quiz_pk>/', views.quiz_detail),  # 단일 퀴즈 조회/관리
    path('<int:quiz_pk>/quiz_item/', views.quiz_item_detail),  # 퀴즈 아이템 관리
    path('<int:quiz_pk>/submit/', views.submit_quiz),  # 퀴즈 답변 제출
    path('user_correct_quiz_count/', views.user_correct_quiz_count),  # 사용자의 정답 수 확인
]
