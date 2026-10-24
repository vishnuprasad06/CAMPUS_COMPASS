# CAMPUS COMPASS — HTML/CSS/JS frontend + Python API scaffold

This is a standalone frontend and a minimal Flask API scaffold intended to be connected to your existing Colab RAG functions.

## Files
- `index.html`: application interface
- `static/style.css`: responsive design, high-contrast black text, SSIT orange / UpGrad red theme switching
- `static/script.js`: navigation, question submission, institution selection, upload requests, source display
- `app.py`: minimal API scaffold; deliberately does not fabricate AI answers
- `requirements.txt`: Python dependencies
- `RAG_BACKEND_INTEGRATION.md`: instructions to connect your existing RAG notebook

## Run the UI locally
1. Install Python 3.10+.
2. In this folder, run `pip install -r requirements.txt`.
3. Run `python app.py`.
4. Open `http://127.0.0.1:8000`.

The starter API returns a clear "not connected" response for questions until you wire in your actual embedding, retrieval and generation functions. It does not pretend to answer from PDFs.

## Connect the existing RAG
See `RAG_BACKEND_INTEGRATION.md`. Never place your Google API key in `static/script.js`.
