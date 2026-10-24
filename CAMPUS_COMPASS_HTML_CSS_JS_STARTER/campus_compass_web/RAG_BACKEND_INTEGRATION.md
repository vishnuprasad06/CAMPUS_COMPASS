# Connect this frontend to your existing Colab RAG notebook

The frontend is ready, but it does not know the variable/function names in your current notebook. Those must be wired in deliberately.

## Recommended integration contract

The browser sends `POST /api/ask` JSON:
```json
{
  "question": "What is the minimum attendance required?",
  "institution": "upgrad",
  "college_name": "",
  "institution_name": "UpGrad School of Technology, Tumakuru",
  "category": "academic"
}
```

Return JSON like:
```json
{
  "answer": "The uploaded regulation states ...",
  "citations": [
    {
      "filename": "Classroom Conduct and Attendance.pdf",
      "page": 1,
      "category": "academic",
      "excerpt": "The supporting passage from the PDF..."
    }
  ]
}
```

## Where to connect your notebook

In your existing notebook, locate the functions/variables for:
1. PDF extraction and chunking
2. Embedding the chunks
3. Retrieving top passages for a question
4. Calling Gemini with the question and retrieved passages

Move these into a Python module such as `rag_service.py`, or import/call them from `app.py`. Replace the body of `ask()` with:
- Validate the institution and question.
- Search only the chosen institution's index.
- If no relevant passage is found, return a clear "not found in the uploaded documents" response.
- Generate an answer only from retrieved passages.
- Return citations with source filename/page/excerpt.

Replace the body of `upload()` so that after saving a PDF it:
- extracts text and page numbers,
- chunks and embeds the text,
- adds the vectors/metadata only to the selected institution's index,
- returns success only after indexing completes.

Replace `documents()` so it returns actual indexed metadata for the selected institution. The frontend currently calls it with `GET /api/documents`; add the institution and college name as query parameters if needed, and update `script.js` accordingly.

## Important security and correctness notes
- Do not put `GOOGLE_API_KEY` in HTML or JavaScript.
- A frontend dropdown does not provide data isolation by itself. The backend must enforce institution-specific retrieval filters.
- For a Colab demo, you can expose a running Flask API using a tunnel, but the tunnel URL and runtime can change. A temporary tunnel is not a permanent production deployment.
- The included API scaffold deliberately returns an explanatory placeholder instead of a fabricated campus rule.
