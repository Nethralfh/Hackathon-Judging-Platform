/**
 * src/routes/pages.js
 *
 * All server-rendered page routes for DOGFOOD.
 * Returns HTML via EJS templates rendered through the shared layout.
 * Auth is only used for UI personalisation — enforcement stays in the backend API routes.
 */

"use strict";

const express = require("express");
const ejs     = require("ejs");
const path    = require("path");
const fs      = require("fs");

const router = express.Router();

// ---------- Layout renderer helper ----------
// Renders a view into the shared layout and sends the full HTML page.
async function renderPage(res, viewPath, locals) {
  const { title, currentUser, currentPath, ...viewLocals } = locals;

  // Render the inner view first (pass shared context so views can do role-based UI)
  const body = await ejs.renderFile(viewPath, { currentUser: currentUser || null, currentPath: currentPath || "", ...viewLocals }, { async: true });

  // Then inject into the layout
  // __dirname is src/routes/, so layout is at src/views/partials/layout.ejs
  const layoutPath = path.join(__dirname, "../views/partials/layout.ejs");
  const html       = await ejs.renderFile(layoutPath, {
    title,
    currentUser: currentUser || null,
    currentPath: currentPath || "",
    body,
  }, { async: true });

  res.send(html);
}

// ---------- Route helpers ----------
function getUser(db, req) {
  const cookie = req.headers.cookie || "";
  const match  = cookie.split(";").map(c => c.trim()).find(c => c.startsWith("session="));
  if (!match) return null;
  const token = match.split("=")[1];
  const row   = db.prepare("SELECT * FROM session WHERE token = ?").get(token);
  if (!row) return null;
  return { role: row.role, judgeId: row.judge_id, token };
}

// ---------- Factory: create the page router with db & fixtures injected ----------
module.exports = function createPagesRouter(db, fixtures) {
  // Build track name lookup from fixtures
  const trackNameById = {};
  (fixtures.tracks || []).forEach(t => { trackNameById[t.id] = t.name; });

  // Build judge metadata lookup (name, tracks[]) from fixtures
  const judgeMetaById = {};
  (fixtures.judges || []).forEach(j => {
    judgeMetaById[j.id] = {
      id:     j.id,
      name:   j.name,
      tracks: (j.tracks || []).map(tid => trackNameById[tid] || tid),
    };
  });

  // ------------------------------------------------------------------ //
  // GET /projects — Public Gallery
  // ------------------------------------------------------------------ //
  router.get("/projects", async (req, res) => {
    try {
      const currentUser = getUser(db, req);
      const rows        = db.prepare("SELECT * FROM project ORDER BY submitted_at DESC").all();

      const projects = rows.map(p => ({
        ...p,
        track: trackNameById[p.track] || p.track,
      }));

      // Unique track names for the filter dropdown
      const tracks = [...new Set(projects.map(p => p.track))].sort();

      await renderPage(res, path.join(__dirname, "../views/projects/index.ejs"), {
        title:       "Gallery",
        currentUser,
        currentPath: "/projects",
        projects,
        tracks,
      });
    } catch (err) {
      console.error(err);
      res.status(500).send("Internal server error");
    }
  });

  // ------------------------------------------------------------------ //
  // GET /projects/new — Submission Form
  // ------------------------------------------------------------------ //
  router.get("/projects/new", async (req, res) => {
    try {
      const currentUser = getUser(db, req);

      await renderPage(res, path.join(__dirname, "../views/projects/new.ejs"), {
        title:       "Submit Project",
        currentUser,
        currentPath: "/projects/new",
      });
    } catch (err) {
      console.error(err);
      res.status(500).send("Internal server error");
    }
  });

  // ------------------------------------------------------------------ //
  // GET /projects/:id — Project Detail
  // ------------------------------------------------------------------ //
  router.get("/projects/:id", async (req, res) => {
    try {
      const currentUser = getUser(db, req);
      const row         = db.prepare("SELECT * FROM project WHERE id = ?").get(req.params.id);

      if (!row) return res.status(404).send("Project not found");

      const project = {
        ...row,
        track: trackNameById[row.track] || row.track,
      };

      await renderPage(res, path.join(__dirname, "../views/projects/show.ejs"), {
        title:       project.title,
        currentUser,
        currentPath: `/projects/${project.id}`,
        project,
      });
    } catch (err) {
      console.error(err);
      res.status(500).send("Internal server error");
    }
  });

  // ------------------------------------------------------------------ //
  // GET /judge/dashboard — Judge Scoring View
  // ------------------------------------------------------------------ //
  router.get("/judge/dashboard", async (req, res) => {
    try {
      const currentUser = getUser(db, req);

      // UI nicety: show only this judge's assigned projects.
      // The backend API enforces auth independently; this is display-only.
      if (!currentUser || currentUser.role !== "judge" || !currentUser.judgeId) {
        // Show empty queue for non-judges rather than hard-blocking
        return await renderPage(res, path.join(__dirname, "../views/judge/dashboard.ejs"), {
          title:       "Scoring Queue",
          currentUser,
          currentPath: "/judge/dashboard",
          assignments: [],
        });
      }

      const judgeId   = currentUser.judgeId;
      const judgeMeta = judgeMetaById[judgeId] || { tracks: [] };

      // Find which track IDs this judge covers
      const judgeTrackIds = (fixtures.judges || [])
        .find(j => j.id === judgeId)?.tracks || [];

      // Projects in this judge's tracks
      let assignedProjects = [];
      if (judgeTrackIds.length > 0) {
        const placeholders = judgeTrackIds.map(() => "?").join(",");
        assignedProjects   = db
          .prepare(`SELECT * FROM project WHERE track IN (${placeholders}) ORDER BY title ASC`)
          .all(...judgeTrackIds);
      }

      // Load existing scores for this judge from the score table
      const existingScores = {};
      try {
        const scoreRows = db
          .prepare("SELECT * FROM score WHERE judge_id = ?")
          .all(judgeId);
        scoreRows.forEach(s => { existingScores[s.project_id] = s; });
      } catch (_) {
        // score table might not exist in a minimal setup — gracefully ignore
      }

      const assignments = assignedProjects.map(p => {
        const raw = existingScores[p.id] || null;
        let criteria = null;
        if (raw && raw.criteria_json) {
          try { criteria = JSON.parse(raw.criteria_json); } catch (_) {}
        }
        return {
          project: {
            ...p,
            track: trackNameById[p.track] || p.track,
          },
          existingScore: raw ? { criteria, comment: raw.comment || "" } : null,
        };
      });

      await renderPage(res, path.join(__dirname, "../views/judge/dashboard.ejs"), {
        title:       "Scoring Queue",
        currentUser,
        currentPath: "/judge/dashboard",
        assignments,
      });
    } catch (err) {
      console.error(err);
      res.status(500).send("Internal server error");
    }
  });

  // ------------------------------------------------------------------ //
  // GET /organizer/dashboard — Organizer Progress View
  // ------------------------------------------------------------------ //
  router.get("/organizer/dashboard", async (req, res) => {
    try {
      const currentUser = getUser(db, req);

      // Per-project stats
      const allProjects = db.prepare("SELECT * FROM project ORDER BY title ASC").all();

      let scoreByProject = {};
      try {
        const scoreRows = db.prepare("SELECT * FROM score").all();
        scoreRows.forEach(s => {
          if (!scoreByProject[s.project_id]) scoreByProject[s.project_id] = [];
          scoreByProject[s.project_id].push(s);
        });
      } catch (_) {}

      const projectRows = allProjects.map(p => {
        const scores = scoreByProject[p.id] || [];
        const sums   = scores.map(s => {
          try {
            const c = JSON.parse(s.criteria_json || "{}");
            return Object.values(c).reduce((a, b) => a + (Number(b) || 0), 0);
          } catch (_) { return 0; }
        });
        const avgScore = sums.length > 0
          ? sums.reduce((a, b) => a + b, 0) / sums.length
          : null;

        return {
          id:         p.id,
          title:      p.title,
          track:      trackNameById[p.track] || p.track,
          scoreCount: scores.length,
          avgScore,
        };
      });

      const totalProjects  = projectRows.length;
      const scoredProjects = projectRows.filter(r => r.scoreCount > 0).length;
      const totalScores    = projectRows.reduce((a, r) => a + r.scoreCount, 0);

      // Per-judge review counts
      let reviewsByJudge = {};
      try {
        const scoreRows = db.prepare("SELECT judge_id, COUNT(*) as cnt FROM score GROUP BY judge_id").all();
        scoreRows.forEach(r => { reviewsByJudge[r.judge_id] = r.cnt; });
      } catch (_) {}

      const judgeRows = (fixtures.judges || []).map(j => ({
        id:          j.id,
        name:        j.name,
        tracks:      (j.tracks || []).map(tid => trackNameById[tid] || tid),
        reviewCount: reviewsByJudge[j.id] || 0,
      })).sort((a, b) => b.reviewCount - a.reviewCount);

      await renderPage(res, path.join(__dirname, "../views/organizer/dashboard.ejs"), {
        title:       "Organizer Dashboard",
        currentUser,
        currentPath: "/organizer/dashboard",
        stats:       { totalProjects, scoredProjects, totalScores },
        projectRows,
        judgeRows,
      });
    } catch (err) {
      console.error(err);
      res.status(500).send("Internal server error");
    }
  });

  return router;
};
