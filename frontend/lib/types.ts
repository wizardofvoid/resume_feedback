export type AnalysisResult = {
  ats_score: number;
  skill_match_score: number;
  format_score: number;
  found_skills: string[];
  missing_skills: string[];
  job_skill_weights: Record<string, number>;
  ai_feedback: string;
  contact_info?: {
    email?: string;
    phone?: string;
  };
  persistence_warning?: string;
  quality_analysis?: {
    recommendations?: string[];
    text_metrics?: Record<string, number>;
    section_completeness?: Record<string, boolean>;
  };
};

export type HistoryItem = {
  id: string;
  created_at: string;
  score: number;
  resume_name: string;
  email: string | null;
  phone: string | null;
};

export type HistoryResponse = {
  history: HistoryItem[];
};
