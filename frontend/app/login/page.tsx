import type { Metadata } from "next";
import { redirect } from "next/navigation";
import { BrandWordmark } from "@/components/brand-wordmark";
import { LoginForm } from "@/components/login-form";
import { SiteHeader } from "@/components/site-header";
import { getCurrentUser } from "@/lib/supabase/auth";

export const metadata: Metadata = {
  title: "Log in — Glance",
  description: "Log in to revisit your resume analyses and feedback.",
};

export default async function LoginPage({
  searchParams,
}: {
  searchParams: Promise<{ message?: string; mode?: string }>;
}) {
  const [user, params] = await Promise.all([getCurrentUser(), searchParams]);
  if (user) redirect("/");

  return (
    <main className="auth-shell">
      <a className="skip-link" href="#auth-content">Skip to login</a>
      <SiteHeader />

      <section className="auth-page shell" id="auth-content" aria-labelledby="login-title">
        <aside className="auth-story" aria-label="Why create a Glance account">
          <p className="eyebrow"><span /> One account, every scan</p>
          <h2>Your progress should be easier to see than your mistakes.</h2>
          <p>
            Return to past scans, compare your improvements, and keep the role-specific advice that matters.
          </p>
          <div className="auth-story-note">
            <span>Built for continuity</span>
            <p>Supabase protects each signed-in session, while your saved scan history stays private to your account.</p>
          </div>
        </aside>

        <LoginForm
          initialMessage={params.message}
          initialMode={params.mode === "signup" ? "signup" : "login"}
        />
      </section>

      <footer className="auth-footer shell">
        <BrandWordmark />
        <p>Authentication is handled by Supabase. Glance never stores your password.</p>
      </footer>
    </main>
  );
}
