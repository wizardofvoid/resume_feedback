"use client";

import { FormEvent, useRef, useState } from "react";
import { ArrowIcon, CheckIcon } from "./icons";

type FieldErrors = {
  email: string;
  password: string;
};

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

export function LoginForm() {
  const emailRef = useRef<HTMLInputElement>(null);
  const passwordRef = useRef<HTMLInputElement>(null);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [remember, setRemember] = useState(true);
  const [errors, setErrors] = useState<FieldErrors>(EMPTY_ERRORS);
  const [notice, setNotice] = useState("");

  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const nextErrors = {
      email: emailError(email),
      password: passwordError(password),
    };
    setErrors(nextErrors);
    setNotice("");

    if (nextErrors.email) {
      emailRef.current?.focus();
      return;
    }
    if (nextErrors.password) {
      passwordRef.current?.focus();
      return;
    }

    setNotice("The login interface is ready. Supabase authentication will be connected next.");
  }

  return (
    <div className="login-card">
      <div className="login-card-heading">
        <p className="eyebrow"><span /> Account access</p>
        <h1 id="login-title">Welcome back.</h1>
        <p>Log in to keep your scans, revisit feedback, and track what improved.</p>
      </div>

      <button
        className="oauth-button"
        type="button"
        onClick={() => setNotice("Google sign-in will be connected through Supabase.")}
      >
        <span className="google-mark" aria-hidden="true">G</span>
        Continue with Google
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
            autoComplete="current-password"
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
          <label className="remember-check">
            <input type="checkbox" checked={remember} onChange={(event) => setRemember(event.target.checked)} />
            <span className="check-box"><CheckIcon /></span>
            <span>Keep me signed in</span>
          </label>
          <button
            className="password-recovery"
            type="button"
            onClick={() => setNotice("Password recovery will be connected through Supabase.")}
          >
            Forgot password?
          </button>
        </div>

        <button className="primary-button login-submit" type="submit">
          <span>Log in</span>
          <ArrowIcon />
        </button>
      </form>

      <div className="auth-notice" aria-live="polite">
        {notice && <p>{notice}</p>}
      </div>

      <p className="signup-note">
        New to Glance? <button type="button" onClick={() => setNotice("Account creation will be added with Supabase authentication.")}>Create an account</button>
      </p>
    </div>
  );
}
