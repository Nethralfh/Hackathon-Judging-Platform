"use strict";

const express = require("express");
const fs      = require("fs");
const path    = require("path");
const Database = require("better-sqlite3");

const app = express();
app.use(express.json());

// ---------- VIEW ENGINE ----------
app.set("view engine", "ejs");
// __dirname is now src/, so views live at src/views/
app.set("views", path.join(__dirname, "views"));

// ---------- DATABASE ----------
// DB file sits at project root (one level up from src/)
const DB_PATH = path.join(__dirname, "..", "dogfood.db");

// Wipe old db on every boot so seed data is always fresh
if (fs.existsSync(DB_PATH)) fs.unlinkSync(DB_PATH);
const db = new Database(DB_PATH);

// ---------- SCHEMA ----------
db.exec(`
  CREATE TABLE event (
    id TEXT PRIMARY KEY,
    name TEXT,
    submissions_close TEXT
  );
  CREATE TABLE project (
    id TEXT PRIMARY KEY,
    team TEXT,
    track TEXT,
    title TEXT,
    summary TEXT,
    repo_url TEXT,
    submitted_at TEXT
  );
  CREATE TABLE session (
    token TEXT PRIMARY KEY,
    role TEXT,
    judge_id TEXT
  );
  CREATE TABLE IF NOT EXISTS score (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    judge_id     TEXT NOT NULL,
    project_id   TEXT NOT NULL,
    criteria_json TEXT NOT NULL,
    comment      TEXT,
    submitted_at TEXT NOT NULL,
    UNIQUE(judge_id, project_id)
  );
`);

// ---------- LOAD FIXTURES ----------
// fixtures.json lives at project root
const fixturesPath = path.join(__dirname, "..", "fixtures.json");
const fixtures     = JSON.parse(fs.readFileSync(fixturesPath, "utf-8"));

function loadFixtures() {
  const ev = fixtures.event;
  db.prepare("INSERT INTO event (id, name, submissions_close) VALUES (?, ?, ?)")
    .run(ev.id, ev.name, ev.submissions_close);

  const insertProject = db.prepare(
    "INSERT INTO project (id, team, track, title, summary, repo_url, submitted_at) VALUES (?, ?, ?, ?, ?, ?, ?)"
  );
  for (const p of fixtures.projects || []) {
    insertProject.run(p.id, p.team, p.track, p.title, p.summary, p.repo_url, p.submitted_at);
  }

  const judges  = fixtures.judges || [];
  const judgeAId = judges[0] ? judges[0].id : "jdg_01";
  const judgeBId = judges[1] ? judges[1].id : "jdg_02";

  const insertSession = db.prepare("INSERT INTO session VALUES (?, ?, ?)");
  insertSession.run("org_7f2a",    "organizer",   null);
  insertSession.run("jdg_a_91bc", "judge",        judgeAId);
  insertSession.run("jdg_b_44de", "judge",        judgeBId);
  insertSession.run("prt_2e88",   "participant",  null);

  // Seed scores from fixtures for the organizer dashboard demo
  const insertScore = db.prepare(
    `INSERT OR IGNORE INTO score (judge_id, project_id, criteria_json, comment, submitted_at)
     VALUES (?, ?, ?, ?, ?)`
  );
  const now = new Date().toISOString();
  for (const s of (fixtures.scores || [])) {
    insertScore.run(
      s.judge,
      s.project,
      JSON.stringify(s.criteria || {}),
      s.comment || "",
      now
    );
  }

  console.log("=== DOGFOOD test sessions ===");
  console.log("organizer   -> Cookie: session=org_7f2a");
  console.log(`judge_a     -> Cookie: session=jdg_a_91bc  (maps to judge ${judgeAId})`);
  console.log(`judge_b     -> Cookie: session=jdg_b_44de  (maps to judge ${judgeBId})`);
  console.log("participant -> Cookie: session=prt_2e88");
  console.log("==============================");
}

loadFixtures();

// ---------- AUTH HELPER ----------
function getCurrentUser(req) {
  const cookie = req.headers.cookie || "";
  const match  = cookie.split(";").map(c => c.trim()).find(c => c.startsWith("session="));
  if (!match) return null;
  const token = match.split("=")[1];
  const row   = db.prepare("SELECT * FROM session WHERE token = ?").get(token);
  if (!row) return null;
  return { role: row.role, judgeId: row.judge_id };
}

// ---------- PAGE ROUTES (EJS) ----------
const createPagesRouter = require("./routes/pages");
app.use("/", createPagesRouter(db, fixtures));

// ---------- API ROUTES ----------

// Root
app.get("/", (req, res) => {
  res.redirect("/projects");
});

// POST /projects/new — Project submission API
app.post("/projects/new", (req, res) => {
  const user = getCurrentUser(req);
  if (!user || user.role !== "participant") {
    return res.status(401).json({ error: "unauthorized" });
  }

  const ev       = db.prepare("SELECT * FROM event").get();
  const deadline = new Date(ev.submissions_close);
  const now      = new Date();

  if (now > deadline) {
    return res.status(403).json({ error: "submissions are closed" });
  }

  const { title, summary, repo_url } = req.body;
  if (!title || !summary || !repo_url) {
    return res.status(400).json({ error: "title, summary, and repo_url are required" });
  }

  const id = "prj_" + Math.random().toString(36).slice(2, 8);
  db.prepare(
    "INSERT INTO project (id, team, track, title, summary, repo_url, submitted_at) VALUES (?, ?, ?, ?, ?, ?, ?)"
  ).run(id, "unknown", "trk_01", title, summary, repo_url, new Date().toISOString());

  res.status(201).json({ status: "submitted", id });
});

// POST /api/scores — Submit or update a score (judge only)
app.post("/api/scores", (req, res) => {
  const user = getCurrentUser(req);
  if (!user || user.role !== "judge" || !user.judgeId) {
    return res.status(401).json({ error: "unauthorized" });
  }

  const { project_id, criteria, comment } = req.body;
  if (!project_id || !criteria) {
    return res.status(400).json({ error: "project_id and criteria are required" });
  }

  // Validate criteria values
  for (const [key, val] of Object.entries(criteria)) {
    const n = Number(val);
    if (!Number.isInteger(n) || n < 1 || n > 5) {
      return res.status(400).json({ error: `Invalid score for ${key}: must be 1–5` });
    }
  }

  db.prepare(
    `INSERT INTO score (judge_id, project_id, criteria_json, comment, submitted_at)
     VALUES (?, ?, ?, ?, ?)
     ON CONFLICT(judge_id, project_id) DO UPDATE SET
       criteria_json = excluded.criteria_json,
       comment       = excluded.comment,
       submitted_at  = excluded.submitted_at`
  ).run(
    user.judgeId,
    project_id,
    JSON.stringify(criteria),
    comment || "",
    new Date().toISOString()
  );

  res.status(200).json({ status: "saved" });
});

// GET /api/export/csv — Download scores as CSV (organizer only)
app.get("/api/export/csv", (req, res) => {
  const user = getCurrentUser(req);
  if (!user || user.role !== "organizer") {
    return res.status(401).json({ error: "unauthorized" });
  }

  const scores = db.prepare(
    `SELECT s.judge_id, s.project_id, p.title, s.criteria_json, s.comment, s.submitted_at
     FROM score s
     LEFT JOIN project p ON p.id = s.project_id
     ORDER BY s.project_id, s.judge_id`
  ).all();

  const lines = ["judge_id,project_id,project_title,functionality,creativity,impact,comment,submitted_at"];
  for (const row of scores) {
    let criteria = {};
    try { criteria = JSON.parse(row.criteria_json); } catch (_) {}
    const cols = [
      row.judge_id,
      row.project_id,
      `"${(row.title || "").replace(/"/g, '""')}"`,
      criteria.functionality ?? "",
      criteria.creativity    ?? "",
      criteria.impact        ?? "",
      `"${(row.comment || "").replace(/"/g, '""')}"`,
      row.submitted_at,
    ];
    lines.push(cols.join(","));
  }

  res.setHeader("Content-Type", "text/csv");
  res.setHeader("Content-Disposition", "attachment; filename=\"dogfood-scores.csv\"");
  res.send(lines.join("\n"));
});

// ---------- START ----------
app.listen(8080, "0.0.0.0", () => {
  console.log("DOGFOOD running on http://localhost:8080");
});
