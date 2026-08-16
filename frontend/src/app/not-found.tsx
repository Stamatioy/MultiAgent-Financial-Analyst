import Link from "next/link";

import {
  SearchX,
} from "lucide-react";


export default function NotFound() {
  return (
    <div className="mx-auto flex min-h-[60vh] max-w-4xl items-center justify-center">
      <div className="text-center">
        <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-xl border border-[var(--border)] bg-white/[0.02] text-[var(--muted-light)]">
          <SearchX className="h-5 w-5" />
        </div>

        <div className="mt-5 text-xs uppercase tracking-[0.16em] text-emerald-400">
          404
        </div>

        <h1 className="mt-2 text-2xl font-semibold text-white">
          Page not found
        </h1>

        <p className="mt-3 text-sm text-[var(--muted)]">
          The page you requested does not exist.
        </p>

        <Link
          href="/"
          className="mt-6 inline-flex rounded-lg border border-emerald-400/20 bg-emerald-400/[0.04] px-4 py-2 text-sm font-medium text-emerald-300 transition hover:bg-emerald-400/[0.08]"
        >
          Return to Dashboard
        </Link>
      </div>
    </div>
  );
}