from django.contrib.auth.models import User
from .models import Poll, Question, Answer, Report, Question_choice
from rest_framework import serializers


class QuestionTypeslSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question_choice
        fields = ('id', 'words')


class QuestionlSerializer(serializers.ModelSerializer):
    text = serializers.ListSerializer(child=serializers.CharField())

    class Meta:
        model = Question
        fields = ('id', 'type', 'poll_id', 'text')


class PollSerializer(serializers.ModelSerializer):
    questions = QuestionlSerializer(many=True, read_only=True)
    date_end = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Poll
        fields = ('id', 'title', 'description',
                  'date_start', 'date_end', 'questions')


class AnswerSerializer(serializers.ModelSerializer):
    question = QuestionlSerializer()

    class Meta:
        model = Answer
        fields = ('id', 'ans', 'question')


class ReportSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Report
        fields = ('id', 'owner', 'poll_id', 'completed', 'answers')


class ReportStartSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Report
        fields = ('id', 'owner', 'poll_id', 'answers')


class UserReportSerializer(serializers.ModelSerializer):
    reports = ReportSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'reports')


class AnswersSendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'ans')


class PolCloseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Poll
        fields = ('id', 'date_end')
