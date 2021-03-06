
from django.urls import path
from .views import *
app_name = "articles"
# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('poll', PollList.as_view()),
    path('poll/<int:pk>', PollDetail.as_view()),
    path('poll/<int:pk>/close', PollClose.as_view()),
    path('questions', QuestionList.as_view()),
    path('questions/<int:pk>', QuestionDetail.as_view()),
    path('report/<int:pk>', ReportDetail.as_view()),
    path('report/start', ReportCreate.as_view()),
    path('user', UserViewSet.as_view()),
    path('user/<int:pk>/report', UserReportsDetail.as_view()),
    path('answer/<int:pk>', AnswerSend.as_view()),
]
