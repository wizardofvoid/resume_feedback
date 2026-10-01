"use client";

import { ChangeEvent, DragEvent, FormEvent, useCallback, useEffect, useRef, useState } from "react";
import { formatSkill } from "@/lib/format";
import type { AnalysisResult, HistoryItem, HistoryResponse } from "@/lib/types";
import { ArrowIcon, CheckIcon, CloseIcon, EyeIcon, FileIcon, ShieldIcon, UploadIcon } from "./icons";
import { ScoreRing } from "./score-ring";
import { HistoryPanel } from "./history-panel";

const MAX_FILE_SIZE = 10 * 1024 * 1024;
const ACCEPTED_EXTENSIONS = ["pdf", "docx"];

function getErrorMessage(payload: unknown, fallback: string) {
  if (payload && typeof payload === "object" && "detail" in payload && typeof payload.detail === "string") {
    return payload.detail;
  }
  return fallback;
}

export function Analyzer() {
  const inputRef = useRef<HTMLInputElement>(null);
  const resultsRef = useRef<HTMLElement>(null);
  const [file, setFile] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState("");
  const [dragging, setDragging] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState("");
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [historyLoading, setHistoryLoading] = useState(true);
  const [clearing, setClearing] = useState(false);
  const [consent, setConsent] = useState(false);

  const loadHistory = useCallback(async () => {
    try {
      const response = await fetch("/api/history", { cache: "no-store" });
      if (!response.ok) throw new Error("History unavailable");
      const data = (await response.json()) as HistoryResponse;
      setHistory(data.history ?? []);
    } catch {
      setHistory([]);
    } finally {
      setHistoryLoading(false);
    }
  }, []);

  useEffect(() => {
    const timer = window.setTimeout(() => {
      void loadHistory();
      setConsent(Boolean(window.localStorage.getItem("glance-external-ai-consent-at")));
      const saved =
        window.sessionStorage.getItem("glance-result") ??
        window.sessionStorage.getItem("resume-signal-result");
      if (saved) {
        try {
          const parsed = JSON.parse(saved) as AnalysisResult;
          setResult(parsed);
          window.sessionStorage.setItem("glance-result", saved);
          window.sessionStorage.removeItem("resume-signal-result");
        } catch {
          window.sessionStorage.removeItem("glance-result");
          window.sessionStorage.removeItem("resume-signal-result");
        }
      }
    }, 0);
    return () => window.clearTimeout(timer);
  }, [loadHistory]);

  function validateFile(candidate: File) {
    const extension = candidate.name.split(".").pop()?.toLowerCase() ?? "";
    if (!ACCEPTED_EXTENSIONS.includes(extension)) {
      setError("Use a PDF or DOCX file.");
      return false;
    }
    if (candidate.size > MAX_FILE_SIZE) {
      setError("Resume files must be 10 MB or smaller.");
      return false;
    }
    setError("");
    return true;
  }

  function chooseFile(candidate?: File) {
    if (candidate && validateFile(candidate)) setFile(candidate);
  }

  function onFileChange(event: ChangeEvent<HTMLInputElement>) {
    chooseFile(event.target.files?.[0]);
  }

  function onDrop(event: DragEvent<HTMLElement>) {
    event.preventDefault();
    setDragging(false);
    chooseFile(event.dataTransfer.files?.[0]);
  }

  async function analyze(event: FormEvent) {
    event.preventDefault();
    if (!file) {
      setError("Add your resume before starting the analysis.");
      return;
    }
    if (!consent) {
      setError("Confirm the processing note before starting the analysis.");
      return;
    }

    setAnalyzing(true);
    setError("");
    window.localStorage.setItem("glance-external-ai-consent-at", new Date().toISOString());

    const data = new FormData();
    data.append("file", file);
    data.append("job_description", jobDescription.trim());

    try {
      const response = await fetch("/api/analyze", { method: "POST", body: data });
      const payload = (await response.json().catch(() => null)) as AnalysisResult | { detail?: string } | null;
      if (!response.ok) throw new Error(getErrorMessage(payload, "Analysis failed. Please try again."));

      const analysis = payload as AnalysisResult;
      setResult(analysis);
      window.sessionStorage.setItem("glance-result", JSON.stringify(analysis));
      await loadHistory();
      window.setTimeout(() => resultsRef.current?.scrollIntoView({ behavior: "smooth", block: "start" }), 80);
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Analysis failed. Please try again.");
    } finally {
      setAnalyzing(false);
    }
  }

  async function clearHistory() {
    if (!window.confirm("Clear every saved analysis from this local backend? This cannot be undone.")) return;
    setClearing(true);
    try {
      const response = await fetch("/api/history", { method: "DELETE" });
      if (!response.ok) throw new Error();
      setHistory([]);
    } catch {
      setError("History could not be cleared. Please try again.");
    } finally {
      setClearing(false);
    }
  }

  const found = result?.found_skills ?? [];
  const missing = result?.missing_skills ?? [];

  return (
    <>
      <section className="workspace shell" id="analyze" aria-labelledby="workspace-title">
        <div className="section-heading workspace-heading">
          <div>
            <p className="eyebrow"><span /> Your turn</p>
            <h2 id="workspace-title">See what gets noticed</h2>
          </div>
          <p>PDF or DOCX · 10 MB maximum</p>
        </div>

        <form className="analysis-form" onSubmit={analyze}>
          <div className="field-panel upload-panel">
            <label className="field-label" htmlFor="resume-file">
              <span>01</span> resume file
            </label>
            <input
              ref={inputRef}
              id="resume-file"
              className="sr-only"
              type="file"
              accept=".pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
              onChange={onFileChange}
            />
            {file ? (
              <div className="selected-file">
                <FileIcon />
                <div>
                  <strong>{file.name}</strong>
                  <span>{(file.size / 1024 / 1024).toFixed(2)} MB · file added</span>
                </div>
                <button
                  type="button"
                  className="remove-file"
                  onClick={() => {
                    setFile(null);
                    if (inputRef.current) inputRef.current.value = "";
                  }}
                  aria-label="Remove selected resume"
                >
                  <CloseIcon />
                </button>
              </div>
            ) : (
              <label
                className={`drop-zone${dragging ? " is-dragging" : ""}`}
                htmlFor="resume-file"
                tabIndex={0}
                onKeyDown={(event) => {
                  if (event.key === "Enter" || event.key === " ") {
                    event.preventDefault();
                    inputRef.current?.click();
                  }
                }}
                onDragEnter={(event) => { event.preventDefault(); setDragging(true); }}
                onDragOver={(event) => event.preventDefault()}
                onDragLeave={() => setDragging(false)}
                onDrop={onDrop}
              >
                <UploadIcon />
                <strong>Drop your resume here</strong>
                <span>or pick a file · PDF or DOCX</span>
                <span className="secondary-button" aria-hidden="true">Choose file</span>
              </label>
            )}
          </div>

          <div className="field-panel brief-panel">
            <label className="field-label" htmlFor="job-description">
              <span>02</span> role brief <em>optional</em>
            </label>
            <textarea
              id="job-description"
              value={jobDescription}
              onChange={(event) => setJobDescription(event.target.value)}
              placeholder="Paste the complete job description here. Requirements, responsibilities, and preferred skills all improve the comparison."
            />
            <div className="brief-meta">
              <span>{jobDescription.trim() ? `${jobDescription.trim().split(/\s+/).length} words` : "Optional, but recommended"}</span>
              {jobDescription && <button type="button" className="text-button" onClick={() => setJobDescription("")}>Clear</button>}
            </div>
          </div>

          <div className="consent-row">
            <label className="consent-check">
              <input type="checkbox" checked={consent} onChange={(event) => setConsent(event.target.checked)} />
              <span className="check-box"><CheckIcon /></span>
              <span>
                <strong>I’m okay with external AI processing</strong>
                <small>Your resume and role brief are sent through the configured AI service to write feedback. Completed results are kept in this backend’s local history.</small>
              </span>
            </label>
          </div>

          <div className="submit-row">
            <div className="privacy-note">
              <ShieldIcon />
              <p>Clear the local history whenever you want.</p>
            </div>
            <button className="primary-button" type="submit" disabled={analyzing}>
              <span>{analyzing ? "Reading your resume…" : "Scan resume"}</span>
              {analyzing ? <i className="spinner" /> : <ArrowIcon />}
            </button>
          </div>

          {error && <div className="error-banner" role="alert"><strong>Couldn’t complete that.</strong><span>{error}</span></div>}
        </form>

        <div className="trust-strip" aria-label="How to read your result">
          <div><EyeIcon /><span><strong>Specific</strong> See the evidence behind the score.</span></div>
          <div><CheckIcon /><span><strong>Actionable</strong> Fix the biggest gaps first.</span></div>
          <div><ShieldIcon /><span><strong>In your control</strong> Delete local history any time.</span></div>
        </div>
      </section>

      {result && (
        <section className="results shell" ref={resultsRef} aria-labelledby="results-title">
          <div className="section-heading results-heading">
            <div>
              <p className="eyebrow"><span /> Analysis complete</p>
              <h2 id="results-title">The recruiter’s glance</h2>
            </div>
            <button className="text-button" type="button" onClick={() => {
              setResult(null);
              window.sessionStorage.removeItem("glance-result");
              window.sessionStorage.removeItem("resume-signal-result");
              document.getElementById("analyze")?.scrollIntoView({ behavior: "smooth" });
            }}>Start another</button>
          </div>

          <div className="score-board">
            <ScoreRing score={result.ats_score} />
            <div className="score-breakdown">
              <div className="metric">
                <span>Skill alignment</span>
                <strong>{result.skill_match_score.toFixed(0)}<small>%</small></strong>
                <div className="metric-bar"><i style={{ width: `${Math.max(0, Math.min(100, result.skill_match_score))}%` }} /></div>
              </div>
              <div className="metric">
                <span>Resume structure</span>
                <strong>{result.format_score.toFixed(0)}<small>%</small></strong>
                <div className="metric-bar"><i style={{ width: `${Math.max(0, Math.min(100, result.format_score))}%` }} /></div>
              </div>
              <p className="score-explainer">Compatibility combines role-specific skill coverage with the resume’s parseable structure.</p>
            </div>
          </div>

          {(found.length > 0 || missing.length > 0) && (
            <div className="skill-analysis">
              <div className="skill-column found-column">
                <div className="skill-heading"><span>Found</span><strong>{found.length.toString().padStart(2, "0")}</strong></div>
                <div className="skill-list">
                  {found.length ? found.map((skill) => (
                    <span className="skill-chip" key={skill}>
                      <i />{formatSkill(skill)}
                      {result.job_skill_weights[skill] === 2 && <em>Required</em>}
                    </span>
                  )) : <p className="empty-skills">No matching role skills were detected.</p>}
                </div>
              </div>
              <div className="skill-column missing-column">
                <div className="skill-heading"><span>Missing</span><strong>{missing.length.toString().padStart(2, "0")}</strong></div>
                <div className="skill-list">
                  {missing.length ? missing.map((skill) => (
                    <span className="skill-chip" key={skill}>
                      <i />{formatSkill(skill)}
                      {result.job_skill_weights[skill] === 2 && <em>Required</em>}
                    </span>
                  )) : <p className="empty-skills">No missing role skills were detected.</p>}
                </div>
              </div>
            </div>
          )}

          {result.ai_feedback && (
            <article className="feedback-panel">
              <div className="feedback-label"><span>Recruiter’s note</span><i /></div>
              <div className="feedback-copy">
                {result.ai_feedback.split(/\n+/).filter(Boolean).map((paragraph, index) => <p key={index}>{paragraph}</p>)}
              </div>
            </article>
          )}
        </section>
      )}

      <HistoryPanel items={history} loading={historyLoading} onClear={clearHistory} clearing={clearing} />
    </>
  );
}
