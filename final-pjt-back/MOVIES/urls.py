from django.urls import path
from . import views


app_name = 'MOVIES'


urlpatterns = [
    path('api_test/TMDB_GENRE/', views.api_test_TG),  # TMDB 영화 장르
    path('api_test/TMDB_TRENDING/', views.api_test_TT),  # TMDB 트렌딩
    path('api_test/TMDB_POPULAR/', views.api_test_TP),  # TMDB 인기있는 영화
    path('', views.movies_main),  # 메인 영화 조회
    path('<int:sort_num>/sort/', views.movie_sort),  # 필터링된 영화 정보(장르 포함)
    path('<int:movie_pk>/', views.movie_detail),  # 단일 영화 조회
    # path('<int:movie_pk>/review/', views.movie_review),  # 영화별 게시글 조회
    # 영화 좋아요 등록 및 해제(좋아요 수까지 출력)
    path('<int:movie_pk>/like/', views.movie_like),
    # 영화 싫어요 등록 및 해제(싫어요 수까지 출력)
    path('<int:movie_pk>/dislike/', views.movie_dislike),
    # 시청 중인 영화 등록 및 해제(시청 수까지 출력)
    path('<int:movie_pk>/watching/', views.movie_watching),
    # 찜한 영화 등록 및 해제(찜한 수까지 출력)
    path('<int:movie_pk>/favorite/', views.movie_favorite),
    path('trend/', views.movie_trend),  # 박스오피스 인기 영화 조회
    path('<int:genre_id>/genre/', views.movie_genre),  # 장르별 추천 영화 조회
    # path('recommend/the_best_movie/', views.best_movie),  # 역대급 영화
    # path('recommend/for_weather/', views.for_weather),  # 날씨별 추천 영화
]
