from django.urls import path
from . import views


app_name = 'MOVIES'


urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_pk>/', views.detail, name='detail'),
    path('recommended/', views.recommended, name='index'),
    path('api_test/', views.api_test),
]
