"use client";

import {
  FormEvent,
  useState,
} from "react";

import {
  AlertCircle,
  ArrowRight,
  LoaderCircle,
  Search,
} from "lucide-react";

import {
  createResearchJob,
} from "@/lib/api";

import {
  useRouter,
} from "next/navigation";

import {
  CompanyInvestmentReport,
} from "@/lib/types";

import {
  formatLabel,
  formatPercent,
} from "@/lib/format";


const DEFAULT_QUERY =
  "material company developments, earnings, " +
  "guidance, products, competition and risks";


export function ResearchForm() {
  const [ticker, setTicker] =
    useState("AMD");

  const [fiscalYear, setFiscalYear] =
    useState(2025);

  const [marketYears, setMarketYears] =
    useState(5);

  const [newsLimit, setNewsLimit] =
    useState(15);

  const [newsQuery, setNewsQuery] =
    useState(DEFAULT_QUERY);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState<string | null>(
      null,
    );

  const router =
    useRouter();
  const [report, setReport] =
    useState<
      CompanyInvestmentReport | null
    >(null);


  async function handleSubmit(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    setError(null);
    setReport(null);
    setLoading(true);

    try {
      const job =
        await createResearchJob({
          ticker:
            ticker
              .trim()
              .toUpperCase(),

          fiscal_year:
            fiscalYear,

          market_years:
            marketYears,

          benchmark_ticker:
            "^GSPC",

          risk_free_rate_annual:
            0.0,

          news_query:
            newsQuery.trim(),

          news_limit:
            newsLimit,

          refresh_market:
            false,

          refresh_fundamentals:
            false,
        });

      router.push(
        `/research/${job.job_id}`
      );
    } catch (exception) {
      if (
        exception instanceof Error
      ) {
        setError(
          exception.message,
        );
      } else {
        setError(
          "Unknown research error.",
        );
      }
    } finally {
      setLoading(false);
    }
  }


  return (
    <section
      className="
        rounded-2xl
        border
        border-[var(--border)]
        bg-[var(--surface)]
        p-6
      "
    >
      <div>
        <h2
          className="
            text-base
            font-semibold
            text-white
          "
        >
          Research a company
        </h2>

        <p
          className="
            mt-1
            text-xs
            leading-5
            text-[var(--muted)]
          "
        >
          Run the complete multi-agent
          research pipeline.
        </p>
      </div>

      <form
        onSubmit={
          handleSubmit
        }
        className="
          mt-6
          space-y-5
        "
      >
        <div>
          <label
            className="
              mb-2
              block
              text-xs
              font-medium
              text-[var(--muted-light)]
            "
          >
            Stock ticker
          </label>

          <div className="relative">
            <Search
              className="
                absolute
                left-3.5
                top-1/2
                h-4
                w-4
                -translate-y-1/2
                text-[var(--muted)]
              "
            />

            <input
              value={ticker}
              onChange={(
                event,
              ) =>
                setTicker(
                  event.target.value,
                )
              }
              required
              placeholder="AMD"
              className="
                h-11
                w-full
                rounded-xl
                border
                border-[var(--border)]
                bg-[#0a0f16]
                pl-10
                pr-4
                text-sm
                font-medium
                uppercase
                tracking-wide
                text-white
                outline-none
                transition
                placeholder:text-[#465264]
                focus:border-emerald-400/40
              "
            />
          </div>
        </div>

        <div
          className="
            grid
            gap-4
            sm:grid-cols-3
          "
        >
          <NumberField
            label="Fiscal Year"
            value={fiscalYear}
            onChange={
              setFiscalYear
            }
            min={2000}
            max={2100}
          />

          <NumberField
            label="Market History"
            value={marketYears}
            onChange={
              setMarketYears
            }
            min={1}
            max={30}
            suffix="years"
          />

          <NumberField
            label="News Limit"
            value={newsLimit}
            onChange={
              setNewsLimit
            }
            min={1}
            max={50}
            suffix="articles"
          />
        </div>

        <div>
          <label
            className="
              mb-2
              block
              text-xs
              font-medium
              text-[var(--muted-light)]
            "
          >
            Research focus
          </label>

          <textarea
            value={newsQuery}
            onChange={(
              event,
            ) =>
              setNewsQuery(
                event.target.value,
              )
            }
            rows={3}
            className="
              w-full
              resize-none
              rounded-xl
              border
              border-[var(--border)]
              bg-[#0a0f16]
              px-4
              py-3
              text-sm
              leading-6
              text-white
              outline-none
              transition
              placeholder:text-[#465264]
              focus:border-emerald-400/40
            "
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="
            flex
            h-11
            w-full
            items-center
            justify-center
            gap-2
            rounded-xl
            bg-emerald-400
            px-5
            text-sm
            font-semibold
            text-[#07110d]
            transition
            hover:bg-emerald-300
            disabled:cursor-not-allowed
            disabled:opacity-60
          "
        >
          {loading ? (
            <>
              <LoaderCircle
                className="
                  h-4
                  w-4
                  animate-spin
                "
              />

              Running research...
            </>
          ) : (
            <>
              Analyze Company

              <ArrowRight
                className="
                  h-4
                  w-4
                "
              />
            </>
          )}
        </button>
      </form>

      {error && (
        <div
          className="
            mt-5
            flex
            items-start
            gap-3
            rounded-xl
            border
            border-red-400/20
            bg-red-400/[0.05]
            p-4
          "
        >
          <AlertCircle
            className="
              mt-0.5
              h-4
              w-4
              shrink-0
              text-red-400
            "
          />

          <div>
            <div
              className="
                text-xs
                font-medium
                text-red-300
              "
            >
              Research failed
            </div>

            <div
              className="
                mt-1
                text-xs
                leading-5
                text-red-200/70
              "
            >
              {error}
            </div>
          </div>
        </div>
      )}

    </section>
  );
}


function NumberField({
  label,
  value,
  onChange,
  min,
  max,
  suffix,
}: {
  label: string;
  value: number;
  onChange: (
    value: number,
  ) => void;
  min: number;
  max: number;
  suffix?: string;
}) {
  return (
    <div>
      <label
        className="
          mb-2
          block
          text-xs
          font-medium
          text-[var(--muted-light)]
        "
      >
        {label}
      </label>

      <div className="relative">
        <input
          type="number"
          value={value}
          min={min}
          max={max}
          onChange={(
            event,
          ) =>
            onChange(
              Number(
                event.target.value,
              ),
            )
          }
          className="
            h-11
            w-full
            rounded-xl
            border
            border-[var(--border)]
            bg-[#0a0f16]
            px-4
            pr-14
            text-sm
            text-white
            outline-none
            transition
            focus:border-emerald-400/40
          "
        />

        {suffix && (
          <span
            className="
              absolute
              right-3
              top-1/2
              -translate-y-1/2
              text-[10px]
              text-[var(--muted)]
            "
          >
            {suffix}
          </span>
        )}
      </div>
    </div>
  );
}


