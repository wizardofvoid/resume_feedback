import type { Metadata } from "next";
import { Space_Grotesk, Space_Mono } from "next/font/google";
import { APP_NAME, APP_TAGLINE } from "@/lib/brand";
import "./globals.css";

const spaceGrotesk = Space_Grotesk({
  subsets: ["latin"],
  variable: "--font-space-grotesk",
  display: "swap",
});

const spaceMono = Space_Mono({
  subsets: ["latin"],
  weight: ["400", "700"],
  variable: "--font-space-mono",
  display: "swap",
});

export const metadata: Metadata = {
  title: `${APP_NAME} — ${APP_TAGLINE}`,
  description:
    "See how your resume aligns with a role before a recruiter gives it a glance.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" className={`${spaceGrotesk.variable} ${spaceMono.variable}`} suppressHydrationWarning>
      <body>
        <script
          dangerouslySetInnerHTML={{
            __html: `(function(){try{var t=localStorage.getItem('glance-theme')||localStorage.getItem('resume-signal-theme')||'dark';document.documentElement.dataset.theme=t==='light'?'light':'dark';localStorage.setItem('glance-theme',t)}catch(e){document.documentElement.dataset.theme='dark'}})()`,
          }}
        />
        {children}
      </body>
    </html>
  );
}
