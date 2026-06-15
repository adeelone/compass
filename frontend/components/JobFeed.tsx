"use client";

import { useEffect, useState } from "react";
import { matchJobs } from "../lib/api";
import type { ScoredJob } from "../lib/types";
import { MatchPanel } from "./MatchPanel";

export function JobFeed({ compact = false }: { compact?: boolean }) {
  const [jobs, setJobs] = useState<ScoredJob[]>([]);

  useEffect(() => {
    matchJobs().then(setJobs);
  }, []);

  return (
    <section className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
      <div>
        <h2 className="text-lg font-semibold">Unified job feed</h2>
        <p className="text-sm text-slate-600">Sorted by relevance with transparent match reasons.</p>
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
          </article>
        ))}
      </div>
    </section>
  );
}

