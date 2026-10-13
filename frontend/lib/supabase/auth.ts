import { createClient } from "./server";

export type AuthIdentity = {
  id: string;
  email: string;
};

export async function getCurrentUser(): Promise<AuthIdentity | null> {
  const supabase = await createClient();
  if (!supabase) return null;

  const { data, error } = await supabase.auth.getClaims();
  const claims = data?.claims;

  if (error || !claims || typeof claims.sub !== "string") return null;

  return {
    id: claims.sub,
    email: typeof claims.email === "string" ? claims.email : "Signed in",
  };
}
