"""import csv
import random

from django.http import JsonResponse
english_to_norwegian = True

def select_lang():
    print("Choose your language!")
    if input() == 1:
        english_to_norwegian = True
        return
    elif input () == 2:
        english_to_norwegian = False
        return
    else:
        print("invalid language")
        return


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
  
    
def find_random_word(request):
    english_to_norwegian = request.GET.get('direction', 'en-no') == 'en-no'
    random_row = random.randint(10,8449)
    column = 1 if english_to_norwegian else column = 0
    
    with open('cleaned.csv ', 'r', encoding = 'utf-8') as file:
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
                        nyval = [item.strip() for  item in value.split(',')]
                    else:
                        nyval = value
                    return JsonResponse({
                    'word': key,
                    'translations': nyval                  
                    })
        return JsonResponse({'error': 'No word found'}, status=404)
            
        
        
        
    
        
                    
    
        
        
    """