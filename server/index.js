import express from "express";
import cors from "cors";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const app = express();
app.use(cors());
app.use(express.json());

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const DB_PATH = path.join(__dirname, "db.json");

/* ---------- utils ---------- */

function loadDB() {
  if (!fs.existsSync(DB_PATH)) {
    fs.writeFileSync(DB_PATH, JSON.stringify({}));
  }
  return JSON.parse(fs.readFileSync(DB_PATH, "utf8"));
}

function saveDB(data) {
  fs.writeFileSync(DB_PATH, JSON.stringify(data, null, 2));
}

/* ---------- health ---------- */

app.get("/__ping", (req, res) => {
  res.json({ alive: true });
});

/* ---------- card of the day ---------- */

app.post("/card-of-the-day", (req, res) => {
  const { user_id } = req.body;
  if (!user_id) {
    return res.status(400).json({ error: "No user_id" });
  }

  const today = new Date().toISOString().slice(0, 10);
  const db = loadDB();

  if (!db[user_id]) db[user_id] = {};

  // если уже есть карта на сегодня
  if (db[user_id][today]) {
    return res.json(db[user_id][today]);
  }

  const card = Math.floor(Math.random() * 22); // 0–21
  const reversed = Math.random() < 0.5; // true / false

  const payload = {
    card,
    reversed
  };

  db[user_id][today] = payload;
  saveDB(db);

  res.json(payload);
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Tarot backend running on port ${PORT}`);
});
