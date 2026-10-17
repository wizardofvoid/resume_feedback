# Glance

Glance analyzes a PDF or DOCX resume against a job description and turns the result into a concise ATS score, skill-gap breakdown, and actionable feedback.

The repository contains one frontend and one backend:

- `frontend/` — Next.js 16, React 19, and Supabase Auth interface
- `backend/` — stateless FastAPI service for resume parsing, scoring, and Gemini feedback

Supabase provides authentication and per-user PostgreSQL analysis history. Authentication supports email/password, account confirmation, password recovery, Google OAuth, and cookie-backed sessions.

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

## Supabase authentication

Create a free Supabase project, then copy its Project URL and publishable key from the project **Connect** dialog into `frontend/.env.local`:

```dotenv
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY=your-publishable-key
```

In Supabase Authentication URL settings, set the local Site URL to `http://localhost:3000` and allow `http://localhost:3000/**` as a redirect URL. Email/password auth is enabled by default.

For server-rendered email confirmation, set the Confirm signup email template link to:

```text
{{ .SiteURL }}/auth/confirm?token_hash={{ .TokenHash }}&type=email
```

Google login additionally requires enabling the Google provider in Supabase and adding the callback URL shown on that provider page to the Google Cloud OAuth client.

## Supabase database

Open the Supabase SQL Editor, create a new query, paste the contents of
`supabase/migrations/202610060001_create_resume_analyses.sql`, and run it once.

The migration creates the `resume_analyses` table, enables row-level security, and grants authenticated users access only to rows that belong to their own account. Resume files and full extracted resume text are not stored; Glance keeps the filename, extracted contact details, scores, skill results, and feedback needed for history.

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

The Next.js analyze and history routes require a verified Supabase session. Next.js writes history with that user's session, so Supabase row-level security remains the authorization boundary. FastAPI is stateless and only returns the analysis result.

## Project structure

```text
backend/
  api.py                  FastAPI endpoints
  data/skills_list.json   known skills catalogue
  parsers/                resume and job-description extraction
  scoring/                ATS and skill matching logic
frontend/
  app/                    routes and API proxies
  components/             interface components
  lib/                    shared frontend helpers and types
supabase/
  migrations/             versioned PostgreSQL schema and RLS policies
requirements.txt          Python dependencies
run.ps1 / run.sh          local two-process launchers
```

## Checks

```powershell
npm --prefix frontend run lint
npm --prefix frontend run typecheck
npm --prefix frontend run build
npm --prefix frontend audit --omit=dev --audit-level=high
python -m compileall backend
```

## Continuous integration

GitHub Actions runs `.github/workflows/ci.yml` for every pull request into `main`, every push to `main`, and manual runs from the Actions tab. Its independent frontend and backend jobs install dependencies in clean Linux environments and run the checks listed above. The backend job also runs `pip check` to detect incompatible Python packages.

Automatic deployment is intentionally not configured yet. Once the Render backend and Vercel frontend exist, they can deploy the `main` branch only after these CI checks pass.

## License

[MIT](LICENSE)
