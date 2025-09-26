import random #for å hente tilfeldig svar
from django.shortcuts import render
from django.http import JsonResponse

quiz = [
    {"question": "1+1", "answers": ["2", "two","to"]},
    {"question": "3+4", "answers": ["7", "seven","syv"]},
    {"question": "5-2", "answers": ["3", "three","tre"]},
    {"question": "6*2", "answers": ["12", "twelve","tolv"]},
]


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