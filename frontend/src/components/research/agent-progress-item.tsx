"use client";

import { ReactNode, useState } from "react";
import {
  Check,
  ChevronDown,
  ChevronUp,
  Circle,
  LoaderCircle,
  TriangleAlert,
} from "lucide-react";


export type AgentStatus =
  | "waiting"
  | "running"
  | "complete"
  | "error";


type AgentProgressItemProps = {
  name: string;
  status: AgentStatus;
  children?: ReactNode;
};


export function AgentProgressItem({
  name,
  status,
  children,
}: AgentProgressItemProps) {
  const [expanded, setExpanded] = useState(false);

  const canExpand =
    status === "complete" &&
    children !== undefined;

  function toggleExpanded() {
    if (!canExpand) {
      return;
    }

    setExpanded((current) => !current);
  }

  return (
    <div className="overflow-hidden border-b border-[var(--border-soft)] last:border-b-0">
      <button
        type="button"
        onClick={toggleExpanded}
        disabled={!canExpand}
        className={`flex w-full items-center justify-between px-4 py-4 text-left transition ${
          canExpand
            ? "cursor-pointer hover:bg-white/[0.03]"
            : "cursor-default"
        }`}
      >
        <div className="flex items-center gap-3">
          <StatusIcon status={status} />

          <div>
            <div className="text-sm font-medium text-white">
              {name}
            </div>

            <div className="mt-0.5 text-xs text-[var(--muted)]">
              {getStatusLabel(status)}
            </div>
          </div>
        </div>

        {canExpand && (
          <div className="text-[var(--muted-light)]">
            {expanded ? (
              <ChevronUp className="h-4 w-4" />
            ) : (
              <ChevronDown className="h-4 w-4" />
            )}
          </div>
        )}
      </button>

      {expanded && canExpand && (
        <div className="border-t border-[var(--border-soft)] bg-white/[0.015] px-4 py-4">
          {children}
        </div>
      )}
    </div>
  );
}


function StatusIcon({
  status,
}: {
  status: AgentStatus;
}) {
  if (status === "complete") {
    return (
      <div className="flex h-7 w-7 items-center justify-center rounded-full bg-emerald-400/10 text-emerald-400">
        <Check className="h-4 w-4" />
      </div>
    );
  }

  if (status === "running") {
    return (
      <div className="flex h-7 w-7 items-center justify-center rounded-full bg-amber-400/10 text-amber-400">
        <LoaderCircle className="h-4 w-4 animate-spin" />
      </div>
    );
  }

  if (status === "error") {
    return (
      <div className="flex h-7 w-7 items-center justify-center rounded-full bg-red-400/10 text-red-400">
        <TriangleAlert className="h-4 w-4" />
      </div>
    );
  }

  return (
    <div className="flex h-7 w-7 items-center justify-center text-[var(--muted)]">
      <Circle className="h-3 w-3" />
    </div>
  );
}


function getStatusLabel(
  status: AgentStatus,
): string {
  switch (status) {
    case "waiting":
      return "Waiting";

    case "running":
      return "Analyzing...";

    case "complete":
      return "Complete";

    case "error":
      return "Failed";
  }
}