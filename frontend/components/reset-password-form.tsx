"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import { createClient } from "@/lib/supabase/client";
import { ArrowIcon } from "./icons";

export function ResetPasswordForm() {
  const router = useRouter();
  const [password, setPassword] = useState("");
  const [confirmation, setConfirmation] = useState("");
  const [error, setError] = useState("");
  const [pending, setPending] = useState(false);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");

    if (password.length < 8) {
      setError("Use at least 8 characters.");
      return;
    }
    if (password !== confirmation) {
      setError("The passwords do not match.");
      return;
    }

    const supabase = createClient();
    if (!supabase) {
      setError("Supabase is not configured.");
      return;
    }

    setPending(true);
    const { error: updateError } = await supabase.auth.updateUser({ password });
    if (updateError) {
      setError(updateError.message);
      setPending(false);
      return;
    }

    router.replace("/");
    router.refresh();
  }

  return (
    <div className="login-card">
      <div className="login-card-heading">
        <p className="eyebrow"><span /> Account recovery</p>
        <h1 id="reset-title">Choose a new password.</h1>
        <p>Use something unique that you do not use for another account.</p>
      </div>

      <form className="login-form reset-form" onSubmit={submit}>
        <div className="auth-field">
          <label htmlFor="new-password">New password</label>
          <input
            id="new-password"
            type="password"
            autoComplete="new-password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            placeholder="At least 8 characters"
          />
        </div>
        <div className="auth-field">
          <label htmlFor="confirm-password">Confirm password</label>
          <input
            id="confirm-password"
            type="password"
            autoComplete="new-password"
            value={confirmation}
            onChange={(event) => setConfirmation(event.target.value)}
            placeholder="Repeat your password"
          />
        </div>

        {error && <p className="field-error" role="alert">{error}</p>}

        <button className="primary-button login-submit" type="submit" disabled={pending}>
          <span>{pending ? "Updating…" : "Update password"}</span>
          <ArrowIcon />
        </button>
      </form>
    </div>
  );
}
