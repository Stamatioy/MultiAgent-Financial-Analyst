import {
  BrainCircuit,
} from "lucide-react";


export default function Loading() {
  return (
    <div className="mx-auto flex min-h-[60vh] max-w-6xl items-center justify-center">
      <div className="text-center">
        <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-xl border border-emerald-400/20 bg-emerald-400/[0.05] text-emerald-400">
          <BrainCircuit className="h-5 w-5 animate-pulse" />
        </div>

        <div className="mt-4 text-sm font-medium text-white">
          Loading financial workspace
        </div>

        <div className="mt-2 text-xs text-[var(--muted)]">
          Preparing research data...
        </div>

        <div className="mx-auto mt-5 h-1 w-48 overflow-hidden rounded-full bg-white/[0.05]">
          <div className="loading-bar h-full w-1/3 rounded-full bg-emerald-400" />
        </div>
      </div>
    </div>
  );
}