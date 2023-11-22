from django.urls import path
from . import views

app_name = 'QUIZ'


urlpatterns = [
    path('', views.index),  # 전체 문제 
    path('<int:quiz_pk>/', views.quiz_detail),  # 단일 문제 조회
    path('<int:quiz_pk>/quiz_item/', views.quiz_item_detail),  # 단일 문제 조회
    # path('/start/', views.start),  # 
    # path('/result/', views.result),  # 결과 나옴 
]
