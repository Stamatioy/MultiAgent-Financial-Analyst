import {
  Check,
  Circle,
  LoaderCircle,
  X,
} from "lucide-react";

import {
  ResearchStep as ResearchStepType,
} from "@/lib/types";


export function ResearchStep({
  step,
}: {
  step: ResearchStepType;
}) {
  return (
    <div
      className={`
        flex
        items-center
        gap-4
        rounded-xl
        border
        px-4
        py-4
        transition-all
        ${
          step.status === "running"
            ? "border-emerald-400/30 bg-emerald-400/[0.04]"
            : step.status === "completed"
              ? "border-[var(--border)] bg-white/[0.015]"
              : step.status === "failed"
                ? "border-red-400/30 bg-red-400/[0.04]"
                : "border-[var(--border-soft)] bg-transparent"
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

        <div
          className="
            mt-1
            text-[11px]
            text-[var(--muted)]
          "
        >
          {statusLabel(
            step.status,
          )}
        </div>
      </div>
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
      <div
        className="
          flex
          h-8
          w-8
          items-center
          justify-center
          rounded-full
          bg-emerald-400/10
          text-emerald-400
        "
      >
        <Check className="h-4 w-4" />
      </div>
    );
  }

  if (
    status === "running"
  ) {
    return (
      <div
        className="
          flex
          h-8
          w-8
          items-center
          justify-center
          rounded-full
          bg-emerald-400/10
          text-emerald-400
        "
      >
        <LoaderCircle
          className="
            h-4
            w-4
            animate-spin
          "
        />
      </div>
    );
  }

  if (
    status === "failed"
  ) {
    return (
      <div
        className="
          flex
          h-8
          w-8
          items-center
          justify-center
          rounded-full
          bg-red-400/10
          text-red-400
        "
      >
        <X className="h-4 w-4" />
      </div>
    );
  }

  return (
    <div
      className="
        flex
        h-8
        w-8
        items-center
        justify-center
        rounded-full
        border
        border-[var(--border)]
        text-[var(--muted)]
      "
    >
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
      return "Complete";

    case "failed":
      return "Failed";

    default:
      return "Waiting";
  }
}