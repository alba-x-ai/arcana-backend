import express from "express";
import cors from "cors";
import fs from "fs";

const app = express();
app.use(cors());
app.use(express.json());

const DB_PATH = "./db.json";

// утилита загрузки базы
function loadDB() {
  if (!fs.existsSync(DB_PATH)) return {};
  return JSON.parse(fs.readFileSync(DB_PATH, "utf8"));
}

// утилита сохранения базы
function saveDB(data) {
  fs.writeFileSync(DB_PATH, JSON.stringify(data, null, 2));
}

// получить карту дня
app.post("/card-of-the-day", (req, res) => {
  const { user_id } = req.body;

  if (!user_id) {
    return res.status(400).json({ error: "No user_id" });
  }

  const today = new Date().toISOString().slice(0, 10); // YYYY-MM-DD
  const db = loadDB();

  if (!db[user_id]) db[user_id] = {};

  // если карта уже есть — возвращаем
  if (db[user_id][today] !== undefined) {
    return res.json({
      card: db[user_id][today],
      cached: true
    });
  }

  // иначе генерируем
  const card = Math.floor(Math.random() * 22); // 0–21

  db[user_id][today] = card;
  saveDB(db);

  res.json({
    card,
    cached: false
  });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Tarot backend running on ${PORT}`);
});
