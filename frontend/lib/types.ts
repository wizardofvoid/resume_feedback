export type AnalysisResult = {
  ats_score: number;
  skill_match_score: number;
  format_score: number;
  found_skills: string[];
  missing_skills: string[];
  job_skill_weights: Record<string, number>;
  ai_feedback: string;
  quality_analysis?: {
    recommendations?: string[];
    text_metrics?: Record<string, number>;
    section_completeness?: Record<string, boolean>;
  };
};

export type HistoryItem = {
  id: number;
  created_at: string;
  score: number;
  resume_id: number;
  email: string | null;
  phone: string | null;
  jd_id: number;
};

export type HistoryResponse = {
  history: HistoryItem[];
};
