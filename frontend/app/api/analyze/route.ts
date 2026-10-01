import { backendFetch, backendUnavailable, relay } from "@/lib/server/backend";

export const runtime = "nodejs";

export async function POST(request: Request) {
  try {
    const formData = await request.formData();
    const file = formData.get("file");

    if (!(file instanceof File)) {
      return Response.json({ detail: "A resume file is required." }, { status: 400 });
    }

    if (file.size > 10 * 1024 * 1024) {
      return Response.json({ detail: "Resume files must be 10 MB or smaller." }, { status: 413 });
    }

    return relay(
      await backendFetch("/analyze", {
        method: "POST",
        body: formData,
      }),
    );
  } catch (error) {
    return backendUnavailable(error);
  }
}
