import type { Application, ApplicationStatus, ResumeAnalysis, ScoredJob } from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api";

export async function analyzeResume(text: string): Promise<ResumeAnalysis> {
  if (process.env.NEXT_PUBLIC_USE_MOCK_API === "true") {
    return {
      ats_score: 100,
      content_score: 100,
      best_points: ["Built API used by 120 teams and reduced review time by 32%"],
      ats_rules: [
        { id: "contact-email", label: "Contact email parses cleanly", passed: true, severity: "high", fix: "No fix needed.", source: "mock" },
      ],
    };
  }
  const response = await fetch(`${API_BASE}/resume/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });
  return response.json();
}

export async function uploadResume(file: File): Promise<ResumeAnalysis> {
  const form = new FormData();
  form.append("file", file);
  const response = await fetch(`${API_BASE}/resume/upload`, {
    method: "POST",
    body: form,
  });
  return response.json();
}

export async function getJobs(query = "python intern"): Promise<ScoredJob[]> {
  if (process.env.NEXT_PUBLIC_USE_MOCK_API === "true") {
    return matchJobs();
  }
  const params = new URLSearchParams({ query });
  const response = await fetch(`${API_BASE}/jobs?${params.toString()}`);
  const data = await response.json();
  return data.results;
}

export async function matchJobs(): Promise<ScoredJob[]> {
  if (process.env.NEXT_PUBLIC_USE_MOCK_API === "true") {
    return [{
      job: { id: "mock-1", title: "Backend Engineer", company: "Example Systems", locations: ["Remote"], apply_url: "https://example.com/jobs/mock-1" },
      score: 87,
      matched_keywords: ["python", "fastapi"],
      why: [{ label: "Skill overlap", points: 55, evidence: "Python and FastAPI", source: "mock" }],
      missing_keywords: ["react", "postgres"],
      gap_closers: { react: ["https://react.dev/learn"], postgres: ["https://www.postgresql.org/docs/current/tutorial.html"] },
    }];
  }
  const response = await fetch(`${API_BASE}/jobs/match`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      query: "backend",
      profile: {
        contact: { name: "Ada Example", email: "ada@example.com" },
        headline: "Backend engineer",
        skills: [{ name: "Python" }, { name: "FastAPI" }],
        preferences: { remote: true, level: "mid" },
      },
    }),
  });
  const data = await response.json();
  return data.results;
}

export async function getProfileCompleteness(): Promise<{ score: number; next_steps: string[] }> {
  const response = await fetch(`${API_BASE}/profile/completeness`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      contact: { name: "Ada Example", email: "ada@example.com" },
      headline: "Backend engineer",
      skills: [{ name: "Python" }, { name: "FastAPI" }],
      preferences: { remote: true },
    }),
  });
  return response.json();
}

export async function exportResume(resumeId: string, jobId?: string): Promise<{ format: string; content: string }> {
  const params = new URLSearchParams({ format: "markdown" });
  if (jobId) params.set("job_id", jobId);
  const response = await fetch(`${API_BASE}/resume/${resumeId}/export?${params.toString()}`);
  return response.json();
}

export async function draftCoverLetter(resumeId: string, jobId: string): Promise<{ content: string; source: string }> {
  const response = await fetch(`${API_BASE}/cover-letter`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ resume_id: resumeId, job_id: jobId }),
  });
  return response.json();
}

export async function saveApplication(jobId: string, status: ApplicationStatus, note?: string): Promise<Application> {
  const response = await fetch(`${API_BASE}/applications`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ job_id: jobId, status, note }),
  });
  return response.json();
}

export async function listApplications(): Promise<Application[]> {
  const response = await fetch(`${API_BASE}/applications`);
  const data = await response.json();
  return data.results;
}

export async function getDigest(): Promise<{ content: string; count: number }> {
  const response = await fetch(`${API_BASE}/notifications/digest`);
  return response.json();
}

export async function getPublicProfile(profile: object): Promise<Record<string, unknown>> {
  const response = await fetch(`${API_BASE}/profile/public`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(profile),
  });
  return response.json();
}
