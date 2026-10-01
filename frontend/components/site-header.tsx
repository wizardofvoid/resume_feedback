"use client";

import Link from "next/link";
import { MoonIcon, SunIcon } from "./icons";
import { BrandWordmark } from "./brand-wordmark";

export function SiteHeader() {
  function toggleTheme() {
    const next = document.documentElement.dataset.theme !== "dark";
    document.documentElement.dataset.theme = next ? "dark" : "light";
    window.localStorage.setItem("glance-theme", next ? "dark" : "light");
  }

  return (
    <header className="site-header shell" id="top">
      <Link className="brand" href="/" aria-label="Glance home">
        <BrandWordmark />
      </Link>
      <nav className="header-nav" aria-label="Primary navigation">
        <Link href="/#how-it-works">How it works</Link>
        <Link href="/#history">History</Link>
      </nav>
      <div className="header-meta">
        <button className="icon-button" type="button" onClick={toggleTheme} aria-label="Toggle color theme">
          <MoonIcon className="theme-icon theme-icon-dark" />
          <SunIcon className="theme-icon theme-icon-light" />
        </button>
        <Link className="login-link" href="/login">Log in</Link>
        <Link className="header-cta" href="/#analyze">Scan resume</Link>
      </div>
    </header>
  );
}
