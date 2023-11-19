from django.urls import path
from . import views

urlpatterns = [
    # 회원 탈퇴(POST)
    path('delete/', views.delete),
    # 회원 정보 조회(GET)/수정(PUT)
    path('profile/<int:user_pk>/', views.profile),
    # 선호, 불호 장르 조회(GET)/수정(PUT)/그 수 출력
    path('preference/<str:pType>/', views.preference),
    # 팔로잉(POST)
    path('follow/<int:user_pk>/', views.follow),
    # 팔로우 조회(GET)
    path('follow/<int:user_pk>/list/', views.follow_list),
    # 지역을 고려한 친구 추천
    path('<int:user_pk>/friend/', views.user_friend),
    # 싫어하는 장르 조회
    path('<int:user_pk>/hate_genre/', views.hate_genre_list),
    # 싫어하는 장르 등록 및 해제
    path('<int:user_pk>/hate_genre/<int:genre_pk>/',
         views.hate_genre_update_or_delete),
]
