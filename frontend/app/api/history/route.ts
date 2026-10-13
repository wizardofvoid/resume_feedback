import { getCurrentUser } from "@/lib/supabase/auth";
import { isSupabaseConfigured } from "@/lib/supabase/config";
import { createClient } from "@/lib/supabase/server";

export const runtime = "nodejs";

async function authorize() {
  if (!isSupabaseConfigured()) {
    return { response: Response.json({ detail: "Authentication is not configured." }, { status: 503 }) };
  }

  const user = await getCurrentUser();
  if (!user) {
    return { response: Response.json({ detail: "Log in to access scan history." }, { status: 401 }) };
  }

  const supabase = await createClient();
  if (!supabase) {
    return { response: Response.json({ detail: "Database is not configured." }, { status: 503 }) };
  }

  return { user, supabase };
}

export async function GET() {
  const auth = await authorize();
  if ("response" in auth) return auth.response;

  const { data, error } = await auth.supabase
    .from("resume_analyses")
    .select("id, created_at, ats_score, resume_name, contact_email, contact_phone")
    .eq("user_id", auth.user.id)
    .order("created_at", { ascending: false })
    .limit(20);

  if (error) {
    console.error("Failed to load resume history:", error.message);
    return Response.json({ detail: "Scan history could not be loaded." }, { status: 500 });
  }

  return Response.json({
    history: (data ?? []).map((item) => ({
      id: item.id,
      created_at: item.created_at,
      score: item.ats_score,
      resume_name: item.resume_name,
      email: item.contact_email,
      phone: item.contact_phone,
    })),
  });
}

export async function DELETE() {
  const auth = await authorize();
  if ("response" in auth) return auth.response;

  const { error } = await auth.supabase.from("resume_analyses").delete().eq("user_id", auth.user.id);

  if (error) {
    console.error("Failed to clear resume history:", error.message);
    return Response.json({ detail: "Scan history could not be cleared." }, { status: 500 });
  }

  return Response.json({ status: "cleared" });
}
