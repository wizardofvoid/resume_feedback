import { backendFetch, backendUnavailable, relay } from "@/lib/server/backend";
import { getCurrentUser } from "@/lib/supabase/auth";
import { isSupabaseConfigured } from "@/lib/supabase/config";
import { createClient } from "@/lib/supabase/server";
import type { AnalysisResult } from "@/lib/types";

export const runtime = "nodejs";

export async function POST(request: Request) {
  if (!isSupabaseConfigured()) {
    return Response.json({ detail: "Authentication is not configured." }, { status: 503 });
  }
  const user = await getCurrentUser();
  if (!user) {
    return Response.json({ detail: "Log in before analyzing a resume." }, { status: 401 });
  }

  try {
    const formData = await request.formData();
    const file = formData.get("file");

    if (!(file instanceof File)) {
      return Response.json({ detail: "A resume file is required." }, { status: 400 });
    }

    if (file.size > 10 * 1024 * 1024) {
      return Response.json({ detail: "Resume files must be 10 MB or smaller." }, { status: 413 });
    }

    const backendResponse = await backendFetch("/analyze", {
      method: "POST",
      body: formData,
    });

    if (!backendResponse.ok) return relay(backendResponse);

    const analysis = (await backendResponse.json()) as AnalysisResult;
    const supabase = await createClient();

    if (!supabase) {
      return Response.json({
        ...analysis,
        persistence_warning: "Your analysis was completed but could not be saved.",
      });
    }

    const { error: persistenceError } = await supabase.from("resume_analyses").insert({
      user_id: user.id,
      resume_name: file.name,
      contact_email: analysis.contact_info?.email || null,
      contact_phone: analysis.contact_info?.phone || null,
      ats_score: analysis.ats_score,
      skill_match_score: analysis.skill_match_score,
      format_score: analysis.format_score,
      found_skills: analysis.found_skills,
      missing_skills: analysis.missing_skills,
      job_skill_weights: analysis.job_skill_weights,
      ai_feedback: analysis.ai_feedback,
      quality_analysis: analysis.quality_analysis ?? {},
    });

    if (persistenceError) {
      console.error("Failed to persist resume analysis:", persistenceError.message);
      return Response.json({
        ...analysis,
        persistence_warning: "Your analysis was completed but could not be saved to history.",
      });
    }

    return Response.json(analysis);
  } catch (error) {
    return backendUnavailable(error);
  }
}
