import type { Metadata } from "next";
import { BrandWordmark } from "@/components/brand-wordmark";
import { LoginForm } from "@/components/login-form";
import { SiteHeader } from "@/components/site-header";

export const metadata: Metadata = {
  title: "Log in — Glance",
  description: "Log in to revisit your resume analyses and feedback.",
};

export default function LoginPage() {
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
            <p>Your authentication and saved account data will live in Supabase once the backend connection is added.</p>
          </div>
        </aside>

        <LoginForm />
      </section>

      <footer className="auth-footer shell">
        <BrandWordmark />
        <p>Your credentials are not transmitted in this frontend-only version.</p>
      </footer>
    </main>
  );
}
