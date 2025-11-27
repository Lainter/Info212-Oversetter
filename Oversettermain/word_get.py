import csv
import random
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
  
    
def find_random_word():
    random_row = random.randint(10,8449)
    if english_to_norwegian:
        column = 1
    else: 
        column = 0
    
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
                    return key, nyval

def check_translation():
    key,value = find_random_word()
    print ("engelsk: ", key,"\nnorsk: ",  value)
    active = True
    while(active):
        a = input(f"translate {key} \n")
        if isinstance(value, list):
            if a in value:
                print("wow! niceee")
                active = False
        elif a == value:
                print("wow! niceee")
                active = False     
        else:
            print("wrong")
            print(value)
            continue
check_translation()
            
        
        
        
    
        
                    
    
        
        
    