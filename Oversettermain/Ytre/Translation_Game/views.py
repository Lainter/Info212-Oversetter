from django.shortcuts import render
import csv
import random
from django.http import JsonResponse
from .models import Word, Translation, Language
english_to_norwegian = True
def get_random_translation(request):
    source_lang = request.GET.get('source', 'en')
    target_lang = request.GET.get('target', 'no')

    try:
        src_lang = Language.objects.get(code=source_lang)
        tgt_lang = Language.objects.get(code=target_lang)
    except Language.DoesNotExist:
        return JsonResponse({'error': 'Invalid language code'}, status=400)

    translations = Translation.objects.filter(
        source_word__language=src_lang,
        target_word__language=tgt_lang
    ).select_related('source_word', 'target_word')

    if not translations.exists():
        return JsonResponse({'error': 'No translations found'}, status=404)

    random_translation = random.choice(list(translations))
    
    source_word_text = random_translation.source_word.word
    count = source_word_text.count(',')
    if count > 0:
        n = random.randint(0, count)
        b = [item.strip() for item in source_word_text.split(',')]
        source_word_text = b[n]
        
    return JsonResponse({
        'source_word': source_word_text,
        'target_word': random_translation.target_word.word,
        'source_language': src_lang.code,
        'target_language': tgt_lang.code,
    })

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
            return JsonResponse(
                {"result": "Riktig!" if is_correct else "Feil, det riktige svaret er  " + q["answers"][0]})

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