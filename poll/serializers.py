from django.contrib.auth.models import User
from .models import Poll, Question, Answer, Report
from rest_framework import serializers

class QuestionlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'text', 'poll')


class PollSerializer(serializers.ModelSerializer):
    questions = QuestionlSerializer(many=True, read_only=True)
    
    class Meta:
        model = Poll
        fields = ('id', 'title', 'description', 'date_start', 'date_end', 'questions')


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'ans', 'question_id')


class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report
        fields = ('id', 'owner', 'poll_id', 'completed')


class ReportStartSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Report
        fields = ('id', 'owner', 'poll_id', 'answers')


class UserReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        filelds = ('id', 'reports')


class AnswersSendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'ans')
