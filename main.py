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

# --- загрузка арканов из JSON ---

ARCANA_PATH = Path(__file__).parent / "arcana.json"

with open(ARCANA_PATH, "r", encoding="utf-8") as f:
    ARCANA = json.load(f)

# --- endpoint ---

@app.get("/spread/three")
def three_card_spread(user_id: int = 0, language: str = "en"):
    positions = ["past", "present", "future"]
    cards = random.sample(ARCANA, 3)

    spread = []

    for pos, card in zip(positions, cards):
        spread.append({
            "position": pos,
            "card": {
                "id": card["id"],
                "key": card["key"],
                "name": card["name"].get(language, card["name"]["en"])
            },
            "meaning": {
                "full": card["positions"][pos].get(language, card["positions"][pos]["en"])
            }
        })

    return {"cards": spread}
