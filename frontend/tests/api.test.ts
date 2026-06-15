import { afterEach, describe, expect, test, vi } from "vitest";
import { analyzeResume, getProfileCompleteness, matchJobs } from "../lib/api";

describe("api client", () => {
  afterEach(() => {
    vi.restoreAllMocks();
    delete process.env.NEXT_PUBLIC_USE_MOCK_API;
  });

  test("uses mock responses when enabled", async () => {
    process.env.NEXT_PUBLIC_USE_MOCK_API = "true";
    expect((await analyzeResume("Ada")).ats_score).toBe(100);
    expect((await matchJobs())[0].score).toBe(87);
  });

  test("calls backend endpoints", async () => {
    const fetchMock = vi.spyOn(global, "fetch").mockImplementation(async (input) => {
      const url = String(input);
      if (url.endsWith("/resume/analyze")) {
        return Response.json({ ats_score: 80, content_score: 90, ats_rules: [], best_points: [] });
      }
      if (url.endsWith("/jobs/match")) {
        return Response.json({ results: [{ job: { id: "1", title: "Engineer", company: "Example", locations: [], apply_url: "https://example.com" }, score: 75, why: [], missing_keywords: [], gap_closers: {} }] });
      }
      return Response.json({ score: 50, next_steps: ["Add at least five skills."] });
    });

    expect((await analyzeResume("Ada")).content_score).toBe(90);
    expect((await matchJobs())[0].job.title).toBe("Engineer");
    expect((await getProfileCompleteness()).score).toBe(50);
    expect(fetchMock).toHaveBeenCalledTimes(3);
  });
});
