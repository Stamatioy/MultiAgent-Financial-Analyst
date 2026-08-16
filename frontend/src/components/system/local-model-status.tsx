"use client";

import {
  useEffect,
  useState,
} from "react";

import {
  BrainCircuit,
} from "lucide-react";

import {
  getSystemStatus,
} from "@/lib/api";

import type {
  SystemStatusResponse,
} from "@/lib/types";


const POLL_INTERVAL_MS =
  10_000;


export function LocalModelStatus() {
  const [
    status,
    setStatus,
  ] = useState<
    SystemStatusResponse | null
  >(null);

  const [
    unavailable,
    setUnavailable,
  ] = useState(false);


  useEffect(
    () => {
      let cancelled = false;

      let timeout:
        ReturnType<
          typeof setTimeout
        >
        | undefined;


      async function check() {
        try {
          const result =
            await getSystemStatus();

          if (cancelled) {
            return;
          }

          setStatus(
            result
          );

          setUnavailable(
            false
          );

        } catch {
          if (cancelled) {
            return;
          }

          setUnavailable(
            true
          );
        }


        timeout =
          setTimeout(
            check,
            POLL_INTERVAL_MS,
          );
      }


      check();


      return () => {
        cancelled = true;

        if (timeout) {
          clearTimeout(
            timeout
          );
        }
      };
    },
    [],
  );


  const checking =
    status === null
    && !unavailable;


  const online =
    status?.llm.online
    === true;


  return (
    <div className="rounded-xl border border-[var(--border-soft)] bg-black/10 p-4">
      <div className="flex items-center gap-3">
        <div
          className={
            online
              ? "flex h-9 w-9 items-center justify-center rounded-lg bg-emerald-400/10 text-emerald-400"
              : "flex h-9 w-9 items-center justify-center rounded-lg bg-white/[0.03] text-[var(--muted)]"
          }
        >
          <BrainCircuit className="h-4 w-4" />
        </div>

        <div className="min-w-0 flex-1">
          <div className="text-xs font-medium text-white">
            {status?.llm.model
              ?? "Qwen3-8B"}
          </div>

          <div className="mt-1 flex items-center gap-2">
            <StatusDot
              online={online}
              checking={checking}
            />

            <span
              className={
                online
                  ? "text-[10px] text-emerald-400"
                  : "text-[10px] text-[var(--muted)]"
              }
            >
              {checking
                ? "Checking..."
                : online
                  ? "Local · Online"
                  : "Local · Offline"}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}


function StatusDot({
  online,
  checking,
}: {
  online: boolean;
  checking: boolean;
}) {
  if (checking) {
    return (
      <div className="h-2 w-2 animate-pulse rounded-full bg-amber-400" />
    );
  }

  return (
    <div
      className={
        online
          ? "h-2 w-2 rounded-full bg-emerald-400 shadow-[0_0_8px_rgba(52,211,153,0.55)]"
          : "h-2 w-2 rounded-full bg-red-400"
      }
    />
  );
}