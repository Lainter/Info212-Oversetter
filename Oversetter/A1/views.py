import random #for å hente tilfeldig svar
from django.shortcuts import render
from django.http import JsonResponse
import csv
import random
english_to_norwegian = True

quiz = [
    {"question": "1+1", "answers": ["2", "two","to"]},
    {"question": "3+4", "answers": ["7", "seven","syv"]},
    {"question": "5-2", "answers": ["3", "three","tre"]},
    {"question": "6*2", "answers": ["12", "twelve","tolv"]},
]

def home(request):
    return render(request, "home.html")

def game(request):
    return render(request, "game.html")

# Add these missing view functions:
def categories(request):
    return render(request, "categories.html")

def menu(request):
    return render(request, "menu.html")

def math_quiz(request):
    return render(request, "math_quiz.html")

def vocabulary(request):
    return render(request, "vocabulary.html")

def sign_in(request):
    return render(request, "sign_in.html")


def home(request):
    return render(request, "home.html")


def get_question(request):
    question = random.choice(quiz)
    return JsonResponse({"question": question["question"]})


def check_answer(request):
    user_answer = request.GET.get("answer", "").strip().lower()
    question_text = request.GET.get("question", "")

    # Find the question in the list
    for q in quiz:
        if q["question"] == question_text:
            is_correct = user_answer in [a.lower() for a in q["answers"]]
            return JsonResponse({"result": "Riktig!" if is_correct else "Feil, det riktige svaret er  " + q["answers"][0]})

    # fallback
    return JsonResponse({"result": "Question not found"})
def set_language(request):
    global english_to_norwegian
    lang = request.GET.get("language", "")
    if lang == "en_to_no":
        english_to_norwegian = True
        return JsonResponse({"status": "Language set to English → Norwegian"})
    elif lang == "no_to_en":
        english_to_norwegian = False
        return JsonResponse({"status": "Language set to Norwegian → English"})
    else:
        return JsonResponse({"status": "Invalid language"})


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
  
    
def find_random_word():
    random_row = random.randint(2, 8415)
    global english_to_norwegian
    
    if english_to_norwegian:
        column = 1
    else: 
        column = 0
    
    try:
        with open('cleaned.csv', 'r', encoding='utf-8') as file:
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
    word, correct_translations = find_random_word()
    
    # Store the correct answer in session for verification
    request.session['current_translation'] = {
        'word': word,
        'correct_answers': correct_translations if isinstance(correct_translations, list) else [correct_translations]
    }
    
    return JsonResponse({
        "question": word,
        "language": "English → Norwegian" if english_to_norwegian else "Norwegian → English"
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