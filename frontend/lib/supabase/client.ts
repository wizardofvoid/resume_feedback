import { createBrowserClient } from "@supabase/ssr";
import type { SupabaseClient } from "@supabase/supabase-js";
import { getSupabaseConfig } from "./config";

let browserClient: SupabaseClient | null | undefined;

export function createClient() {
  if (browserClient !== undefined) return browserClient;

  const config = getSupabaseConfig();
  browserClient = config
    ? createBrowserClient(config.url, config.publishableKey)
    : null;

  return browserClient;
}
