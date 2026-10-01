import { backendFetch, backendUnavailable, relay } from "@/lib/server/backend";

export const runtime = "nodejs";

export async function GET() {
  try {
    return relay(await backendFetch("/history"));
  } catch (error) {
    return backendUnavailable(error);
  }
}

export async function DELETE() {
  try {
    return relay(await backendFetch("/clear_history", { method: "POST" }));
  } catch (error) {
    return backendUnavailable(error);
  }
}
