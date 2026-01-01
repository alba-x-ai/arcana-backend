from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/spread/three")
def three_card_spread(user_id: int = 0, language: str = "en"):
    return {
        "cards": [
            {
                "position": "past",
                "meaning": {
                    "full": "The past invites reflection and understanding."
                }
            },
            {
                "position": "present",
                "meaning": {
                    "full": "The present reveals what is asking for attention."
                }
            },
            {
                "position": "future",
                "meaning": {
                    "full": "The future unfolds through conscious choice."
                }
            }
        ]
    }
