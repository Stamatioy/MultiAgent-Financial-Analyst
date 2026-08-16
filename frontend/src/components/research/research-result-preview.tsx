import {
  ArrowUpRight,
} from "lucide-react";

import {
  CompanyInvestmentReport,
} from "@/lib/types";

import {
  formatLabel,
  formatPercent,
} from "@/lib/format";


export function ResearchResultPreview({
  report,
}: {
  report: CompanyInvestmentReport;
}) {
  const committee =
    report.committee;

  return (
    <div
      className="
        mt-7
        animate-fade-in-up
        rounded-2xl
        border
        border-emerald-400/20
        bg-emerald-400/[0.025]
        p-6
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
              text-xs
              uppercase
              tracking-[0.16em]
              text-emerald-400
            "
          >
            Investment Committee
          </div>

          <h2
            className="
              mt-2
              text-2xl
              font-semibold
              text-white
            "
          >
            {report.ticker}
          </h2>
        </div>

        <div
          className="
            rounded-full
            border
            border-amber-400/20
            bg-amber-400/10
            px-4
            py-2
            text-xs
            font-semibold
            uppercase
            tracking-[0.13em]
            text-amber-300
          "
        >
          {formatLabel(
            committee.recommendation,
          )}
        </div>
      </div>

      <div
        className="
          mt-6
          grid
          gap-4
          sm:grid-cols-3
        "
      >
        <Metric
          label="Confidence"
          value={formatPercent(
            committee.confidence_score,
            0,
          )}
        />

        <Metric
          label="Conviction"
          value={formatLabel(
            committee.conviction,
          )}
        />

        <Metric
          label="Horizon"
          value={formatLabel(
            committee.investment_horizon,
          )}
        />
      </div>

      <div
        className="
          mt-6
          border-t
          border-[var(--border)]
          pt-5
        "
      >
        <div
          className="
            text-xs
            font-medium
            text-white
          "
        >
          Investment thesis
        </div>

        <p
          className="
            mt-2
            max-w-4xl
            text-sm
            leading-7
            text-[var(--muted-light)]
          "
        >
          {committee.thesis}
        </p>
      </div>

      <div
        className="
          mt-6
          flex
          items-center
          gap-2
          text-xs
          text-emerald-400
        "
      >
        

        

        <span
          className="
            text-[var(--muted)]
          "
        >
          
        </span>
      </div>
    </div>
  );
}


function Metric({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <div
      className="
        rounded-xl
        border
        border-[var(--border)]
        bg-[#0a0f16]
        p-4
      "
    >
      <div
        className="
          text-[10px]
          uppercase
          tracking-[0.14em]
          text-[var(--muted)]
        "
      >
        {label}
      </div>

      <div
        className="
          mt-2
          text-sm
          font-medium
          text-white
        "
      >
        {value}
      </div>
    </div>
  );
}