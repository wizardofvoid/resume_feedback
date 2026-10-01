# Glance frontend

Standalone Next.js frontend for the Resume Feedback FastAPI service.

## Run locally

Start the existing backend from the repository root:

```powershell
python -m uvicorn backend.api:app --port 8000
```

Then start the frontend:

```powershell
cd frontend
Copy-Item .env.example .env.local
npm install
npm run dev
```

Open `http://localhost:3000`.

`BACKEND_API_URL` is server-only. Browser requests go through the frontend's
same-origin `/api/analyze` and `/api/history` route handlers, so the existing
FastAPI application does not need CORS changes.

## Production

Set `BACKEND_API_URL` to the private or public URL of the deployed FastAPI
service, then run:

```powershell
npm run build
npm start
```
