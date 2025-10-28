import random #for å hente tilfeldig svar
from django.shortcuts import render
from django.http import JsonResponse
import csv
import random

def home(request):
    return render(request, "home.html")

def game(request):
    return render(request, "game.html")

def categories(request):
    return render(request, "categories.html")

def menu(request):
    return render(request, "menu.html")

def vocabulary(request):
    return render(request, "vocabulary.html")

def sign_in(request):
    return render(request, "sign_in.html")


def home(request):
    return render(request, "home.html")

def find_one_word(row, column):
    if column == 0:
        count = row[0].count(',')
        if count > 0:
            n = random.randint(0, count)
            b = [item.strip() for item in row[0].split(',')]
            row[0] = b[n]
    else:
        count = row[1].count(',')
        if count > 0:
            n = random.randint(0, count)
            b = [item.strip() for item in row[1].split(',')]
            row[1] = b[n]
    return row
  
    
def find_random_word(bool):
    random_row = random.randint(2, 8415)    
    if bool:
        column = 1
    else: 
        column = 0
    try:
        with open('templates/dictionary_clean.csv', 'r', encoding='utf-8') as file:
            words = csv.reader(file)
            for i, rows in enumerate(words):
                if i < 10:
                    continue
                else:
                    if i == random_row:
                        b = find_one_word(rows, column)
                        key = b[column]
                        value = b[1 - column]
                        if value.count(',') > 0:
                            nyval = [item.strip() for item in value.split(',')]
                        else:
                            nyval = value
                        return key, nyval
    except FileNotFoundError:
        return JsonResponse({"csv file not found!"})
    
    return JsonResponse({"csv file not found! or something else"})

def get_translation_question(request):
    direction = request.GET.get('direction', 'en-no')
    english_to_norwegian = (direction == 'en-no')
    word, correct_translations = find_random_word(english_to_norwegian)
    print(word, correct_translations)
    return JsonResponse({
        "word": word,
        "translations": correct_translations
    })

def check_translation(request):
    """Check if the translation is correct"""
    user_answer = request.GET.get("answer", "").strip().lower()
    
    # Get the stored correct answer from session
    current_translation = request.session.get('current_translation', {})
    correct_answers = current_translation.get('correct_answers', [])
    original_word = current_translation.get('word', '')
    
    # Check if answer is correct
    is_correct = user_answer in [ans.lower() for ans in correct_answers]
    
    if is_correct:
        result = "Riktig! Godt jobbet! 🎉"
    else:
        if len(correct_answers) == 1:
            result = f"Feil. Riktig svar er: {correct_answers[0]}"
        else:
            result = f"Feil. Riktige svar er en av disse: {(correct_answers)}"
    
    return JsonResponse({
        "result": result,
        "correct": is_correct
    })