"use client";

import { useEffect, useState } from "react";
import { scoreBand } from "@/lib/format";

export function ScoreRing({ score }: { score: number }) {
  const normalized = Math.max(0, Math.min(100, score));
  const band = scoreBand(normalized);
  const [displayScore, setDisplayScore] = useState(0);

  useEffect(() => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      const frame = window.requestAnimationFrame(() => setDisplayScore(Math.round(normalized)));
      return () => window.cancelAnimationFrame(frame);
    }

    const startedAt = performance.now();
    let frame = 0;
    const tick = (now: number) => {
      const progress = Math.min(1, (now - startedAt) / 700);
      const eased = 1 - Math.pow(1 - progress, 3);
      setDisplayScore(Math.round(normalized * eased));
      if (progress < 1) frame = window.requestAnimationFrame(tick);
    };
    frame = window.requestAnimationFrame(tick);
    return () => window.cancelAnimationFrame(frame);
  }, [normalized]);

  return (
    <div
      className={`score-ring score-ring-${band.tone}`}
      role="img"
      aria-label={`Compatibility score ${Math.round(normalized)} out of 100, ${band.label}`}
    >
      <span className="score-kicker">overall match</span>
      <div className="score-highlight" aria-hidden="true">
        <mark>{displayScore}</mark>
        <span>out of 100</span>
      </div>
      <p><span />{band.label}</p>
      <small>This is a compatibility estimate, not a hiring decision.</small>
    </div>
  );
}
