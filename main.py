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
