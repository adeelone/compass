"use client";

import { useEffect, useState } from "react";
import { draftCoverLetter, getJobs, saveApplication } from "../lib/api";
import type { ScoredJob } from "../lib/types";
import { MatchPanel } from "./MatchPanel";

export function JobFeed({ compact = false }: { compact?: boolean }) {
  const [jobs, setJobs] = useState<ScoredJob[]>([]);
  const [query, setQuery] = useState("python intern");
  const [saved, setSaved] = useState<string | null>(null);
  const [letter, setLetter] = useState("");

  useEffect(() => {
    getJobs("python intern").then(setJobs);
  }, []);

  async function runSearch() {
    setJobs(await getJobs(query));
  }

  async function saveJob(jobId: string) {
    await saveApplication(jobId, "saved", "Saved from job feed.");
    setSaved(jobId);
  }

  async function writeLetter(jobId: string) {
    const resumeId = window.localStorage.getItem("compass_resume_id");
    if (!resumeId) {
      setLetter("Upload a resume first.");
      return;
    }
    const result = await draftCoverLetter(resumeId, jobId);
    setLetter(result.content);
  }

  return (
    <section className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
      <div>
        <h2 className="text-lg font-semibold">Unified job feed</h2>
        <p className="text-sm text-slate-600">Sorted by relevance with transparent match reasons.</p>
      </div>
      <div className="mt-4 flex gap-2">
        <input className="min-w-0 flex-1 rounded-md border border-slate-300 px-3 py-2 text-sm" value={query} onChange={(event) => setQuery(event.target.value)} aria-label="Job search query" />
        <button className="rounded-md bg-teal-700 px-3 py-2 text-sm font-medium text-white" onClick={runSearch}>Search</button>
      </div>
      <div className="mt-4 space-y-3">
        {jobs.slice(0, compact ? 3 : jobs.length).map((item) => (
          <article key={item.job.id} className="rounded-md border border-slate-200 p-4">
            <div className="flex flex-wrap items-start justify-between gap-3">
              <div>
                <h3 className="font-semibold">{item.job.title}</h3>
                <p className="text-sm text-slate-600">{item.job.company} · {item.job.locations.join(", ")}</p>
              </div>
              <div className="rounded-md bg-teal-50 px-3 py-1 text-sm font-semibold text-teal-800">{item.score}</div>
            </div>
            <MatchPanel item={item} />
            <div className="mt-3 flex flex-wrap gap-2">
              <button className="rounded-md border border-slate-300 px-3 py-1.5 text-sm" onClick={() => saveJob(item.job.id)}>
                {saved === item.job.id ? "Saved" : "Save"}
              </button>
              <button className="rounded-md border border-slate-300 px-3 py-1.5 text-sm" onClick={() => writeLetter(item.job.id)}>
                Cover letter
              </button>
              {item.source_attribution && <span className="px-2 py-1.5 text-xs text-slate-500">{item.source_attribution}</span>}
            </div>
          </article>
        ))}
      </div>
      {letter && <pre className="mt-4 whitespace-pre-wrap rounded-md bg-slate-950 p-3 text-xs text-white">{letter}</pre>}
    </section>
  );
}
