"use client";

import {
  FormEvent,
  useEffect,
  useState,
} from "react";

import Link from "next/link";

import {
  Bookmark,
  Plus,
  Search,
  Trash2,
} from "lucide-react";

import {
  addToWatchlist,
  getWatchlist,
  removeFromWatchlist,
} from "@/lib/api";

import type {
  WatchlistItem,
} from "@/lib/types";


export default function WatchlistPage() {
  const [
    items,
    setItems,
  ] = useState<
    WatchlistItem[]
  >([]);

  const [
    ticker,
    setTicker,
  ] = useState("");

  const [
    loading,
    setLoading,
  ] = useState(true);

  const [
    submitting,
    setSubmitting,
  ] = useState(false);

  const [
    error,
    setError,
  ] = useState<
    string | null
  >(null);


  useEffect(
    () => {
      loadWatchlist();
    },
    [],
  );


  async function loadWatchlist() {
    try {
      setError(null);

      const result =
        await getWatchlist();

      setItems(
        result.items
      );

    } catch (exception) {
      setError(
        getErrorText(
          exception
        )
      );

    } finally {
      setLoading(false);
    }
  }


  async function handleSubmit(
    event: FormEvent,
  ) {
    event.preventDefault();

    const normalized =
      ticker
        .trim()
        .toUpperCase();

    if (!normalized) {
      return;
    }

    try {
      setSubmitting(true);
      setError(null);

      await addToWatchlist(
        normalized
      );

      setTicker("");

      await loadWatchlist();

    } catch (exception) {
      setError(
        getErrorText(
          exception
        )
      );

    } finally {
      setSubmitting(false);
    }
  }


  async function handleRemove(
    tickerToRemove: string,
  ) {
    try {
      setError(null);

      await removeFromWatchlist(
        tickerToRemove
      );

      setItems(
        (
          current
        ) =>
          current.filter(
            (
              item
            ) =>
              item.ticker
              !== tickerToRemove,
          ),
      );

    } catch (exception) {
      setError(
        getErrorText(
          exception
        )
      );
    }
  }


  return (
    <div className="mx-auto max-w-6xl">
      <div className="flex flex-wrap items-end justify-between gap-6">
        <div>
          <div className="flex items-center gap-2 text-xs uppercase tracking-[0.16em] text-emerald-400">
            <Bookmark className="h-4 w-4" />

            Watchlist
          </div>

          <h1 className="mt-3 text-3xl font-semibold tracking-tight text-white">
            Companies to Watch
          </h1>

          <p className="mt-2 max-w-2xl text-sm leading-6 text-[var(--muted)]">
            Save companies you want to revisit and
            compare their latest Investment Committee
            assessments.
          </p>
        </div>
      </div>


      <form
        onSubmit={
          handleSubmit
        }
        className="mt-8 flex max-w-lg gap-3"
      >
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-[var(--muted)]" />

          <input
            value={ticker}
            onChange={
              (
                event
              ) =>
                setTicker(
                  event.target.value
                    .toUpperCase()
                )
            }
            placeholder="Enter ticker, e.g. AMD"
            className="h-11 w-full rounded-lg border border-[var(--border)] bg-white/[0.02] pl-10 pr-3 text-sm text-white outline-none transition placeholder:text-[var(--muted)] focus:border-emerald-400/40"
          />
        </div>

        <button
          type="submit"
          disabled={
            submitting
          }
          className="flex h-11 items-center gap-2 rounded-lg bg-emerald-400 px-4 text-sm font-medium text-black transition hover:bg-emerald-300 disabled:cursor-not-allowed disabled:opacity-50"
        >
          <Plus className="h-4 w-4" />

          Add
        </button>
      </form>


      {error && (
        <div className="mt-5 rounded-xl border border-red-400/20 bg-red-400/[0.04] p-4 text-sm text-red-200">
          {error}
        </div>
      )}


      {loading && (
        <div className="mt-10 text-sm text-[var(--muted)]">
          Loading watchlist...
        </div>
      )}


      {!loading
        && items.length === 0
        && (
          <EmptyWatchlist />
        )}


      {items.length > 0 && (
        <div className="mt-8 flex flex-col gap-3">
          {items.map(
            (
              item
            ) => (
              <WatchlistCard
                key={
                  item.ticker
                }
                item={item}
                onRemove={
                  handleRemove
                }
              />
            ),
          )}
        </div>
      )}
    </div>
  );
}


function WatchlistCard({
  item,
  onRemove,
}: {
  item: WatchlistItem;

  onRemove: (
    ticker: string
  ) => void;
}) {
  const hasResearch =
    item.research_id
    !== null;

  return (
    <div className="flex flex-wrap items-center justify-between gap-6 rounded-xl border border-[var(--border)] bg-white/[0.015] px-5 py-5">
      <div className="min-w-40">
        <div className="text-xl font-semibold text-white">
          {item.ticker}
        </div>

        <div className="mt-1 text-xs text-[var(--muted)]">
          {item.last_researched_at
            ? `Last researched ${formatDate(
                item.last_researched_at
              )}`
            : "No research available yet"}
        </div>
      </div>


      {hasResearch ? (
        <div className="flex flex-1 flex-wrap items-center justify-end gap-8">
          <WatchlistMetric
            label="Recommendation"
            value={
              formatLabel(
                item.recommendation
                ?? "—"
              )
            }
          />

          <WatchlistMetric
            label="Confidence"
            value={
              item.confidence_score
              !== null
                ? `${Math.round(
                    item.confidence_score
                    * 100
                  )}%`
                : "—"
            }
          />

          <WatchlistMetric
            label="Horizon"
            value={
              formatLabel(
                item.investment_horizon
                ?? "—"
              )
            }
          />

          {item.research_id && (
            <Link
              href={
                `/history/${item.research_id}`
              }
              className="rounded-lg border border-[var(--border)] px-3 py-2 text-xs font-medium text-white transition hover:border-emerald-400/30 hover:bg-emerald-400/[0.03]"
            >
              View Research
            </Link>
          )}

          <RemoveButton
            ticker={
              item.ticker
            }
            onRemove={
              onRemove
            }
          />
        </div>
      ) : (
        <div className="flex items-center gap-3">
          <Link
            href="/"
            className="rounded-lg border border-emerald-400/20 bg-emerald-400/[0.04] px-3 py-2 text-xs font-medium text-emerald-300 transition hover:bg-emerald-400/[0.08]"
          >
            Research Company
          </Link>

          <RemoveButton
            ticker={
              item.ticker
            }
            onRemove={
              onRemove
            }
          />
        </div>
      )}
    </div>
  );
}


function WatchlistMetric({
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


function RemoveButton({
  ticker,
  onRemove,
}: {
  ticker: string;

  onRemove: (
    ticker: string
  ) => void;
}) {
  return (
    <button
      type="button"
      onClick={() =>
        onRemove(
          ticker
        )
      }
      aria-label={
        `Remove ${ticker} from watchlist`
      }
      className="flex h-9 w-9 items-center justify-center rounded-lg border border-[var(--border)] text-[var(--muted)] transition hover:border-red-400/30 hover:bg-red-400/[0.04] hover:text-red-300"
    >
      <Trash2 className="h-4 w-4" />
    </button>
  );
}


function EmptyWatchlist() {
  return (
    <div className="mt-10 rounded-2xl border border-[var(--border-soft)] bg-white/[0.015] p-10 text-center">
      <Bookmark className="mx-auto h-8 w-8 text-[var(--muted)]" />

      <div className="mt-4 text-sm font-medium text-white">
        Your watchlist is empty
      </div>

      <div className="mt-2 text-sm text-[var(--muted)]">
        Add a ticker above to start tracking it.
      </div>
    </div>
  );
}


function formatLabel(
  value: string,
) {
  if (value === "—") {
    return value;
  }

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
  ).toLocaleDateString(
    undefined,
    {
      year: "numeric",
      month: "short",
      day: "numeric",
    },
  );
}


function getErrorText(
  exception: unknown,
) {
  return exception
    instanceof Error
      ? exception.message
      : "Something went wrong.";
}