"use client";

import { useState } from "react";
import { getProfileCompleteness } from "../lib/api";

export function ProfileEditor() {
  const [score, setScore] = useState<number | null>(null);
  const [steps, setSteps] = useState<string[]>([]);

  async function check() {
    const result = await getProfileCompleteness();
    setScore(result.score);
    setSteps(result.next_steps);
  }

  return (
    <section className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
      <h1 className="text-2xl font-semibold">Career profile</h1>
      <p className="mt-1 text-sm text-slate-600">The canonical source for matching, tailoring, and exports.</p>
      <button className="mt-4 rounded-md bg-teal-700 px-3 py-2 text-sm font-medium text-white" onClick={check}>Check completeness</button>
      {score !== null && (
        <div className="mt-4">
          <div className="text-3xl font-semibold">{score}%</div>
          <ul className="mt-2 list-disc pl-5 text-sm text-slate-700">
            {steps.map((step) => <li key={step}>{step}</li>)}
          </ul>
        </div>
      )}
    </section>
  );
}

