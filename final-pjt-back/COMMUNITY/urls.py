# from django.urls import path
# from . import views

# app_name = 'COMMUNITY'
# urlpatterns = [
#     # review
#     path('', views.review_list_or_create), # 전체 게시글 목록 조회 및 영화를 선택하지 않은 게시글 생성
#     path('<int:sort_num>/sort/', views.review_sort), # 필터링된 게시글 정보(최신순, 좋아요, 댓글 많은 순)
#     path('<int:movie_pk>/review/', views.review_create_with_movie),# 영화를 선택한 게시글 생성
#     path('<int:review_pk>/', views.review_detail_or_update_or_delete), # 단일 게시글 조회, 수정, 삭제
#     path('<int:review_pk>/like/', views.review_like), # 게시글 좋아요 등록 및 해제
#     #
#     # comment
#     path('<int:review_pk>/comment/', views.comment_list_or_create), # 게시글 별 댓글 조회 및 최상위 댓글 생성
#     path('<int:review_pk>/comment/<int:comment_pk>/', views.comment_update_or_delete), # 대댓글 생성 및 전체 댓글 수정 및 삭제
#     path('<int:review_pk>/like/<int:comment_pk>/', views.comment_like),# 댓글 좋아요 등록 및 해제
#     path('<int:review_pk>/like_count/<int:comment_pk>/', views.comment_like_count), # 댓글 별 좋아요 개수 조회
# ]    