import re
from .models import Answer, Poll, Question, Report
from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import *
from rest_framework.generics import get_object_or_404
from datetime import datetime
# Create your views here.


class PollList(generics.ListCreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    

class PollDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer


class ReportCreate(generics.CreateAPIView):
    serializer_class = ReportStartSerializer


    def perform_create(self, serializer):
        report = serializer.save()
        questions = Question.objects.filter(poll = report.poll_id).all()
        [(Answer(ans = "", question_id = question, report_id = report).save()) 
            for question in questions]



class AnswerSend(generics.UpdateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswersSendSerializer


class QuestionList(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionlSerializer
      

class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionlSerializer


class ReportDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer 


class UserReportsDetail(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserReportSerializer


class PollClose(generics.UpdateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PolCloseSerializer

    def perform_update(self, serializer):
        poll = Poll.objects.filter(id=serializer.data['id']).first()
        poll.date_end = datetime.utcnow()
        poll.save()