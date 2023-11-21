from django.db import models
from django.conf import settings

class Quiz(models.Model):
    # 퀴즈의 질문 또는 설명
    question = models.CharField(max_length=100)

    # 퀴즈를 작성한 사용자
    write_quiz_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='write_quiz')

    # 퀴즈를 맞춘 사용자
    correct_quiz_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='correct_quiz')

    # 퀴즈 관련 이미지 
    quiz_image = models.ImageField(upload_to='quiz_images/', blank=True, null=True)


class QuizItem(models.Model):
    # Quiz 모델과의 관계 설정
    quiz = models.ForeignKey(
        Quiz, related_name='items', on_delete=models.CASCADE
    )

    # 각 선택지의 내용
    content = models.TextField()

    # 정답 여부
    is_answer = models.BooleanField(default=False)


