import express from "express";
import cors from "cors";

const app = express();
app.use(cors());
app.use(express.json());

/* ---------- STORAGE (MVP) ---------- */
const dailyCards = new Map();

/* ---------- UTILS ---------- */
function getUserLocalDate(timezoneOffset) {
  // timezoneOffset в минутах (например -420)
  const localTime = new Date(Date.now() - timezoneOffset * 60 * 1000);
  return localTime.toISOString().split("T")[0]; // YYYY-MM-DD
}

function randomCard() {
  return {
    card: Math.floor(Math.random() * 22),
    reversed: Math.random() < 0.5
  };
}

/* ---------- ROUTE ---------- */
app.post("/card-of-the-day", (req, res) => {
  const { user_id, timezoneOffset } = req.body;

  if (!user_id || timezoneOffset === undefined) {
    return res.status(400).json({ error: "Missing data" });
  }

  const userDate = getUserLocalDate(timezoneOffset);
  const key = `${user_id}_${userDate}`;

  if (dailyCards.has(key)) {
    return res.json(dailyCards.get(key));
  }

  const newCard = randomCard();
  dailyCards.set(key, newCard);

  res.json(newCard);
});

/* ---------- SERVER ---------- */
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log("Arcana server running on port", PORT);
});
