"use client";

import {
  useEffect,
  useState,
} from "react";

import {
  ArrowLeft,
  Clock3,
} from "lucide-react";

import Link from "next/link";

import {
  useParams,
} from "next/navigation";

import {
  getHistoricalReport,
} from "@/lib/api";

import type {
  CompanyInvestmentReport,
} from "@/lib/types";

import {
  ResearchResultPreview,
} from "@/components/research/research-result-preview";


export default function HistoricalResearchPage() {
  const params =
    useParams<{
      researchId: string;
    }>();

  const researchId =
    params.researchId;

  const [
    report,
    setReport,
  ] = useState<
    CompanyInvestmentReport | null
  >(null);

  const [
    loading,
    setLoading,
  ] = useState(true);

  const [
    error,
    setError,
  ] = useState<
    string | null
  >(null);


  useEffect(
    () => {
      async function loadReport() {
        try {
          const result =
            await getHistoricalReport(
              researchId
            );

          setReport(
            result.report
          );

        } catch (exception) {
          setError(
            exception
              instanceof Error
              ? exception.message
              : "Unable to load research report.",
          );

        } finally {
          setLoading(
            false
          );
        }
      }

      loadReport();
    },
    [
      researchId,
    ],
  );


  if (loading) {
    return (
      <div className="mx-auto max-w-5xl py-16 text-center text-sm text-[var(--muted)]">
        Loading research report...
      </div>
    );
  }


  if (
    error
    || report === null
  ) {
    return (
      <div className="mx-auto max-w-5xl">
        <Link
          href="/history"
          className="inline-flex items-center gap-2 text-sm text-[var(--muted-light)] transition hover:text-white"
        >
          <ArrowLeft className="h-4 w-4" />

          Back to history
        </Link>

        <div className="mt-8 rounded-xl border border-red-400/20 bg-red-400/[0.04] p-5 text-sm text-red-200">
          {error ?? "Research report could not be loaded."}
        </div>
      </div>
    );
  }


  return (
    <div className="mx-auto max-w-5xl">
      <Link
        href="/history"
        className="inline-flex items-center gap-2 text-sm text-[var(--muted-light)] transition hover:text-white"
      >
        <ArrowLeft className="h-4 w-4" />

        Back to history
      </Link>

      <div className="mt-8 flex flex-wrap items-start justify-between gap-5">
        <div>
          <div className="flex items-center gap-2 text-xs uppercase tracking-[0.16em] text-emerald-400">
            <Clock3 className="h-4 w-4" />

            Historical Research
          </div>

          <h1 className="mt-3 text-3xl font-semibold tracking-tight text-white">
            {report.ticker}
          </h1>

          <p className="mt-2 text-sm text-[var(--muted)]">
            Research completed{" "}
            {formatDate(
              report.generated_at
            )}
          </p>
        </div>

        <div className="rounded-xl border border-[var(--border)] bg-white/[0.015] px-5 py-3">
          <div className="text-[10px] uppercase tracking-[0.12em] text-[var(--muted)]">
            Recommendation
          </div>

          <div className="mt-1 text-sm font-semibold text-white">
            {formatLabel(
              report.committee.recommendation
            )}
          </div>
        </div>
      </div>

      <ResearchResultPreview
        report={report}
      />
    </div>
  );
}


function formatLabel(
  value: string,
): string {
  return value
    .replace(
      /_/g,
      " ",
    )
    .replace(
      /\b\w/g,
      (character) =>
        character.toUpperCase(),
    );
}


function formatDate(
  value: string,
): string {
  return new Date(
    value
  ).toLocaleString();
}