from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI()

# --- CORS (обязательно для Mini App) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ДАННЫЕ АРКАНОВ (MVP-слой) ---

ARCANA = [
    {
        "id": 1,
        "key": "magician",
        "name": "The Magician",
        "essence": "Conscious will, focus, and the power to act intentionally.",
        "positions": {
            "past": "You learned how to direct your energy instead of wasting it.",
            "present": "You are being asked to act — not wait, not doubt.",
            "future": "Mastery comes through deliberate choice and practice."
        }
    },
    {
        "id": 2,
        "key": "high_priestess",
        "name": "The High Priestess",
        "essence": "Inner knowledge, silence, and trust in the unseen.",
        "positions": {
            "past": "You were guided by intuition even when logic was absent.",
            "present": "Something is not meant to be revealed yet — listen inward.",
            "future": "Clarity will emerge when you stop forcing answers."
        }
    },
    {
        "id": 3,
        "key": "empress",
        "name": "The Empress",
        "essence": "Creation, nourishment, and embodied abundance.",
        "positions": {
            "past": "You experienced growth through care, beauty, or connection.",
            "present": "It is time to nurture what you want to grow.",
            "future": "What you invest love in will flourish."
        }
    },
    {
        "id": 4,
        "key": "emperor",
        "name": "The Emperor",
        "essence": "Structure, responsibility, and the strength to hold form.",
        "positions": {
            "past": "You learned discipline through rules, limits, or authority.",
            "present": "Stability requires ownership, not control.",
            "future": "What you build with integrity will endure."
        }
    },
    {
        "id": 5,
        "key": "hierophant",
        "name": "The Hierophant",
        "essence": "Tradition, meaning, and shared spiritual language.",
        "positions": {
            "past": "Teachings or mentors shaped your worldview.",
            "present": "You are questioning inherited beliefs.",
            "future": "True guidance comes through lived experience."
        }
    }
]

# --- ENDPOINT: 3-CARD SPREAD ---

@app.get("/spread/three")
def three_card_spread(user_id: int = 0, language: str = "en"):
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
                "name": card["name"]
            },
            "meaning": {
                "full": card["positions"][pos]
            }
        })

    return {
        "cards": spread
    }

