import type { ScoredJob } from "../lib/types";

export function MatchPanel({ item }: { item: ScoredJob }) {
  return (
    <div className="mt-3 grid gap-3 text-sm md:grid-cols-2">
      <div>
        <div className="font-medium">Why this score</div>
        <ul className="mt-2 space-y-1 text-slate-700">
          {item.why.map((reason) => (
            <li key={reason.label}>{reason.label}: {reason.points} pts</li>
          ))}
        </ul>
      </div>
      <div>
        <div className="font-medium">Missing keywords</div>
        <div className="mt-2 flex flex-wrap gap-2">
          {item.missing_keywords.map((keyword) => (
            <span className="rounded-md bg-amber-50 px-2 py-1 text-amber-900" key={keyword}>{keyword}</span>
          ))}
        </div>
      </div>
    </div>
  );
}

