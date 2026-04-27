from datetime import datetime
from html import escape
import os
from pathlib import Path

from flask import Flask, abort, jsonify, redirect, request, send_from_directory, url_for
from werkzeug.utils import secure_filename


BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = Path(os.environ.get("UPLOAD_DIR", BASE_DIR / "uploads"))
UPLOAD_TOKEN = os.environ.get("UPLOAD_TOKEN", "")
MAX_UPLOAD_MB = int(os.environ.get("MAX_UPLOAD_MB", "25"))
ALLOWED_EXTENSIONS = {"pdf", "txt"}

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_MB * 1024 * 1024
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

DELETE_PASSWORD = "1234"


def is_allowed(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def require_token():
    if not UPLOAD_TOKEN:
        return

    token = request.headers.get("X-Upload-Token") or request.form.get("token")
    if token != UPLOAD_TOKEN:
        abort(401, "Invalid upload token.")


def stored_filename(filename):
    clean_name = secure_filename(filename) or "upload.pdf"
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{timestamp}-{clean_name}"


@app.get("/")
def index():
    files = sorted(
        [path for path in UPLOAD_DIR.iterdir() if path.is_file() and path.name != ".gitkeep"],
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )

    rows = "\n".join(
        f'<li><a href="/files/{escape(path.name)}">{escape(path.name)}</a> '
        f'<span>{path.stat().st_size} bytes</span></li>'
        for path in files
    )
    if not rows:
        rows = "<li>Aucun fichier recu.</li>"

    return f"""<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Pico upload</title>
  <style>
    body {{ font-family: sans-serif; max-width: 760px; margin: 48px auto; padding: 0 20px; }}
    form {{ display: flex; gap: 8px; align-items: center; margin-bottom: 28px; }}
    li {{ margin: 10px 0; }}
    span {{ color: #666; font-size: 0.9rem; }}
  </style>
</head>
<body>
<form action="/delete-all" method="post"
      style="display:flex; gap:8px; align-items:center; margin-bottom:28px;">
  <input type="password" name="delete_password"
         placeholder="Mot de passe" required>
  <button type="submit"
          style="background:#c0392b; color:white; border:none;
                 padding:6px 14px; border-radius:4px; cursor:pointer;">
    🗑 Tout effacer
  </button>
</form>
  <h1>Pico upload</h1>
  <form action="/upload" method="post" enctype="multipart/form-data">
    <input type="file" name="file" accept=".pdf,.txt">
    <button type="submit">Upload</button>
  </form>
  <h2>Fichiers recus</h2>
  <ul>{rows}</ul>
</body>
</html>"""


@app.post("/upload")
def upload():
    require_token()

    uploaded_file = request.files.get("file")
    if uploaded_file is None or uploaded_file.filename == "":
        abort(400, "Missing file field.")

    if not is_allowed(uploaded_file.filename):
        abort(400, "Only PDF and TXT files are accepted.")

    filename = stored_filename(uploaded_file.filename)
    destination = UPLOAD_DIR / filename
    uploaded_file.save(destination)

    return redirect(url_for("index"))

@app.post("/delete-all")
def delete_all():
    password = request.form.get("delete_password", "")

    if not DELETE_PASSWORD or password != DELETE_PASSWORD:
        abort(401, "Mot de passe incorrect.")

    deleted = 0
    for path in UPLOAD_DIR.iterdir():
        if path.is_file() and path.name != ".gitkeep":
            path.unlink()
            deleted += 1

    return redirect(url_for("index"))


@app.get("/files/<path:filename>")
def files(filename):
    return send_from_directory(UPLOAD_DIR, filename, as_attachment=False)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
