from django.db import models
from django.contrib.auth.models import User


class Poll(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    date_start = models.DateTimeField(auto_now_add=True)
    date_end = models.DateTimeField(null=True, blank=True)


class Question(models.Model):

    Question_choices = (
        (1, 1),
        (2, 2),
        (3, 3),
    )
    poll_id = models.ForeignKey(
        'Poll', on_delete=models.CASCADE, null=False, default=None)
    type = models.IntegerField(choices=Question_choices, default=1)
    question = models.CharField(max_length=200, null=True)


class Question_choice(models.Model):
    # words - выбор ответа
    words = models.CharField(max_length=120)
    question_id = models.ForeignKey(
        'Question', related_name='chooses', on_delete=models.CASCADE, default=None)


class Report(models.Model):
    owner = models.ForeignKey(
        User, related_name='reports', on_delete=models.CASCADE, default=None, null=True)
    poll_id = models.ForeignKey(
        'Poll', on_delete=models.CASCADE, null=False, default=None)
    completed = models.BooleanField(default=False)


class Answer(models.Model):
    ans = models.CharField(max_length=500, default=None)
    question = models.ForeignKey(
        'Question', related_name='answers', on_delete=models.CASCADE)
    report_id = models.ForeignKey(
        'Report', related_name='answers', on_delete=models.CASCADE)
