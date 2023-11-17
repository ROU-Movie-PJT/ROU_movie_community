from django.urls import path
from . import views

urlpatterns = [
    path('api_test/TMDB_POPULAR/', views.api_test_TP),
    path('api_test/TMDB_GENRE/', views.api_test_TG),
    path('api_test/TMDB_DETAIL/', views.api_test_TD),
    path('api_test/KOBIS_DETAIL/', views.api_test_K),
]
