import Link from "next/link";
import { BriefcaseBusiness, FileText, LayoutDashboard, UserRound, Columns3 } from "lucide-react";

const nav = [
  { href: "/", label: "Dashboard", icon: LayoutDashboard },
  { href: "/resume", label: "Resume", icon: FileText },
  { href: "/jobs", label: "Jobs", icon: BriefcaseBusiness },
  { href: "/profile", label: "Profile", icon: UserRound },
  { href: "/applications", label: "Applications", icon: Columns3 },
];

export function AppShell({ children }: { children: React.ReactNode }) {
  return (
    <main className="min-h-screen bg-slate-50 text-slate-950">
      <aside className="fixed inset-y-0 left-0 hidden w-64 border-r border-slate-200 bg-white px-4 py-5 md:block">
        <div className="mb-8 text-xl font-semibold tracking-tight">Compass</div>
        <nav className="space-y-1">
          {nav.map((item) => (
            <Link className="flex items-center gap-3 rounded-md px-3 py-2 text-sm hover:bg-slate-100 focus:outline-none focus:ring-2 focus:ring-teal-600" href={item.href} key={item.href}>
              <item.icon aria-hidden className="h-4 w-4" />
              {item.label}
            </Link>
          ))}
        </nav>
      </aside>
      <div className="md:pl-64">
        <header className="sticky top-0 z-10 border-b border-slate-200 bg-white/90 px-4 py-3 backdrop-blur md:hidden">
          <div className="font-semibold">Compass</div>
        </header>
        <section className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">{children}</section>
      </div>
    </main>
  );
}

