#!/usr/bin/env python3
"""Local dashboard server: serves this folder statically + job-deletion API.

Usage:
    python3 server.py [port]      # default 8000, then open http://localhost:8000/

API:
    DELETE /api/jobs/<id>  -> deletes the job row and its contacts rows
                              (contacts.job_id = id). Returns JSON.
    PATCH  /api/jobs/<id>  -> JSON body {"applied": true|false}; flips the
                              job's applied flag. Returns JSON.

The static viewer (index.html) keeps reading jobs.db via sql.js; after a
successful DELETE/PATCH it re-fetches jobs.db so the UI stays in sync.
"""
import json
import os
import re
import sqlite3
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, "jobs.db")


class Handler(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):  # quieter logging
        print(f"[{self.log_date_time_string()}] {self.command} {self.path} ->", fmt % args)

    def _send_json(self, code, obj):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_DELETE(self):
        m = re.fullmatch(r"/api/jobs/(\d+)", urlparse(self.path).path)
        if not m:
            return self._send_json(404, {"ok": False, "error": "unknown endpoint"})
        job_id = int(m.group(1))
        if not os.path.exists(DB):
            return self._send_json(404, {"ok": False, "error": "jobs.db not found"})
        try:
            conn = sqlite3.connect(DB)
            cur = conn.cursor()
            row = cur.execute("SELECT id, title, company FROM jobs WHERE id=?", (job_id,)).fetchone()
            if not row:
                conn.close()
                return self._send_json(404, {"ok": False, "error": f"job {job_id} not found"})
            contacts_deleted = 0
            try:
                cur.execute("DELETE FROM contacts WHERE job_id=?", (job_id,))
                contacts_deleted = cur.rowcount
            except sqlite3.Error:
                pass  # contacts table may be absent in old DBs
            cur.execute("DELETE FROM jobs WHERE id=?", (job_id,))
            conn.commit()
            conn.close()
            return self._send_json(200, {
                "ok": True, "deleted_id": job_id,
                "title": row[1], "company": row[2],
                "contacts_deleted": contacts_deleted,
            })
        except sqlite3.Error as e:
            return self._send_json(500, {"ok": False, "error": str(e)})

    def do_PATCH(self):
        m = re.fullmatch(r"/api/jobs/(\d+)", urlparse(self.path).path)
        if not m:
            return self._send_json(404, {"ok": False, "error": "unknown endpoint"})
        job_id = int(m.group(1))
        if not os.path.exists(DB):
            return self._send_json(404, {"ok": False, "error": "jobs.db not found"})
        try:
            length = int(self.headers.get("Content-Length") or 0)
            payload = json.loads(self.rfile.read(length).decode("utf-8") or "{}")
        except (ValueError, json.JSONDecodeError):
            return self._send_json(400, {"ok": False, "error": "invalid JSON body"})
        if "applied" not in payload:
            return self._send_json(400, {"ok": False, "error": 'body must contain "applied"'})
        applied = 1 if payload["applied"] in (True, 1, "1", "true") else 0
        try:
            conn = sqlite3.connect(DB)
            cur = conn.cursor()
            try:
                cur.execute("ALTER TABLE jobs ADD COLUMN applied INTEGER NOT NULL DEFAULT 0")
            except sqlite3.Error:
                pass  # column already exists
            cur.execute("UPDATE jobs SET applied=? WHERE id=?", (applied, job_id))
            if cur.rowcount == 0:
                conn.close()
                return self._send_json(404, {"ok": False, "error": f"job {job_id} not found"})
            row = cur.execute("SELECT title, company FROM jobs WHERE id=?", (job_id,)).fetchone()
            conn.commit()
            conn.close()
            return self._send_json(200, {
                "ok": True, "id": job_id, "applied": applied,
                "title": row[0], "company": row[1],
            })
        except sqlite3.Error as e:
            return self._send_json(500, {"ok": False, "error": str(e)})

    # No-cache jobs.db so Refresh / auto-refresh always sees fresh rows.
    def end_headers(self):
        if urlparse(self.path).path.endswith("jobs.db"):
            self.send_header("Cache-Control", "no-store")
        super().end_headers()


if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    os.chdir(BASE)
    srv = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"Serving {BASE} at http://localhost:{port}/  (DELETE + PATCH /api/jobs/<id> enabled)")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
