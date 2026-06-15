const columns = ["saved", "applied", "interviewing", "offer", "closed"];

export function ApplyKanban() {
  return (
    <section>
      <h1 className="text-2xl font-semibold">Application pipeline</h1>
      <div className="mt-4 grid gap-4 lg:grid-cols-5">
        {columns.map((column) => (
          <div className="min-h-64 rounded-lg border border-slate-200 bg-white p-3 shadow-sm" key={column}>
            <h2 className="text-sm font-semibold uppercase tracking-wide text-slate-600">{column}</h2>
            {column === "saved" && (
              <div className="mt-3 rounded-md border border-slate-200 p-3 text-sm">Backend Engineer · Example Systems</div>
            )}
          </div>
        ))}
      </div>
    </section>
  );
}

