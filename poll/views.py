import re

from django.db.models.query_utils import Q
from .models import Answer, Poll, Question, Report
from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import *
from datetime import datetime
import re
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
# Create your views here.


class UserViewSet(generics.ListCreateAPIView):
    """
    - 'GET' Получение списка юзеров
    - 'POST' Создание юзера

    - Для создание опроса требуется:
    -- {
        "username": "string",
        "password": "string"
        }
    """
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer

    def create(self, request, *args, **kwargs):
        return super(UserViewSet, self).create(request, *args, **kwargs)


class PollList(generics.ListCreateAPIView):
    """
    - 'GET' Получение списка опросов
    - 'POST' Создание опроса

    - Для создание опроса требуется:
    -- {
        "title": "string",
        "description": "string"
        }
    """
    queryset = Poll.objects.all()
    serializer_class = PollSerializer


class PollDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    - 'GET' Получение опроса (детально)
    - 'PUT' Изменение опроса
    - 'PATCH' Изменение опроса
    - 'DELETE' Удаление опроса

    - id - (poll.id)
    """
    queryset = Poll.objects.all()
    serializer_class = PollSerializer


class ReportCreate(generics.CreateAPIView):
    """
    - 'POST' Начало выполнение опроса.
    Опрос можно проходить анонимно. Для этого уберите - [owner]

    Для создание начала опроса требуется обязатально - {"poll_id":"int"}
    """
    serializer_class = ReportStartSerializer

    def perform_create(self, serializer):
        report = serializer.save()
        questions = Question.objects.filter(poll_id=report.poll_id).all()
        [(Answer(ans="", question=question, report_id=report).save())
            for question in questions]

        return Response(ReportStartSerializer(report).data, status=status.HTTP_201_CREATED)


class AnswerSend(generics.UpdateAPIView):
    """
    - 'PUT' Отправка ответа
    - 'PATCH' Отправка ответа
    - id - (answer.id)
    """
    queryset = Answer.objects.all()
    serializer_class = AnswersSendSerializer

    def update(self, request, **kwargs):
        answer = get_object_or_404(Answer, pk=kwargs.get('pk'))
        question = answer.question
        type = question.type
        chooses = [choose.words for choose in question.chooses.all()]
        success = False
        if type == 1 or type == 2:
            if request.data['ans'] in chooses:
                success = True
        else:
            success = True
        if success == True:
            answer.ans = request.data['ans']
            answer.save()
            return Response(AnswerSerializer(answer).data, status=status.HTTP_200_OK)

        return Response({"detail": "Error with answer type"}, status=status.HTTP_406_NOT_ACCEPTABLE)


class QuestionList(generics.ListCreateAPIView):
    """
    - 'GET' Получение списка вопросов. (Для понимания, что он создан)
    - 'POST' Создание вопроса.

    - ['type'] - 1 (Вопрос с одним вариантом ответа)
    - ['type'] - 2 (Вопрос с двумя и более вариантом ответа)
    - ['type'] - 3 (Вопрос с текстом)

    Создание текста вопроса. Пример с (type = 1). "chooses":["Яблоко"], (type = 2) "chooses":["Первый выбор", "Второй выбор"], (type = 3) "chooses": ["Длинный длинный текст и ещё больше"]

    - Для создание вопроса требуется обязательно - {'type': int, 'poll_id':''int, 'chooses': [String], 'question':'Вопрос?'}
    - text - выбор ответа 
    - question - выбор вопроса
    """

    queryset = Question.objects.all()
    serializer_class = QuestionlSerializer

    def create(self, request):
        question = Question
        poll = Poll.objects.filter(id=request.data['poll_id']).first()
        if poll is None:
            return Response({"detail": "None of poll"}, status=status.HTTP_404_NOT_FOUND)
        question = Question.objects.create(
            type=request.data['type'], poll_id=poll, question=request.data['question'])
        if (request.data['type'] == 1 and len(request.data['chooses']) == 1):
            Question_choice(
                words=request.data['chooses'][0], question_id=question).save()
        elif (request.data['type'] == 2) and len(request.data['chooses']) > 1:
            [Question_choice(words=word, question_id=question).save()
             for word in request.data['chooses']]
        elif (request.data['type'] == 3) and len(request.data['chooses']) == 1:
            Question_choice(
                words=request.data['chooses'][0], question_id=question,).save()
        else:
            return Response({"error": "Error with type of question"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        question.save()

        return Response(request.data, status=status.HTTP_201_CREATED)


class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    - 'GET' Получение вопроса (детально)
    - 'PUT' Изменение вопроса
    - 'PATCH' Изменение вопроса
    - 'DELETE' Удаление вопроса

    - id - (question.id)
    - question - название вопроса   
    - chooses - выбор ответа 
     """
    queryset = Question.objects.all()
    serializer_class = QuestionlSerializer

    def update(self, request, *args, **kwargs):
        question = Question.objects.filter(id=kwargs['pk']).first()
        if question is None:
            return Response({"detail": "question is None"}, status=status.HTTP_404_NOT_FOUND)
        if (request.data['type'] == 1 and len(request.data['chooses']) == 1):
            question.chooses.all().delete()
            Question_choice(
                words=request.data['chooses'][0], question_id=question).save()
        elif (request.data['type'] == 2) and len(request.data['chooses']) > 1:
            question.chooses.all().delete()
            [Question_choice(words=word, question_id=question).save()
             for word in request.data['chooses']]
        elif (request.data['type'] == 3) and len(request.data['chooses']) == 1:
            question.text.all().delete()
            Question_choice(
                words=request.data['chooses'][0], question_id=question).save()
        else:
            return Response({"error": "Error with type of question"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        question.question = kwargs.get('question')
        question.type = kwargs.get('type')

        return Response(QuestionlSerializer(question).data, status=status.HTTP_201_CREATED)


class ReportDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    - 'GET' Получение отчёта (детально)
    - 'PUT' Изменение отчёта
    - 'PATCH' Изменение отчёта
    - 'DELETE' Удаление отчёта

    - id - (report.id)
     """
    queryset = Report.objects.all()
    serializer_class = ReportSerializer


class UserReportsDetail(generics.ListAPIView):
    """
    - 'GET' Получение отчёта по id юзеру (детально)
    """

    queryset = User.objects.all()
    serializer_class = UserReportSerializer

    def list(self, request, **kwargs):
        user = generics.get_object_or_404(User, pk=kwargs.get('pk'))
        return Response(UserReportSerializer(user).data, status=status.HTTP_200_OK)


class PollClose(generics.UpdateAPIView):
    """
    - 'PUT' Завершение опроса
    - 'PATCH' Завершение опроса
    id -  (poll.id)
    """
    queryset = Poll.objects.all()
    serializer_class = PolCloseSerializer

    def perform_update(self, serializer):
        poll = Poll.objects.filter(id=serializer.data['id']).first()
        poll.date_end = datetime.utcnow()
        poll.save()
