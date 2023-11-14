from django.urls import path
from . import views


app_name = 'ACCOUNTS'


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('update/', views.update, name='update'),
    path('resign/', views.resign, name='resign'),
    path('password/', views.change_password, name='change_password'),
    path('profile/<username>/', views.profile, name='profile'),
    path('<int:user_id>/follow/', views.follow, name='follow'),
    path('<int:user_id>/liked-items/', views.liked_items, name='liked_items'),
    path('<int:user_id>/followers/', views.followers, name='followers'),
    path('<int:user_id>/followings/', views.followings, name='followings'),
]