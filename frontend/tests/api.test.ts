import { afterEach, describe, expect, test, vi } from "vitest";
import {
  analyzeResume,
  draftCoverLetter,
  exportResume,
  getDigest,
  getProfileCompleteness,
  getPublicProfile,
  matchJobs,
  saveApplication,
} from "../lib/api";

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
      if (url.includes("/resume/res_1/export")) {
        return Response.json({ format: "markdown", content: "# Ada Example" });
      }
      if (url.endsWith("/cover-letter")) {
        return Response.json({ content: "Dear Example", source: "profile+job" });
      }
      if (url.endsWith("/applications")) {
        return Response.json({ job_id: "job_1", status: "applied", notes: [], contacts: [], updated_at: "2026-06-16T00:00:00Z" });
      }
      if (url.endsWith("/notifications/digest")) {
        return Response.json({ content: "# Compass Daily Digest", count: 1 });
      }
      if (url.endsWith("/profile/public")) {
        return Response.json({ name: "Ada Example" });
      }
      return Response.json({ score: 50, next_steps: ["Add at least five skills."] });
    });

    expect((await analyzeResume("Ada")).content_score).toBe(90);
    expect((await matchJobs())[0].job.title).toBe("Engineer");
    expect((await getProfileCompleteness()).score).toBe(50);
    expect((await exportResume("res_1")).content).toContain("Ada");
    expect((await draftCoverLetter("res_1", "job_1")).source).toBe("profile+job");
    expect((await saveApplication("job_1", "applied")).status).toBe("applied");
    expect((await getDigest()).count).toBe(1);
    expect((await getPublicProfile({ contact: { name: "Ada Example" } })).name).toBe("Ada Example");
    expect(fetchMock).toHaveBeenCalledTimes(8);
  });
});
