"use client";

import {
  useEffect,
  useState,
} from "react";

import Link from "next/link";

import {
  Clock3,
  FileSearch,
} from "lucide-react";

import {
  getResearchHistory,
} from "@/lib/api";

import type {
  ResearchHistoryItem,
} from "@/lib/types";


export default function HistoryPage() {
  const [
    items,
    setItems,
  ] = useState<
    ResearchHistoryItem[]
  >([]);

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
      async function load() {
        try {
          const result =
            await getResearchHistory();

          setItems(
            result.items
          );

        } catch (exception) {
          setError(
            exception
              instanceof Error
              ? exception.message
              : "Unable to load history.",
          );

        } finally {
          setLoading(
            false
          );
        }
      }

      load();
    },
    [],
  );


  return (
    <div className="mx-auto max-w-6xl">
      <div>
        <div className="flex items-center gap-2 text-xs uppercase tracking-[0.16em] text-emerald-400">
          <Clock3 className="h-4 w-4" />

          Research History
        </div>

        <h1 className="mt-3 text-3xl font-semibold tracking-tight text-white">
          Previous Research
        </h1>

        <p className="mt-2 max-w-2xl text-sm leading-6 text-[var(--muted)]">
          Review completed company analyses and revisit previous
          Investment Committee decisions.
        </p>
      </div>


      {loading && (
        <div className="mt-10 text-sm text-[var(--muted)]">
          Loading research history...
        </div>
      )}


      {error && (
        <div className="mt-10 rounded-xl border border-red-400/20 bg-red-400/[0.04] p-4 text-sm text-red-200">
          {error}
        </div>
      )}


      {!loading
        && !error
        && items.length === 0
        && (
          <div className="mt-10 rounded-2xl border border-[var(--border-soft)] bg-white/[0.015] p-10 text-center">
            <FileSearch className="mx-auto h-8 w-8 text-[var(--muted)]" />

            <div className="mt-4 text-sm font-medium text-white">
              No research yet
            </div>

            <div className="mt-2 text-sm text-[var(--muted)]">
              Completed analyses will appear here.
            </div>
          </div>
        )}


      {items.length > 0 && (
        <div className="mt-8 flex flex-col gap-3">
          {items.map(
            (item) => (
              <Link
                key={
                  item.research_id
                }
                href={
                  `/history/${item.research_id}`
                }
                className="group flex flex-wrap items-center justify-between gap-6 rounded-xl border border-[var(--border)] bg-white/[0.015] px-5 py-4 transition hover:border-emerald-400/30 hover:bg-white/[0.025]"
              >
                <div>
                  <div className="text-lg font-semibold text-white">
                    {item.ticker}
                  </div>

                  <div className="mt-1 text-xs text-[var(--muted)]">
                    {formatDate(
                      item.generated_at
                    )}
                  </div>
                </div>

                <div className="flex flex-wrap items-center gap-8">
                  <HistoryMetric
                    label="Recommendation"
                    value={
                      formatLabel(
                        item.recommendation
                      )
                    }
                  />

                  <HistoryMetric
                    label="Confidence"
                    value={`${Math.round(
                      item.confidence_score
                      * 100
                    )}%`}
                  />

                  <HistoryMetric
                    label="Horizon"
                    value={
                      formatLabel(
                        item.investment_horizon
                      )
                    }
                  />
                </div>
              </Link>
            ),
          )}
        </div>
      )}
    </div>
  );
}


function HistoryMetric({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <div>
      <div className="text-[10px] uppercase tracking-[0.12em] text-[var(--muted)]">
        {label}
      </div>

      <div className="mt-1 text-sm font-medium text-white">
        {value}
      </div>
    </div>
  );
}


function formatLabel(
  value: string,
) {
  return value
    .replace(
      /_/g,
      " ",
    )
    .replace(
      /\b\w/g,
      (
        character
      ) =>
        character.toUpperCase(),
    );
}


function formatDate(
  value: string,
) {
  return new Date(
    value
  ).toLocaleString();
}