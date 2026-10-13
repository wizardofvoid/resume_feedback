"use client";

import { FormEvent, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { createClient } from "@/lib/supabase/client";
import { ArrowIcon } from "./icons";

type FieldErrors = {
  email: string;
  password: string;
};

type AuthMode = "login" | "signup";
type PendingAction = "email" | "google" | "recovery" | null;
type Notice = { tone: "error" | "success"; message: string } | null;

const EMPTY_ERRORS: FieldErrors = { email: "", password: "" };

function emailError(value: string) {
  if (!value.trim()) return "Enter your email address.";
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) return "Enter a valid email address.";
  return "";
}

function passwordError(value: string) {
  if (!value) return "Enter your password.";
  if (value.length < 8) return "Use at least 8 characters.";
  return "";
}

export function LoginForm({ initialMessage = "" }: { initialMessage?: string }) {
  const router = useRouter();
  const emailRef = useRef<HTMLInputElement>(null);
  const passwordRef = useRef<HTMLInputElement>(null);
  const [mode, setMode] = useState<AuthMode>("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [errors, setErrors] = useState<FieldErrors>(EMPTY_ERRORS);
  const [pending, setPending] = useState<PendingAction>(null);
  const [notice, setNotice] = useState<Notice>(
    initialMessage ? { tone: "error", message: initialMessage } : null,
  );

  function getClient() {
    const supabase = createClient();
    if (!supabase) {
      setNotice({
        tone: "error",
        message: "Supabase is not configured yet. Add the project URL and publishable key to frontend/.env.local.",
      });
    }
    return supabase;
  }

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const nextErrors = {
      email: emailError(email),
      password: passwordError(password),
    };
    setErrors(nextErrors);
    setNotice(null);

    if (nextErrors.email) {
      emailRef.current?.focus();
      return;
    }
    if (nextErrors.password) {
      passwordRef.current?.focus();
      return;
    }

    const supabase = getClient();
    if (!supabase) return;

    setPending("email");

    if (mode === "login") {
      const { error } = await supabase.auth.signInWithPassword({ email, password });
      if (error) {
        setNotice({ tone: "error", message: error.message });
        setPending(null);
        return;
      }

      router.replace("/");
      router.refresh();
      return;
    }

    const { data, error } = await supabase.auth.signUp({
      email,
      password,
      options: {
        emailRedirectTo: `${window.location.origin}/auth/callback?next=/`,
      },
    });

    if (error) {
      setNotice({ tone: "error", message: error.message });
      setPending(null);
      return;
    }

    if (data.session) {
      router.replace("/");
      router.refresh();
      return;
    }

    setNotice({
      tone: "success",
      message: "Check your inbox to confirm your account, then return here to log in.",
    });
    setPending(null);
  }

  async function continueWithGoogle() {
    const supabase = getClient();
    if (!supabase) return;

    setPending("google");
    setNotice(null);
    const { error } = await supabase.auth.signInWithOAuth({
      provider: "google",
      options: {
        redirectTo: `${window.location.origin}/auth/callback?next=/`,
      },
    });

    if (error) {
      setNotice({ tone: "error", message: error.message });
      setPending(null);
    }
  }

  async function recoverPassword() {
    const nextEmailError = emailError(email);
    setErrors((current) => ({ ...current, email: nextEmailError }));
    if (nextEmailError) {
      emailRef.current?.focus();
      return;
    }

    const supabase = getClient();
    if (!supabase) return;

    setPending("recovery");
    setNotice(null);
    const { error } = await supabase.auth.resetPasswordForEmail(email, {
      redirectTo: `${window.location.origin}/auth/callback?next=/reset-password`,
    });

    setPending(null);
    setNotice(
      error
        ? { tone: "error", message: error.message }
        : { tone: "success", message: "Password reset link sent. Check your inbox." },
    );
  }

  function switchMode() {
    setMode((current) => (current === "login" ? "signup" : "login"));
    setErrors(EMPTY_ERRORS);
    setNotice(null);
  }

  const isLogin = mode === "login";

  return (
    <div className="login-card">
      <div className="login-card-heading">
        <p className="eyebrow"><span /> {isLogin ? "Account access" : "Create your account"}</p>
        <h1 id="login-title">{isLogin ? "Welcome back." : "Start keeping score."}</h1>
        <p>
          {isLogin
            ? "Log in to keep your scans, revisit feedback, and track what improved."
            : "Create an account to keep each scan tied to your progress."}
        </p>
      </div>

      <button
        className="oauth-button"
        type="button"
        disabled={pending !== null}
        onClick={continueWithGoogle}
      >
        <span className="google-mark" aria-hidden="true">G</span>
        {pending === "google" ? "Opening Google…" : "Continue with Google"}
      </button>

      <div className="auth-divider"><span>or use email</span></div>

      <form className="login-form" onSubmit={submit} noValidate>
        <div className="auth-field">
          <label htmlFor="login-email">Email address</label>
          <input
            ref={emailRef}
            id="login-email"
            name="email"
            type="email"
            value={email}
            autoComplete="email"
            placeholder="name@college.edu"
            aria-invalid={Boolean(errors.email)}
            aria-describedby={errors.email ? "login-email-error" : undefined}
            onChange={(event) => {
              setEmail(event.target.value);
              if (errors.email) setErrors((current) => ({ ...current, email: "" }));
            }}
            onBlur={() => setErrors((current) => ({ ...current, email: emailError(email) }))}
          />
          {errors.email && <p className="field-error" id="login-email-error" role="alert">{errors.email}</p>}
        </div>

        <div className="auth-field">
          <div className="auth-label-row">
            <label htmlFor="login-password">Password</label>
            <button
              type="button"
              className="password-toggle"
              onClick={() => setShowPassword((current) => !current)}
              aria-label={`${showPassword ? "Hide" : "Show"} password`}
            >
              {showPassword ? "hide" : "show"}
            </button>
          </div>
          <input
            ref={passwordRef}
            id="login-password"
            name="password"
            type={showPassword ? "text" : "password"}
            value={password}
            autoComplete={isLogin ? "current-password" : "new-password"}
            placeholder="At least 8 characters"
            aria-invalid={Boolean(errors.password)}
            aria-describedby={errors.password ? "login-password-error" : undefined}
            onChange={(event) => {
              setPassword(event.target.value);
              if (errors.password) setErrors((current) => ({ ...current, password: "" }));
            }}
            onBlur={() => setErrors((current) => ({ ...current, password: passwordError(password) }))}
          />
          {errors.password && <p className="field-error" id="login-password-error" role="alert">{errors.password}</p>}
        </div>

        <div className="login-options">
          <span className="session-note">Secure, cookie-backed session</span>
          {isLogin && (
            <button
              className="password-recovery"
              type="button"
              disabled={pending !== null}
              onClick={recoverPassword}
            >
              {pending === "recovery" ? "Sending…" : "Forgot password?"}
            </button>
          )}
        </div>

        <button className="primary-button login-submit" type="submit" disabled={pending !== null}>
          <span>{pending === "email" ? "Working…" : isLogin ? "Log in" : "Create account"}</span>
          <ArrowIcon />
        </button>
      </form>

      <div className={`auth-notice${notice ? ` is-${notice.tone}` : ""}`} aria-live="polite">
        {notice && <p>{notice.message}</p>}
      </div>

      <p className="signup-note">
        {isLogin ? "New to Glance?" : "Already have an account?"}{" "}
        <button type="button" onClick={switchMode} disabled={pending !== null}>
          {isLogin ? "Create an account" : "Log in"}
        </button>
      </p>
    </div>
  );
}
