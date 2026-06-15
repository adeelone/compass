import { ResumeAnalyzer } from "./ResumeAnalyzer";
import { JobFeed } from "./JobFeed";

export function Dashboard() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-semibold tracking-tight">Today</h1>
        <p className="mt-1 text-sm text-slate-600">3 strong matches, 2 resume fixes, and 1 follow-up due.</p>
      </div>
      <div className="grid gap-6 xl:grid-cols-[1fr_1.2fr]">
        <ResumeAnalyzer compact />
        <JobFeed compact />
      </div>
    </div>
  );
}

