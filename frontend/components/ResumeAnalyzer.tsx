"use client";

import { useMemo, useState } from "react";
import { FileDown, UploadCloud } from "lucide-react";
import { analyzeResume, exportResume, uploadResume } from "../lib/api";
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
  const [exported, setExported] = useState("");
  const rules = useMemo(() => analysis?.ats_rules ?? [], [analysis]);

  async function runAnalysis() {
    setLoading(true);
    setAnalysis(await analyzeResume(text));
    setLoading(false);
  }

  async function runUpload(file: File | undefined) {
    if (!file) return;
    setLoading(true);
    const result = await uploadResume(file);
    if (result.resume_id) {
      window.localStorage.setItem("compass_resume_id", result.resume_id);
    }
    setAnalysis(result);
    setLoading(false);
  }

  async function exportActive() {
    if (!analysis?.resume_id) return;
    const result = await exportResume(analysis.resume_id);
    setExported(result.content);
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
        <div className="mt-4 space-y-3">
          <input className="block w-full text-sm" type="file" accept=".pdf,.docx,.txt,.md,.png,.jpg,.jpeg" onChange={(event) => runUpload(event.target.files?.[0])} aria-label="Upload resume" />
          <textarea className="h-48 w-full rounded-md border border-slate-300 p-3 text-sm focus:outline-none focus:ring-2 focus:ring-teal-700" value={text} onChange={(event) => setText(event.target.value)} aria-label="Resume text" />
        </div>
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
      {analysis?.resume_id && (
        <button className="mt-4 inline-flex items-center gap-2 rounded-md border border-slate-300 px-3 py-2 text-sm font-medium" onClick={exportActive}>
          <FileDown className="h-4 w-4" />
          Export Markdown
        </button>
      )}
      {exported && <pre className="mt-3 max-h-48 overflow-auto rounded-md bg-slate-950 p-3 text-xs text-white">{exported}</pre>}
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
