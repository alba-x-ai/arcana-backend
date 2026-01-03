import express from "express";
import cors from "cors";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const app = express();

/* -------------------- базовая настройка -------------------- */

app.use(cors());
app.use(express.json());

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const DB_PATH = path.join(__dirname, "db.json");

/* -------------------- utils -------------------- */

function loadDB() {
  if (!fs.existsSync(DB_PATH)) {
    fs.writeFileSync(DB_PATH, JSON.stringify({}));
  }
  return JSON.parse(fs.readFileSync(DB_PATH, "utf8"));
}

function saveDB(data) {
  fs.writeFileSync(DB_PATH, JSON.stringify(data, null, 2));
}

/* -------------------- DIAGNOSTIC ROUTE -------------------- */
/* ЭТО НУЖНО ДЛЯ ПРОВЕРКИ, ЧТО RENDER ЗАПУСТИЛ ИМЕННО ЭТОТ ФАЙЛ */

app.get("/__ping", (req, res) => {
  res.json({ alive: true });
});

/* -------------------- MAIN API -------------------- */

app.post("/card-of-the-day", (req, res) => {
  const { user_id } = req.body;

  if (!user_id) {
    return res.status(400).json({ error: "No user_id" });
  }

  const today = new Date().toISOString().slice(0, 10);
  const db = loadDB();

  if (!db[user_id]) {
    db[user_id] = {};
  }

  if (db[user_id][today] !== undefined) {
    return res.json({
      card: db[user_id][today],
      cached: true
    });
  }

  const card = Math.floor(Math.random() * 22); // 0–21

  db[user_id][today] = card;
  saveDB(db);

  res.json({
    card,
    cached: false
  });
});

/* -------------------- SERVER START -------------------- */

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`Tarot backend running on port ${PORT}`);
});
