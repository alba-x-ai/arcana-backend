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

@app.get("/spread/three")
def three_card_spread(
    language: str = "en",
    allow_reversed: bool = False
):
    positions = ["past", "present", "future"]
    cards = random.sample(ARCANA, 3)

    spread = []

    for pos, card in zip(positions, cards):
        # 1️⃣ ориентация определяется ВСЕГДА
        is_reversed = random.choice([True, False])

        # 2️⃣ решаем, КАК читать карту
        if is_reversed and allow_reversed:
            meaning_block = card["meaning"]["reversed"]
        else:
            meaning_block = card["meaning"]["upright"]

        spread.append({
            "position": pos,
            "orientation": "reversed" if is_reversed else "upright",
            "card": {
                "id": card["id"],
                "key": card["key"],
                "name": card["name"].get(language, card["name"]["en"])
            },
            "meaning": {
                "card": meaning_block.get(language, meaning_block["en"]),
                "position": card["positions"][pos].get(
                    language,
                    card["positions"][pos]["en"]
                )
            }
        })

    return { "cards": spread }
