"use client";

import {
  useEffect,
  useState,
} from "react";

import {
  AlertCircle,
  BrainCircuit,
} from "lucide-react";

import {
  getResearchJobResult,
  getResearchJobStatus,
} from "@/lib/api";

import {
  CompanyInvestmentReport,
  ResearchJobStatusResponse,
} from "@/lib/types";

import {
  ResearchResultPreview,
} from "./research-result-preview";

import {
  ResearchStep,
} from "./research-step";

import {
  AgentResult,
} from "./agent-result";

import {
  addToWatchlist,
} from "@/lib/api";

import Link from "next/link";

const POLL_INTERVAL_MS =
  750;


export function ResearchProgress({
  jobId,
}: {
  jobId: string;
}) {
  const [
    job,
    setJob,
  ] = useState<
    ResearchJobStatusResponse | null
  >(null);

  const [
    report,
    setReport,
  ] = useState<
    CompanyInvestmentReport | null
  >(null);

  const [
    error,
    setError,
  ] = useState<
    string | null
  >(null);

  const [
    addingToWatchlist,
    setAddingToWatchlist,
  ] = useState(false);

  const [
    addedToWatchlist,
    setAddedToWatchlist,
  ] = useState(false);

  async function handleAddToWatchlist() {
    if (
      report === null
      || addingToWatchlist
      || addedToWatchlist
    ) {
      return;
    }

    try {
      setAddingToWatchlist(
        true
      );

      await addToWatchlist(
        report.ticker
      );

      setAddedToWatchlist(
        true
      );

    } catch (exception) {
      setError(
        exception
          instanceof Error
          ? exception.message
          : "Unable to add ticker to watchlist.",
      );

    } finally {
      setAddingToWatchlist(
        false
      );
    }
  }

  useEffect(
    () => {
      let cancelled = false;

      let timeout:
        ReturnType<
          typeof setTimeout
        >
        | undefined;


      async function poll() {
        try {
          const status =
            await getResearchJobStatus(
              jobId
            );

          if (cancelled) {
            return;
          }

          setJob(
            status
          );

          if (
            status.status
            === "completed"
          ) {
            const result =
              await getResearchJobResult(
                jobId
              );

            if (!cancelled) {
              setReport(
                result.report
              );
            }

            return;
          }

          if (
            status.status
            === "failed"
          ) {
            setError(
              status.error ??
              "Research failed."
            );

            return;
          }

          timeout =
            setTimeout(
              poll,
              POLL_INTERVAL_MS,
            );

        } catch (exception) {
          if (cancelled) {
            return;
          }

          setError(
            exception
              instanceof Error
              ? exception.message
              : "Unable to retrieve research status.",
          );
        }
      }


      poll();


      return () => {
        cancelled = true;

        if (timeout) {
          clearTimeout(
            timeout
          );
        }
      };
    },
    [
      jobId,
    ],
  );


  if (
    error
  ) {
    return (
      <ResearchError
        message={error}
      />
    );
  }


  if (
    job === null
  ) {
    return (
      <div
        className="
          mx-auto
          max-w-3xl
          py-16
          text-center
        "
      >
        <div
          className="
            text-sm
            text-[var(--muted)]
          "
        >
          Loading research job...
        </div>
      </div>
    );
  }


  return (
    <div
      className="
        mx-auto
        max-w-4xl
      "
    >
      <div
        className="
          flex
          flex-wrap
          items-start
          justify-between
          gap-5
        "
      >
        <div>
          <div
            className="
              flex
              items-center
              gap-2
              text-xs
              uppercase
              tracking-[0.16em]
              text-emerald-400
            "
          >
            <BrainCircuit
              className="
                h-4
                w-4
              "
            />

            Multi-Agent Research
          </div>

          <h1
            className="
              mt-3
              text-3xl
              font-semibold
              tracking-tight
              text-white
            "
          >
            {job.ticker}
          </h1>

          <p
            className="
              mt-2
              text-sm
              text-[var(--muted)]
            "
          >
            {job.status
            === "completed"
              ? "Research complete."
              : "Specialist agents are analyzing the company."}
          </p>
        </div>

        <ProgressValue
          progress={
            job.progress
          }
        />
      </div>

      <div
        className="
          mt-8
          h-1.5
          overflow-hidden
          rounded-full
          bg-white/[0.05]
        "
      >
        <div
          className="
            h-full
            rounded-full
            bg-emerald-400
            transition-all
            duration-500
            ease-out
          "
          style={{
            width:
              `${job.progress * 100}%`,
          }}
        />
      </div>

      <div className="mt-8 flex flex-col gap-3">
        {job.steps.map(
            (step) => {
                const result =
                    job.partial_results?.[
                        step.name as keyof typeof job.partial_results
                    ];

            return (
                <ResearchStep
                    key={step.name}
                    step={step}
                >
                    {result !== undefined && (
                        <AgentResult
                          stepName={step.name}
                          result={result}
                        />
                    )}
                </ResearchStep>
            );
            },
        )}
      </div>

      {report && (
        <div className="space-y-4">
          <ResearchResultPreview
            report={report}
          />

          <div className="flex justify-center">
            <button
              type="button"
              onClick={
                handleAddToWatchlist
              }
              disabled={
                addingToWatchlist
                || addedToWatchlist
              }
              className={
                addedToWatchlist
                  ? "rounded-xl border border-emerald-400/30 bg-emerald-400/[0.08] px-6 py-3 text-sm font-medium text-emerald-300"
                  : "rounded-xl border border-[var(--border)] bg-white/[0.02] px-6 py-3 text-sm font-medium text-white transition hover:border-emerald-400/30 hover:bg-emerald-400/[0.04] disabled:cursor-not-allowed disabled:opacity-60"
              }
            >
              {addedToWatchlist
                ? `${report.ticker} added to Watchlist`
                : addingToWatchlist
                  ? "Adding..."
                  : `Add ${report.ticker} to Watchlist`}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}


function ProgressValue({
  progress,
}: {
  progress: number;
}) {
  return (
    <div
      className="
        rounded-xl
        border
        border-[var(--border)]
        bg-[var(--surface)]
        px-5
        py-3
        text-right
      "
    >
      <div
        className="
          text-lg
          font-semibold
          text-white
        "
      >
        {Math.round(
          progress * 100
        )}
        %
      </div>

      <div
        className="
          text-[10px]
          uppercase
          tracking-[0.12em]
          text-[var(--muted)]
        "
      >
        Complete
      </div>
    </div>
  );
}


function ResearchError({
  message,
}: {
  message: string;
}) {
  return (
    <div
      className="
        mx-auto
        max-w-3xl
        rounded-2xl
        border
        border-red-400/20
        bg-red-400/[0.04]
        p-6
      "
    >
      <div
        className="
          flex
          gap-4
        "
      >
        <AlertCircle
          className="
            mt-0.5
            h-5
            w-5
            shrink-0
            text-red-400
          "
        />

        <div>
          <h2
            className="
              text-sm
              font-semibold
              text-white
            "
          >
            Research failed
          </h2>

          <p
            className="
              mt-2
              text-sm
              leading-6
              text-red-200/70
            "
          >
            {message}
          </p>
          <Link
            href="/"
            className="mt-4 inline-flex rounded-lg border border-red-400/20 px-3 py-2 text-xs font-medium text-red-200 transition hover:bg-red-400/[0.06]"
          >
            Start New Research
          </Link>
        </div>
      </div>
    </div>
  );
}