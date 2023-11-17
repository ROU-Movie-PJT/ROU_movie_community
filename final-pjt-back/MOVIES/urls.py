from django.urls import path
from . import views

urlpatterns = [
    # TMDB 인기있는 영화
    path('api_test/TMDB_POPULAR/', views.api_test_TP),
    # TMDB 영화 장르
    path('api_test/TMDB_GENRE/', views.api_test_TG),
    path('api_test/TMDB_TRENDING/', views.api_test_TT),
]
