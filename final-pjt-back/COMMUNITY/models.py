# from django.db import models
# from django.conf import settings

# class Review(models.Model):
#     title = models.CharField(max_length=100)
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     # 게시글이 달린 영화
#     write_review_movie = models.ForeignKey('movies.Movie', on_delete=models.CASCADE, related_name='write_movie_review', null=True, blank=True)
#     # 게시글을 작성한 사용자
#     write_review_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='write_review') 
#     # 게시글을 좋아요한 사용자
#     like_review_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_reviews')


# class Comment(models.Model):
#     content = models.CharField(max_length=20)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     # 댓글 작성자
#     write_comment_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='write_comment')
#     # 상위 댓글
#     super_comment = models.ForeignKey('self', on_delete=models.CASCADE, related_name='commented', null=True, blank=True)
#     # 댓글을 좋아요한 사용자
#     like_comment_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_comments')
#     # 댓글이 달린 리뷰글
#     commented_review= models.ForeignKey(Review, on_delete=models.CASCADE, related_name='review_comment')

