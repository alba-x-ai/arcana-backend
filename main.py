from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random
import json
from pathlib import Path

app = FastAPI()

# --- CORS (нужно для Telegram Mini App) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Загрузка арканов из JSON ---
ARCANA_PATH = Path(__file__).parent / "arcana.json"

with open(ARCANA_PATH, "r", encoding="utf-8") as f:
    ARCANA = json.load(f)

# --- Endpoint: расклад из 3 карт ---
@app.get("/spread/three")
def three_card_spread(language: str = "en"):
    positions = ["past", "present", "future"]

    # выбираем 3 разные карты
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
                # общий смысл карты
                "card": card["meaning"].get(language, card["meaning"]["en"]),
                # позиционный смысл
                "position": card["positions"][pos].get(
                    language,
                    card["positions"][pos]["en"]
                )
            }
        })

    return {
        "cards": spread
    }
