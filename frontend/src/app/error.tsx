"use client";

import {
  AlertTriangle,
  RotateCcw,
} from "lucide-react";


export default function ErrorPage({
  error,
  reset,
}: {
  error: Error & {
    digest?: string;
  };

  reset: () => void;
}) {
  return (
    <div className="mx-auto flex min-h-[60vh] max-w-4xl items-center justify-center">
      <div className="w-full rounded-2xl border border-red-400/20 bg-red-400/[0.035] p-8 text-center">
        <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-xl bg-red-400/10 text-red-400">
          <AlertTriangle className="h-5 w-5" />
        </div>

        <h1 className="mt-5 text-xl font-semibold text-white">
          Something went wrong
        </h1>

        <p className="mx-auto mt-3 max-w-xl text-sm leading-6 text-[var(--muted-light)]">
          The application encountered an unexpected error while loading this section.
        </p>

        {process.env.NODE_ENV === "development" && (
          <div className="mx-auto mt-5 max-w-2xl rounded-xl border border-red-400/10 bg-black/20 p-4 text-left">
            <div className="text-[10px] uppercase tracking-[0.12em] text-red-300">
              Development error
            </div>

            <div className="mt-2 break-words font-mono text-xs leading-5 text-red-200/70">
              {error.message}
            </div>
          </div>
        )}

        <button
          type="button"
          onClick={reset}
          className="mx-auto mt-6 flex items-center gap-2 rounded-lg border border-red-400/20 bg-red-400/[0.05] px-4 py-2 text-sm font-medium text-red-200 transition hover:bg-red-400/[0.1]"
        >
          <RotateCcw className="h-4 w-4" />

          Try Again
        </button>
      </div>
    </div>
  );
}