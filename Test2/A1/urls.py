from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("get-question/", views.get_question, name="get_question"),
    path("check-answer/", views.check_answer, name="check_answer"),
]