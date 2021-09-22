from django.db import models
from django.contrib.auth.models import User


class Poll(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    date_start = models.DateTimeField(auto_now_add=True)
    date_end =  models.DateTimeField(null=True, blank=True, editable=False)


class Question(models.Model):
    text = models.CharField(max_length=120)
    poll = models.ForeignKey('Poll', related_name='questions', on_delete=models.CASCADE)


class Report(models.Model):
    owner = models.ForeignKey(User, related_name='reports', on_delete=models.CASCADE, default=None, null=True)
    poll_id = models.ForeignKey('Poll', on_delete=models.CASCADE, null=False)
    completed = models.BooleanField(default=False, editable=False)


class Answer(models.Model):
    ans = models.CharField(max_length=120, default=None)
    question_id = models.ForeignKey('Question', related_name='answers', on_delete=models.CASCADE)
    report_id = models.ForeignKey('Report', related_name='answers', on_delete=models.CASCADE)