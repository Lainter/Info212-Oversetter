from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('game/', views.game, name='game'),
    path('register/', views.register, name='register'),

    # API endpoints for the game
    path('get_question/', views.get_question, name='get_question'),
    path('check_answer/', views.check_answer, name='check_answer'),
    path('set_language/', views.set_language, name='set_language'),
    path('get_translation_question/', views.get_translation_question, name='get_translation_question'),
    path('api/random-translation/', views.get_random_translation, name='random_translation'),

]