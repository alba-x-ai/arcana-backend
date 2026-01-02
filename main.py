from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random
import json
from pathlib import Path

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ARCANA_PATH = Path(__file__).parent / "arcana.json"

with open(ARCANA_PATH, "r", encoding="utf-8") as f:
    ARCANA = json.load(f)

# --- ОДНА КАРТА / ОДИН ВОПРОС ---
@app.get("/spread/one")
def one_card_spread(language: str = "en"):
    card = random.choice(ARCANA)

    # ориентация определяется ВСЕГДА
    is_reversed = random.choice([True, False])

    meaning_block = (
        card["meaning"]["reversed"]
        if is_reversed
        else card["meaning"]["upright"]
    )

    return {
        "card": {
            "id": card["id"],
            "key": card["key"],
            "name": card["name"].get(language, card["name"]["en"]),
            "orientation": "reversed" if is_reversed else "upright"
        },
        "meaning": meaning_block.get(language, meaning_block["en"])
    }
from datetime import date
import hashlib

@app.get("/spread/daily")
def daily_card(language: str = "en"):
    today = date.today().isoformat()

    # детерминированный seed от даты
    seed = int(hashlib.sha256(today.encode()).hexdigest(), 16)
    rng = random.Random(seed)

    card = rng.choice(ARCANA)
    is_reversed = rng.choice([True, False])

    meaning_block = (
        card["meaning"]["reversed"]
        if is_reversed
        else card["meaning"]["upright"]
    )

    return {
        "date": today,
        "card": {
            "id": card["id"],
            "key": card["key"],
            "name": card["name"].get(language, card["name"]["en"]),
            "orientation": "reversed" if is_reversed else "upright"
        },
        "meaning": meaning_block.get(language, meaning_block["en"])
    }
