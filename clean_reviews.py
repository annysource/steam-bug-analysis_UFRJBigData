import json
import csv
import re

INPUT_FILE = "Indie_RelicHuntersZero.json"
OUTPUT_FILE = "Indie_RelicHuntersZero.csv"

BUG_WORDS = [
    "bug",
    "crash",
    "freeze",
    "lag",
    "glitch",
    "broken",
    "stuck",
    "fps",
    "optimization"
]

def clean_text(text):
    if not text:
        return ""

    text = text.lower()
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def detect_bug(text):
    return any(word in text for word in BUG_WORDS)

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

reviews = data.get("reviews", {})

if isinstance(reviews, dict):
    reviews = reviews.values()

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow([
        "review_id",
        "steam_id",
        "playtime_forever",
        "review_text",
        "voted_up",
        "bug_detected",
        "timestamp_created"
    ])

    for review in reviews:

        author = review.get("author", {})

        review_text = clean_text(
            review.get("review", "")
        )

        writer.writerow([
            review.get("recommendationid"),
            author.get("steamid"),
            author.get("playtime_forever"),
            review_text,
            review.get("voted_up"),
            detect_bug(review_text),
            review.get("timestamp_created")
    ])

print("CSV gerado com sucesso.")
