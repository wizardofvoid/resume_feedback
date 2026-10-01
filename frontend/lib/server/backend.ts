const BACKEND_API_URL = process.env.BACKEND_API_URL ?? "http://127.0.0.1:8000";

export async function backendFetch(path: string, init?: RequestInit) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 120_000);

  try {
    return await fetch(`${BACKEND_API_URL}${path}`, {
      ...init,
      cache: "no-store",
      signal: controller.signal,
    });
  } finally {
    clearTimeout(timeout);
  }
}

export async function relay(response: Response) {
  const contentType = response.headers.get("content-type") ?? "application/json";
  const body = await response.text();
  return new Response(body, {
    status: response.status,
    headers: { "content-type": contentType },
  });
}

export function backendUnavailable(reason: unknown) {
  const timedOut = reason instanceof Error && reason.name === "AbortError";
  return Response.json(
    {
      detail: timedOut
        ? "Analysis timed out. Try a smaller file or try again."
        : "The analysis service is unavailable. Confirm that FastAPI is running.",
    },
    { status: timedOut ? 504 : 503 },
  );
}
