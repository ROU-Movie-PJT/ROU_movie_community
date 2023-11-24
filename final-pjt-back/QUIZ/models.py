from django.db import models
from django.conf import settings


class Quiz(models.Model):
    question = models.CharField(max_length=100)

    write_quiz_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='write_quiz')
    correct_quiz_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='correct_quiz')
    quiz_image = models.ImageField(
        upload_to='quiz_images/', blank=True, null=True)


class QuizItem(models.Model):
    quiz = models.ForeignKey(
        Quiz, related_name='items', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)


class UserQuizAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    answered_correctly = models.BooleanField(default=False)

    class Meta:
        unique_together = ['user', 'quiz']
