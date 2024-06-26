from django.urls import path
from . import views

urlpatterns = [
    # 회원 탈퇴(POST)
    path('delete/', views.delete),
    # 회원 정보 조회(GET)/수정(PUT)
    path('profile/<int:user_pk>/', views.profile),
    # 지역을 고려한 친구 추천
    path('<int:user_pk>/friend/', views.user_friend),
    # 선호, 불호 장르 조회(GET)/수정(PUT)
    path('preference/<str:pType>/', views.preference),
    # 팔로잉(POST)
    path('follow/<int:user_pk>/', views.follow),
]
