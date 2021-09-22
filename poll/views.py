import re
from .models import Answer, Poll, Question, Report
from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import *
from datetime import datetime
import re
from rest_framework import status
from rest_framework.response import Response
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
        questions = Question.objects.filter(poll_id=report.poll_id).all()
        [(Answer(ans="", question=question, report_id=report).save())
            for question in questions]


class AnswerSend(generics.UpdateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswersSendSerializer


class QuestionList(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionlSerializer

    def create(self, request):
        question = Question
        poll = Poll.objects.filter(id=request.data['poll_id']).first()
        if poll is None:
            return Response({"detail": "None of poll"}, status=status.HTTP_404_NOT_FOUND)
        question = Question.objects.create(
            type=request.data['type'], poll_id=poll)
        if (request.data['type'] == 1 and len(re.findall(r'\w+', request.data['text'][0])) == 1 and len(request.data['text']) == 1):
            print(re.findall(r'\w+', request.data['text'][0]))
            Question_choice(
                words=request.data['text'][0], question_id=question).save()
        elif (request.data['type'] == 2) and len(request.data['text']) > 1:
            [Question_choice(words=word, question_id=question).save()
             for word in request.data['text']]
        elif (request.data['type'] == 3) and len(request.data['text']) == 1:
            Question_choice(
                words=request.data['text'][0], question_id=question).save()
        else:
            return Response({"error": "Error with type of question"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        question.save()

        return Response(request.data, status=status.HTTP_201_CREATED)


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
