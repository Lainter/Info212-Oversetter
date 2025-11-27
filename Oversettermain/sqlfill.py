import sqlite3
import csv
import ast
from pathlib import Path

DB_PATH = Path("Info_212_Oversetter/db.sqlite3")
CSV_PATH = Path("dictionary_clean.csv")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

def get_or_create_language(code, name):
    cursor.execute("SELECT id FROM Translation_Game_language WHERE code = ?", (code,))
    r = cursor.fetchone()
    if r:
        return r[0]
    cursor.execute("INSERT INTO Translation_Game_language (code, name) VALUES (?, ?)", (code, name))
    conn.commit()
    return cursor.lastrowid

def get_or_create_word(word_text, language_id):
    word_text = word_text.strip()
    cursor.execute("SELECT id FROM Translation_Game_word WHERE word = ? AND language_id = ?", (word_text, language_id))
    r = cursor.fetchone()
    if r:
        return r[0]
    cursor.execute("INSERT INTO Translation_Game_word (word, language_id) VALUES (?, ?)", (word_text, language_id))
    conn.commit()
    return cursor.lastrowid

def ensure_translation(src_id, tgt_id):
    cursor.execute("SELECT 1 FROM Translation_Game_translation WHERE source_word_id = ? AND target_word_id = ?", (src_id, tgt_id))
    if cursor.fetchone():
        return
    cursor.execute("INSERT INTO Translation_Game_translation (source_word_id, target_word_id) VALUES (?, ?)", (src_id, tgt_id))
    conn.commit()

no_id = get_or_create_language("no", "Norwegian")
en_id = get_or_create_language("en", "English")

with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    total_pairs = 0
    for row in reader:
        if len(row) < 2:
            continue
        nor = row[0].strip()
        eng_part = row[1].strip()
        try:
            if eng_part.startswith('[') or eng_part.startswith('"[') or eng_part.startswith("['"):
                eng_words = ast.literal_eval(eng_part)
                if isinstance(eng_words, str):
                    eng_words = [eng_words]
            else:
                eng_words = [eng_part]
        except Exception:
            eng_words = [eng_part]

        nor_id = get_or_create_word(nor, no_id)
        for eng in eng_words:
            eng_id = get_or_create_word(eng, en_id)
            #Insert both language directions
            ensure_translation(nor_id, eng_id)
            ensure_translation(eng_id, nor_id)
            total_pairs += 1

print(f"Imported {total_pairs} CSV word pairs.")
conn.close()
