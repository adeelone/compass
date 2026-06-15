"use client";

import { useMemo, useState } from "react";
import { UploadCloud } from "lucide-react";
import { analyzeResume } from "../lib/api";
import type { ResumeAnalysis } from "../lib/types";

const sample = `Ada Example
ada@example.com
Skills
Python, FastAPI, React, PostgreSQL
- Built API used by 120 teams and reduced review time by 32%`;

export function ResumeAnalyzer({ compact = false }: { compact?: boolean }) {
  const [text, setText] = useState(sample);
  const [analysis, setAnalysis] = useState<ResumeAnalysis | null>(null);
  const [loading, setLoading] = useState(false);
  const rules = useMemo(() => analysis?.ats_rules ?? [], [analysis]);

  async function runAnalysis() {
    setLoading(true);
    setAnalysis(await analyzeResume(text));
    setLoading(false);
  }

  return (
    <section className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
      <div className="flex items-center justify-between gap-4">
        <div>
          <h2 className="text-lg font-semibold">Resume intelligence</h2>
          <p className="text-sm text-slate-600">ATS checks, content quality, and sourced fixes.</p>
        </div>
        <button className="inline-flex items-center gap-2 rounded-md bg-teal-700 px-3 py-2 text-sm font-medium text-white hover:bg-teal-800 focus:outline-none focus:ring-2 focus:ring-teal-700" onClick={runAnalysis} disabled={loading}>
          <UploadCloud className="h-4 w-4" />
          {loading ? "Analyzing" : "Analyze"}
        </button>
      </div>
      {!compact && (
        <textarea className="mt-4 h-48 w-full rounded-md border border-slate-300 p-3 text-sm focus:outline-none focus:ring-2 focus:ring-teal-700" value={text} onChange={(event) => setText(event.target.value)} aria-label="Resume text" />
      )}
      <div className="mt-4 grid gap-3 sm:grid-cols-2">
        <Score label="ATS" value={analysis?.ats_score ?? 0} />
        <Score label="Content" value={analysis?.content_score ?? 0} />
      </div>
      <div className="mt-4 space-y-2">
        {rules.slice(0, compact ? 3 : rules.length).map((rule) => (
          <div key={rule.id} className="flex items-start justify-between gap-3 rounded-md border border-slate-200 p-3 text-sm">
            <div>
              <div className="font-medium">{rule.label}</div>
              <div className="text-slate-600">{rule.fix}</div>
            </div>
            <span className={rule.passed ? "text-teal-700" : "text-rose-700"}>{rule.passed ? "Pass" : "Fix"}</span>
          </div>
        ))}
      </div>
    </section>
  );
}

function Score({ label, value }: { label: string; value: number }) {
  return (
    <div className="rounded-md bg-slate-100 p-3">
      <div className="text-sm text-slate-600">{label}</div>
      <div className="text-2xl font-semibold">{value}</div>
    </div>
  );
}

