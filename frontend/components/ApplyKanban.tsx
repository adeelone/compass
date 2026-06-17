"use client";

import { useEffect, useMemo, useState } from "react";
import { listApplications } from "../lib/api";
import type { Application } from "../lib/types";

const columns = ["saved", "applied", "interviewing", "offer", "closed"] as const;

export function ApplyKanban() {
  const [applications, setApplications] = useState<Application[]>([]);

  useEffect(() => {
    listApplications().then(setApplications).catch(() => setApplications([]));
  }, []);

  const grouped = useMemo(() => {
    return applications.reduce<Record<string, Application[]>>((groups, application) => {
      groups[application.status] = [...(groups[application.status] ?? []), application];
      return groups;
    }, {});
  }, [applications]);

  return (
    <section>
      <h1 className="text-2xl font-semibold">Application pipeline</h1>
      <div className="mt-4 grid gap-4 lg:grid-cols-5">
        {columns.map((column) => (
          <div className="min-h-64 rounded-lg border border-slate-200 bg-white p-3 shadow-sm" key={column}>
            <h2 className="text-sm font-semibold uppercase tracking-wide text-slate-600">{column}</h2>
            {(grouped[column] ?? []).map((application) => (
              <div className="mt-3 rounded-md border border-slate-200 p-3 text-sm" key={application.job_id}>
                <div className="font-medium">{application.job_id}</div>
                {application.notes[0] && <div className="mt-1 text-slate-600">{application.notes[0]}</div>}
              </div>
            ))}
          </div>
        ))}
      </div>
    </section>
  );
}
