import type { ResumeAnalysis, ScoredJob } from "./types";

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

export async function matchJobs(): Promise<ScoredJob[]> {
  if (process.env.NEXT_PUBLIC_USE_MOCK_API === "true") {
    return [{
      job: { id: "mock-1", title: "Backend Engineer", company: "Example Systems", locations: ["Remote"], apply_url: "https://example.com/jobs/mock-1" },
      score: 87,
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

