export function formatSkill(skill: string) {
  const acronyms = new Set([
    "aws", "gcp", "sql", "html", "css", "php", "ai", "ml", "nlp",
    "cv", "bi", "api", "ui", "ux", "ci/cd", "sre", "dl", "ide",
  ]);
  const clean = skill.trim();
  if (acronyms.has(clean.toLowerCase())) return clean.toUpperCase();
  if (/[.+#/]/.test(clean)) return clean;
  return clean.replace(/\b\w/g, (letter) => letter.toUpperCase());
}

export function formatDate(value: string) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "Unknown date";
  return new Intl.DateTimeFormat("en", {
    day: "2-digit",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(date);
}

export function scoreBand(score: number) {
  if (score >= 75) return { label: "Looking good", tone: "good" } as const;
  if (score >= 50) return { label: "Almost there", tone: "warn" } as const;
  return { label: "Needs work", tone: "poor" } as const;
}
