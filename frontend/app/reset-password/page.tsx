import type { Metadata } from "next";
import { BrandWordmark } from "@/components/brand-wordmark";
import { ResetPasswordForm } from "@/components/reset-password-form";
import { SiteHeader } from "@/components/site-header";

export const metadata: Metadata = {
  title: "Reset password — Glance",
  description: "Choose a new password for your Glance account.",
};

export default function ResetPasswordPage() {
  return (
    <main className="auth-shell">
      <SiteHeader />
      <section className="auth-page auth-page-single shell" aria-labelledby="reset-title">
        <ResetPasswordForm />
      </section>
      <footer className="auth-footer shell">
        <BrandWordmark />
        <p>Your new password is securely handled by Supabase.</p>
      </footer>
    </main>
  );
}
