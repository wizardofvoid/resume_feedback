import Link from "next/link";
import { getCurrentUser } from "@/lib/supabase/auth";
import { BrandWordmark } from "./brand-wordmark";
import { ThemeToggle } from "./theme-toggle";

export async function SiteHeader() {
  const user = await getCurrentUser();

  return (
    <header className="site-header shell" id="top">
      <Link className="brand" href="/" aria-label="Glance home">
        <BrandWordmark />
      </Link>
      <nav className="header-nav" aria-label="Primary navigation">
        <Link href="/#how-it-works">How it works</Link>
        {user && <Link href="/#history">History</Link>}
      </nav>
      <div className="header-meta">
        <ThemeToggle />
        {user ? (
          <>
            <span className="account-chip" title={user.email}>{user.email}</span>
            <form action="/auth/signout" method="post">
              <button className="login-link" type="submit">Log out</button>
            </form>
          </>
        ) : (
          <Link className="login-link" href="/login">Log in</Link>
        )}
        <Link className="header-cta" href={user ? "/#analyze" : "/login"}>
          {user ? "Scan resume" : "Start free"}
        </Link>
      </div>
    </header>
  );
}
