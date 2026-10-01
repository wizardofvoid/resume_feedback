# Glance

Glance analyzes a PDF or DOCX resume against a job description and turns the result into a concise ATS score, skill-gap breakdown, and actionable feedback.

The repository contains one frontend and one backend:

- `frontend/` — Next.js 16 and React 19 interface
- `backend/` — FastAPI API, resume parsing, scoring, Gemini feedback, and local SQLite persistence

The login screen is currently visual only. Authentication and hosted persistence will be connected later through Supabase.

## Local setup

Prerequisites: Node.js, npm, Python 3.11+, and a Python virtual environment.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m spacy download en_core_web_md
npm --prefix frontend install
Copy-Item .env.example .env
Copy-Item frontend/.env.example frontend/.env.local
```

Add a Gemini API key to `.env` if you want AI-generated feedback:

```dotenv
GOOGLE_API_KEY=your_key_here
```

The core analyzer still works without the key. OCR for scanned files additionally requires Tesseract and Poppler on the system path.

## Run

Start both applications with:

```powershell
./run.ps1
```

On macOS or Linux:

```bash
./run.sh
```

Glance opens at `http://localhost:3000`; FastAPI runs at `http://localhost:8000`.

To run the processes separately:

```powershell
python -m uvicorn backend.api:app --port 8000
npm --prefix frontend run dev
```

`BACKEND_API_URL` is server-only. The frontend defaults to `http://127.0.0.1:8000` and proxies browser requests through its own `/api` routes.

## Project structure

```text
backend/
  api.py                  FastAPI endpoints
  data/skills_list.json   known skills catalogue
  database/db.py          local SQLite schema and queries
  parsers/                resume and job-description extraction
  scoring/                ATS and skill matching logic
frontend/
  app/                    routes and API proxies
  components/             interface components
  lib/                    shared frontend helpers and types
requirements.txt          Python dependencies
run.ps1 / run.sh          local two-process launchers
```

The local database is created at `backend/database/data/app.db`. It is runtime data and is intentionally ignored by Git.

## Checks

```powershell
npm --prefix frontend run lint
npm --prefix frontend run build
python -m compileall backend
```

## License

[MIT](LICENSE)
