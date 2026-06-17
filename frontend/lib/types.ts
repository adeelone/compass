export type AtsRule = {
  id: string;
  label: string;
  passed: boolean;
  severity: string;
  fix: string;
  source: string;
};

export type ResumeAnalysis = {
  resume_id?: string;
  ats_score: number;
  content_score: number;
  ats_rules: AtsRule[];
  best_points: string[];
  parsed_sections?: {
    work: unknown[];
    education: unknown[];
    skills: unknown[];
  };
};

export type ScoredJob = {
  job: {
    id: string;
    title: string;
    company: string;
    locations: string[];
    apply_url: string;
  };
  score: number;
  matched_keywords: string[];
  why: { label: string; points: number; evidence: string; source: string }[];
  missing_keywords: string[];
  gap_closers: Record<string, string[]>;
  source_attribution?: string;
};

export type ApplicationStatus = "saved" | "applied" | "interviewing" | "offer" | "closed";

export type Application = {
  job_id: string;
  status: ApplicationStatus;
  notes: string[];
  contacts: string[];
  updated_at: string;
};
