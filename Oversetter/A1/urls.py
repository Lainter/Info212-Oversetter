from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('game/', views.game, name='game'),
    path('math-quiz/', views.math_quiz, name='math_quiz'),
    path('vocabulary/', views.vocabulary, name='vocabulary'),
    path('categories/', views.categories, name='categories'),
    path('menu/', views.menu, name='menu'),
    path('sign-in/', views.sign_in, name='sign_in'),
    
    # API endpoints for the game
    path('get_question/', views.get_question, name='get_question'),
    path('check_answer/', views.check_answer, name='check_answer'),
    path('set_language/', views.set_language, name='set_language'),
    path('get_translation_question/', views.get_translation_question, name='get_translation_question'),
    path('check_translation/', views.check_translation, name='check_translation'),
]