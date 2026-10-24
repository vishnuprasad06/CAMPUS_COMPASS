from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from pathlib import Path
from werkzeug.utils import secure_filename

ROOT = Path(__file__).resolve().parent
UPLOAD_DIR = ROOT / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)
ALLOWED = {".pdf"}

app = Flask(__name__, static_folder="static", static_url_path="/static")
app.config["MAX_CONTENT_LENGTH"] = 30 * 1024 * 1024
CORS(app)  # Restrict origins before production deployment.

@app.get("/")
def home():
    return send_from_directory(ROOT, "index.html")

@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "service": "CAMPUS COMPASS API scaffold"})

@app.get("/api/documents")
def documents():
    # Replace with metadata from your real, institution-filtered document index.
    return jsonify({"documents": [], "message": "RAG document index is not connected yet."})

@app.post("/api/ask")
def ask():
    payload = request.get_json(silent=True) or {}
    question = (payload.get("question") or "").strip()
    institution = (payload.get("institution") or "").strip()
    college_name = (payload.get("college_name") or "").strip()
    if not question:
        return jsonify({"error": "Please provide a question."}), 400
    # Deliberately do not invent a response. Connect your actual RAG functions here.
    return jsonify({
        "answer": (
            "The CAMPUS COMPASS UI is connected to the Python API, but the RAG model and "
            "institution-specific document retrieval have not been connected yet. Add your "
            "existing retrieval and Gemini generation functions before asking for official rules."
        ),
        "citations": [],
        "institution": institution,
        "college_name": college_name,
        "connected": False
    })

@app.post("/api/upload")
def upload():
    institution = (request.form.get("institution") or "").strip()
    college_name = (request.form.get("college_name") or "").strip()
    category = (request.form.get("category") or "other").strip()
    files = request.files.getlist("files")
    if not institution:
        return jsonify({"error": "Select an institution before uploading."}), 400
    if institution == "other" and not college_name:
        return jsonify({"error": "Enter the other college's name."}), 400
    if not files:
        return jsonify({"error": "Choose at least one PDF."}), 400
    # Safe per-institution folders. Actual parsing/indexing still needs RAG integration.
    folder_key = secure_filename(institution + "_" + (college_name if institution == "other" else institution)) or "unknown"
    target_dir = UPLOAD_DIR / folder_key / secure_filename(category)
    target_dir.mkdir(parents=True, exist_ok=True)
    saved = []
    for f in files:
        filename = secure_filename(f.filename or "")
        if not filename or Path(filename).suffix.lower() not in ALLOWED:
            return jsonify({"error": "Only PDF files are accepted."}), 400
        destination = target_dir / filename
        f.save(destination)
        saved.append(filename)
    return jsonify({
        "message": f"Saved {len(saved)} PDF file(s), but they have NOT been indexed. Connect the RAG indexing function to complete ingestion.",
        "saved_files": saved,
        "institution": institution,
        "college_name": college_name,
        "category": category,
        "indexed": False
    }), 202

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
