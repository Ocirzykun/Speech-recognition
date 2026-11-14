import sqlite3
from datetime import datetime
from flask import Flask, jsonify, request, render_template, Response

app = Flask(__name__)
DB = "transcripts.db"


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS transcripts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                language TEXT NOT NULL,
                created_at TEXT NOT NULL
            )"""
        )


@app.route("/")
def index():
    return render_template("index.html")


@app.get("/api/transcripts")
def list_transcripts():
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM transcripts ORDER BY id DESC"
        ).fetchall()
    return jsonify([dict(r) for r in rows])


@app.post("/api/transcripts")
def add_transcript():
    data = request.get_json(force=True)
    text = (data.get("text") or "").strip()
    if not text:
        return jsonify({"error": "Empty text"}), 400
    language = data.get("language", "en-US")
    created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_db() as conn:
        cur = conn.execute(
            "INSERT INTO transcripts (text, language, created_at) VALUES (?, ?, ?)",
            (text, language, created),
        )
        new_id = cur.lastrowid
    return jsonify({"id": new_id, "text": text, "language": language,
                    "created_at": created}), 201


@app.delete("/api/transcripts/<int:tid>")
def delete_transcript(tid):
    with get_db() as conn:
        conn.execute("DELETE FROM transcripts WHERE id = ?", (tid,))
    return jsonify({"deleted": tid})


@app.get("/api/export")
def export_transcripts():
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM transcripts ORDER BY id ASC"
        ).fetchall()
    body = "\n".join(f"[{r['created_at']}] {r['text']}" for r in rows)
    return Response(
        body,
        mimetype="text/plain",
        headers={"Content-Disposition": "attachment; filename=transcripts.txt"},
    )


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
