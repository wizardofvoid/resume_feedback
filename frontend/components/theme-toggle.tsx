"use client";

import { MoonIcon, SunIcon } from "./icons";

export function ThemeToggle() {
  function toggleTheme() {
    const next = document.documentElement.dataset.theme !== "dark";
    document.documentElement.dataset.theme = next ? "dark" : "light";
    window.localStorage.setItem("glance-theme", next ? "dark" : "light");
  }

  return (
    <button className="icon-button" type="button" onClick={toggleTheme} aria-label="Toggle color theme">
      <MoonIcon className="theme-icon theme-icon-dark" />
      <SunIcon className="theme-icon theme-icon-light" />
    </button>
  );
}
