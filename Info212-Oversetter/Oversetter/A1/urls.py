from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('game/', views.game, name='game'),
    path('vocabulary/', views.vocabulary, name='vocabulary'),
    path('categories/', views.categories, name='categories'),
    path('menu/', views.menu, name='menu'),
    path('sign-in/', views.sign_in, name='sign_in'),
    path('api/random-word/', views.get_translation_question, name='random_word'),
]