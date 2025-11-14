import sqlite3

DB_PATH = "Info_212_Oversetter/db.sqlite3"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# === Define simple semantic categories ===
TAG_RULES = {
    "animal": ["dog", "cat", "fish", "bird", "horse", "cow", "lion", "bear", "animal", "mouse", "pig"],
    "gaming": ["game", "play", "player", "level", "boss", "score", "quest", "battle", "win"],
    "cooking": ["cook", "food", "meal", "recipe", "kitchen", "bake", "boil", "fry", "eat"],
    "travel": ["travel", "journey", "trip", "country", "city", "road", "map", "flight"],
    "technology": ["computer", "tech", "phone", "app", "internet", "code", "data", "AI"],
    "emotion": ["happy", "sad", "angry", "love", "fear", "joy", "cry", "smile"],
    "school": ["school", "teacher", "student", "class", "study", "learn", "exam"],
}

# === Helper functions ===
def get_or_create_tag(tag_name):
    cursor.execute("SELECT id FROM Translation_Game_tag WHERE name = ?", (tag_name,))
    res = cursor.fetchone()
    if res:
        return res[0]
    cursor.execute("INSERT INTO Translation_Game_tag (name) VALUES (?)", (tag_name,))
    conn.commit()
    return cursor.lastrowid

def link_word_to_tag(word_id, tag_id):
    cursor.execute(
        """
        SELECT 1 FROM Translation_Game_word_tags
        WHERE word_id = ? AND tag_id = ?
        """,
        (word_id, tag_id),
    )
    if cursor.fetchone():
        return
    cursor.execute(
        "INSERT INTO Translation_Game_word_tags (word_id, tag_id) VALUES (?, ?)",
        (word_id, tag_id),
    )

# === Fetch all words ===
cursor.execute("SELECT id, word FROM Translation_Game_word")
words = cursor.fetchall()

# === Create tags upfront ===
tag_ids = {tag: get_or_create_tag(tag) for tag in TAG_RULES.keys()}

# === Assign tags to words ===
total_links = 0
for word_id, word_text in words:
    word_lower = word_text.lower()
    for tag, keywords in TAG_RULES.items():
        if any(keyword in word_lower for keyword in keywords):
            link_word_to_tag(word_id, tag_ids[tag])
            total_links += 1

conn.commit()
conn.close()
print(f"✅ Tagging complete! {len(TAG_RULES)} tags created/verified and {total_links} links added.")
