"use client";

import {
  ReactNode,
  useState,
} from "react";

import {
  Check,
  ChevronDown,
  ChevronUp,
  Circle,
  LoaderCircle,
  X,
} from "lucide-react";

import {
  ResearchStep as ResearchStepType,
} from "@/lib/types";


export function ResearchStep({
  step,
  children,
}: {
  step: ResearchStepType;
  children?: ReactNode;
}) {
  const [
    expanded,
    setExpanded,
  ] = useState(false);

  const canExpand =
    step.status === "completed"
    && children !== undefined;


  function toggle() {
    if (!canExpand) {
      return;
    }

    setExpanded(
      (current) => !current
    );
  }


  return (
    <div
      className={`
        overflow-hidden
        rounded-xl
        border
        transition-all
        ${
          step.status === "running"
            ? "animate-subtle-glow border-emerald-400/30 bg-emerald-400/[0.04]"
            : step.status === "completed"
              ? "border-[var(--border)] bg-white/[0.015]"
              : step.status === "failed"
                ? "border-red-400/30 bg-red-400/[0.04]"
                : "border-[var(--border-soft)] bg-transparent"
        }
      `}
    >
      <button
        type="button"
        disabled={!canExpand}
        onClick={toggle}
        className={`
          flex
          w-full
          items-center
          gap-4
          px-4
          py-4
          text-left
          transition
          ${
            canExpand
              ? "cursor-pointer hover:bg-white/[0.03]"
              : "cursor-default"
          }
        `}
      >
        <StepIcon
          status={
            step.status
          }
        />

        <div className="flex-1">
          <div
            className={`
              text-sm
              font-medium
              ${
                step.status
                === "waiting"
                  ? "text-[var(--muted)]"
                  : "text-white"
              }
            `}
          >
            {step.label}
          </div>

          <div className="mt-1 text-[11px] text-[var(--muted)]">
            {statusLabel(
              step.status
            )}
          </div>
        </div>

        {canExpand && (
          <div className="text-[var(--muted)]">
            {expanded ? (
              <ChevronUp className="h-4 w-4" />
            ) : (
              <ChevronDown className="h-4 w-4" />
            )}
          </div>
        )}
      </button>

      {canExpand && expanded && (
        <div className="animate-fade-in-up border-t border-[var(--border-soft)] bg-black/10 px-5 py-5 lg:px-6 lg:py-6">
          {children}
        </div>
      )}
    </div>
  );
}


function StepIcon({
  status,
}: {
  status:
    ResearchStepType["status"];
}) {
  if (
    status === "completed"
  ) {
    return (
      <div className="flex h-8 w-8 items-center justify-center rounded-full bg-emerald-400/10 text-emerald-400">
        <Check className="h-4 w-4" />
      </div>
    );
  }

  if (
    status === "running"
  ) {
    return (
      <div className="flex h-8 w-8 items-center justify-center rounded-full bg-emerald-400/10 text-emerald-400">
        <LoaderCircle className="h-4 w-4 animate-spin" />
      </div>
    );
  }

  if (
    status === "failed"
  ) {
    return (
      <div className="flex h-8 w-8 items-center justify-center rounded-full bg-red-400/10 text-red-400">
        <X className="h-4 w-4" />
      </div>
    );
  }

  return (
    <div className="flex h-8 w-8 items-center justify-center rounded-full border border-[var(--border)] text-[var(--muted)]">
      <Circle className="h-3 w-3" />
    </div>
  );
}


function statusLabel(
  status:
    ResearchStepType["status"],
) {
  switch (status) {
    case "running":
      return "Analyzing...";

    case "completed":
      return "Complete — click to view";

    case "failed":
      return "Failed";

    default:
      return "Waiting";
  }
}