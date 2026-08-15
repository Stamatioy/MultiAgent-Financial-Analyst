"use client";

import {
  ArrowDownRight,
  ArrowUpRight,
  CircleAlert,
  CircleCheck,
  CircleDot,
  Newspaper,
  ShieldAlert,
  Sparkles,
} from "lucide-react";

import type{
  DrawdownPoint,
  FinancialHistoryPoint,
  PriceHistoryPoint,
} from "@/lib/types";

import {
  DrawdownChart,
} from "@/components/charts/drawdown-chart";

import {
  FinancialHistoryChart,
} from "@/components/charts/financial-history-chart";

import {
  PriceHistoryChart,
} from "@/components/charts/price-history-chart";



type AgentResultProps = {
  stepName: string;
  result: unknown;
};


export function AgentResult({
  stepName,
  result,
}: AgentResultProps) {
  if (
    result === null
    || result === undefined
    || typeof result !== "object"
  ) {
    return null;
  }

  const data =
    result as Record<
      string,
      unknown
    >;

  switch (stepName) {
    case "market":
      return (
        <MarketResult
          data={data}
        />
      );

    case "fundamentals":
      return (
        <FundamentalResult
          data={data}
        />
      );

    case "valuation":
      return (
        <ValuationResult
          data={data}
        />
      );

    case "risk":
      return (
        <RiskResult
          data={data}
        />
      );

    case "news":
      return (
        <NewsResult
          data={data}
        />
      );

    case "committee":
      return (
        <CommitteeResult
          data={data}
        />
      );

    default:
      return (
        <GenericResult
          data={data}
        />
      );
  }
}


function MarketResult({
  data,
}: {
  data: Record<string, unknown>;
}) {
  const charts =
    getCharts(data);

  const priceHistory: PriceHistoryPoint[] =
    Array.isArray(charts.price_history)
      ? (
          charts.price_history as PriceHistoryPoint[]
        )
      : [];

  return (
    <ResultLayout>
      <MetricRow>
        <Metric
          label="Momentum"
          value={formatLabel(
            data.momentum
          )}
        />

        <Metric
          label="Risk"
          value={formatLabel(
            data.risk_level
          )}
        />
      </MetricRow>

      <TextSection
        title="Trend"
        text={data.trend_summary}
      />

      <TextSection
        title="Short-term view"
        text={data.short_term_view}
      />

      <TextSection
        title="Long-term view"
        text={data.long_term_price_view}
      />

      <SignalColumns
        positive={toStringArray(
          data.positive_signals
        )}
        negative={toStringArray(
          data.negative_signals
        )}
      />

      <PriceHistoryChart
        data={priceHistory}
      />

      <Conclusion
        text={data.conclusion}
      />
    </ResultLayout>
  );
}


function FundamentalResult({
  data,
}: {
  data: Record<string, unknown>;
}) {
  const charts =
    getCharts(data);

  const financialHistory: FinancialHistoryPoint[] =
    Array.isArray(charts.financial_history)
      ? (
          charts.financial_history as FinancialHistoryPoint[]
        )
      : [];

  return (
    <ResultLayout>
      <MetricRow>
        <Metric
          label="Growth"
          value={formatLabel(
            data.growth
          )}
        />

        <Metric
          label="Profitability"
          value={formatLabel(
            data.profitability
          )}
        />

        <Metric
          label="Cash Flow"
          value={formatLabel(
            data.cash_flow
          )}
        />

        <Metric
          label="Balance Sheet"
          value={formatLabel(
            data.balance_sheet
          )}
        />
      </MetricRow>

      <TextSection
        title="Growth"
        text={data.growth_summary}
      />

      <TextSection
        title="Profitability"
        text={
          data.profitability_summary
        }
      />

      <TextSection
        title="Cash Flow"
        text={data.cash_flow_summary}
      />

      <TextSection
        title="Balance Sheet"
        text={
          data.balance_sheet_summary
        }
      />

      <SignalColumns
        positive={toStringArray(
          data.strengths
        )}
        negative={toStringArray(
          data.weaknesses
        )}
        positiveTitle="Strengths"
        negativeTitle="Weaknesses"
      />

      <FinancialHistoryChart
        data={financialHistory}
      />

      <Conclusion
        text={data.conclusion}
      />
    </ResultLayout>
  );
}


function ValuationResult({
  data,
}: {
  data: Record<string, unknown>;
}) {
  return (
    <ResultLayout>
      <MetricRow>
        <Metric
          label="Valuation"
          value={formatLabel(
            data.overall_valuation
          )}
        />

        <Metric
          label="Valuation Risk"
          value={formatLabel(
            data.valuation_risk
          )}
        />
      </MetricRow>

      <TextSection
        title="Earnings valuation"
        text={
          data.earnings_valuation_summary
        }
      />

      <TextSection
        title="Revenue valuation"
        text={
          data.revenue_valuation_summary
        }
      />

      <TextSection
        title="Cash-flow valuation"
        text={
          data.cash_flow_valuation_summary
        }
      />

      <TextSection
        title="Enterprise valuation"
        text={
          data.enterprise_valuation_summary
        }
      />

      <SignalColumns
        positive={toStringArray(
          data.valuation_supports
        )}
        negative={toStringArray(
          data.valuation_concerns
        )}
        positiveTitle="Supports"
        negativeTitle="Concerns"
      />

      <Conclusion
        text={data.conclusion}
      />
    </ResultLayout>
  );
}


function RiskResult({
  data,
}: {
  data: Record<string, unknown>;
}) {
  const charts =
    getCharts(data);

  const drawdownHistory: DrawdownPoint[] =
    Array.isArray(charts.drawdown_history)
      ? (
          charts.drawdown_history as DrawdownPoint[]
        )
      : [];

  return (
    <ResultLayout>
      <MetricRow>
        <Metric
          label="Overall Risk"
          value={formatLabel(
            data.overall_risk
          )}
        />

        <Metric
          label="Market"
          value={formatLabel(
            data.market_risk
          )}
        />

        <Metric
          label="Downside"
          value={formatLabel(
            data.downside_risk
          )}
        />

        <Metric
          label="Financial"
          value={formatLabel(
            data.financial_risk
          )}
        />
      </MetricRow>

      <TextSection
        title="Market risk"
        text={
          data.market_risk_summary
        }
      />

      <TextSection
        title="Downside risk"
        text={
          data.downside_risk_summary
        }
      />

      <TextSection
        title="Financial risk"
        text={
          data.financial_risk_summary
        }
      />

      <TextSection
        title="Liquidity risk"
        text={
          data.liquidity_risk_summary
        }
      />

      <SignalColumns
        positive={toStringArray(
          data.risk_mitigants
        )}
        negative={toStringArray(
          data.risk_factors
        )}
        positiveTitle="Risk mitigants"
        negativeTitle="Risk factors"
      />

      <DrawdownChart
        data={drawdownHistory}
      />

      <Conclusion
        text={data.conclusion}
      />
    </ResultLayout>
  );
}


function NewsResult({
  data,
}: {
  data: Record<string, unknown>;
}) {
  const events =
    Array.isArray(data.events)
      ? data.events
      : [];

  const sources =
    Array.isArray(data._sources)
      ? data._sources
      : [];

  return (
    <ResultLayout>
      <MetricRow>
        <Metric
          label="Sentiment"
          value={formatLabel(
            data.overall_sentiment
          )}
        />

        <Metric
          label="Articles"
          value={String(
            data.article_count ?? "—"
          )}
        />

        <Metric
          label="Events"
          value={String(
            data.distinct_event_count
            ?? "—"
          )}
        />
      </MetricRow>

      <TextSection
        title="News summary"
        text={data.overall_summary}
      />

      {events.length > 0 && (
        <div>
          <SectionTitle>
            Material Events
          </SectionTitle>

          <div className="mt-3 flex flex-col gap-3">
            {events.map(
              (
                event,
                index,
              ) => {
                if (
                  typeof event !== "object"
                  || event === null
                ) {
                  return null;
                }

                const item =
                  event as Record<
                    string,
                    unknown
                  >;

                const supportingIds =
                  Array.isArray(
                    item.supporting_article_ids
                  )
                    ? item.supporting_article_ids.filter(
                        (
                          value,
                        ): value is string =>
                          typeof value === "string",
                      )
                    : [];

                const eventSources =
                  sources.filter(
                    (source) => {
                      if (
                        typeof source !== "object"
                        || source === null
                      ) {
                        return false;
                      }

                      const sourceData =
                        source as Record<
                          string,
                          unknown
                        >;

                      return (
                        typeof sourceData.article_id
                          === "string"
                        && supportingIds.includes(
                          sourceData.article_id
                        )
                      );
                    },
                  );

                return (
                  <div
                    key={String(
                      item.event_id
                      ?? index
                    )}
                    className="rounded-xl border border-[var(--border-soft)] bg-white/[0.015] p-4"
                  >
                    <div className="flex flex-wrap items-center gap-2">
                      <Newspaper className="h-4 w-4 text-[var(--muted-light)]" />

                      <span className="text-sm font-medium text-white">
                        {String(
                          item.headline
                          ?? "News event"
                        )}
                      </span>

                      <Badge
                        value={
                          item.sentiment
                        }
                      />

                      <Badge
                        value={
                          item.materiality
                        }
                      />
                    </div>

                    <p className="mt-3 text-sm leading-6 text-[var(--muted-light)]">
                      {String(
                        item.summary
                        ?? ""
                      )}
                    </p>

                    {eventSources.length > 0 && (
                      <div className="mt-4 border-t border-[var(--border-soft)] pt-3">
                        <div className="text-[10px] uppercase tracking-[0.12em] text-[var(--muted)]">
                          Sources
                        </div>

                        <div className="mt-2 flex flex-col gap-2">
                          {eventSources.map(
                            (
                              source,
                              sourceIndex,
                            ) => {
                              const sourceData =
                                source as Record<
                                  string,
                                  unknown
                                >;

                              const url =
                                typeof sourceData.url
                                  === "string"
                                  ? sourceData.url
                                  : null;

                              const title =
                                typeof sourceData.title
                                  === "string"
                                  ? sourceData.title
                                  : "Source article";

                              const publisher =
                                typeof sourceData.publisher
                                  === "string"
                                  ? sourceData.publisher
                                  : null;

                              if (!url) {
                                return null;
                              }

                              return (
                                <a
                                  key={String(
                                    sourceData.article_id
                                    ?? sourceIndex
                                  )}
                                  href={url}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="group flex items-center justify-between gap-4 rounded-lg border border-[var(--border-soft)] bg-black/10 px-3 py-2 transition hover:border-emerald-400/30 hover:bg-emerald-400/[0.03]"
                                >
                                  <div className="min-w-0">
                                    <div className="truncate text-xs font-medium text-white/80 transition group-hover:text-white">
                                      {title}
                                    </div>

                                    {publisher && (
                                      <div className="mt-0.5 text-[10px] text-[var(--muted)]">
                                        {publisher}
                                      </div>
                                    )}
                                  </div>

                                  <span className="shrink-0 text-xs text-emerald-400">
                                    Open ↗
                                  </span>
                                </a>
                              );
                            },
                          )}
                        </div>
                      </div>
                    )}
                  </div>
                );
              },
            )}
          </div>
        </div>
      )}

      <SignalColumns
        positive={toStringArray(
          data.major_positive_developments
        )}
        negative={toStringArray(
          data.major_negative_developments
        )}
        positiveTitle="Positive developments"
        negativeTitle="Negative developments"
      />
    </ResultLayout>
  );
}


function CommitteeResult({
  data,
}: {
  data: Record<string, unknown>;
}) {
  return (
    <ResultLayout>
      <div className="rounded-xl border border-amber-400/20 bg-amber-400/[0.035] p-5">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <div className="text-[10px] uppercase tracking-[0.16em] text-[var(--muted)]">
              Recommendation
            </div>

            <div className="mt-2 text-xl font-semibold text-amber-300">
              {formatLabel(
                data.recommendation
              )}
            </div>
          </div>

          <div className="text-right">
            <div className="text-[10px] uppercase tracking-[0.16em] text-[var(--muted)]">
              Confidence
            </div>

            <div className="mt-2 text-xl font-semibold text-white">
              {formatPercent(
                data.confidence_score
              )}
            </div>
          </div>
        </div>
      </div>

      <TextSection
        title="Investment Thesis"
        text={data.thesis}
      />

      <div className="grid gap-4 lg:grid-cols-2">
        <CaseCard
          type="bull"
          title="Bull Case"
          text={data.bull_case}
        />

        <CaseCard
          type="bear"
          title="Bear Case"
          text={data.bear_case}
        />
      </div>

      <SignalColumns
        positive={toStringArray(
          data.key_catalysts
        )}
        negative={toStringArray(
          data.key_risks
        )}
        positiveTitle="Key catalysts"
        negativeTitle="Key risks"
      />

      <TextSection
        title="Market View"
        text={data.market_view}
      />

      <TextSection
        title="Fundamental View"
        text={data.fundamental_view}
      />

      <TextSection
        title="Valuation View"
        text={data.valuation_view}
      />

      <TextSection
        title="Risk View"
        text={data.risk_view}
      />

      <TextSection
        title="News View"
        text={data.news_view}
      />

      <Conclusion
        text={data.final_summary}
      />
    </ResultLayout>
  );
}


function GenericResult({
  data,
}: {
  data: Record<string, unknown>;
}) {
  return (
    <ResultLayout>
      {Object.entries(
        data
      ).map(
        ([
          key,
          value,
        ]) => (
          <div
            key={key}
          >
            <SectionTitle>
              {formatLabel(
                key
              )}
            </SectionTitle>

            <div className="mt-2 text-sm leading-6 text-[var(--muted-light)]">
              {typeof value
              === "string"
                ? value
                : JSON.stringify(
                    value
                  )}
            </div>
          </div>
        ),
      )}
    </ResultLayout>
  );
}


function ResultLayout({
  children,
}: {
  children:
    React.ReactNode;
}) {
  return (
    <div className="space-y-6">
      {children}
    </div>
  );
}


function MetricRow({
  children,
}: {
  children:
    React.ReactNode;
}) {
  return (
    <div className="flex flex-wrap gap-3">
      {children}
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
    <div className="min-w-32 rounded-lg border border-[var(--border-soft)] bg-black/10 px-4 py-3">
      <div className="text-[10px] uppercase tracking-[0.12em] text-[var(--muted)]">
        {label}
      </div>

      <div className="mt-1 text-sm font-medium text-white">
        {value}
      </div>
    </div>
  );
}


function TextSection({
  title,
  text,
}: {
  title: string;
  text: unknown;
}) {
  if (
    typeof text !== "string"
    || !text
  ) {
    return null;
  }

  return (
    <div>
      <SectionTitle>
        {title}
      </SectionTitle>

      <p className="mt-2 text-sm leading-6 text-[var(--muted-light)]">
        {text}
      </p>
    </div>
  );
}


function SectionTitle({
  children,
}: {
  children:
    React.ReactNode;
}) {
  return (
    <h4 className="text-[11px] font-medium uppercase tracking-[0.14em] text-[var(--muted)]">
      {children}
    </h4>
  );
}


function SignalColumns({
  positive,
  negative,
  positiveTitle = "Positive signals",
  negativeTitle = "Negative signals",
}: {
  positive: string[];
  negative: string[];
  positiveTitle?: string;
  negativeTitle?: string;
}) {
  if (
    positive.length === 0
    && negative.length === 0
  ) {
    return null;
  }

  return (
    <div className="grid gap-4 lg:grid-cols-2">
      <SignalList
        title={positiveTitle}
        values={positive}
        type="positive"
      />

      <SignalList
        title={negativeTitle}
        values={negative}
        type="negative"
      />
    </div>
  );
}


function SignalList({
  title,
  values,
  type,
}: {
  title: string;
  values: string[];
  type:
    | "positive"
    | "negative";
}) {
  if (
    values.length === 0
  ) {
    return null;
  }

  const Icon =
    type === "positive"
      ? CircleCheck
      : CircleAlert;

  return (
    <div className="rounded-xl border border-[var(--border-soft)] bg-black/10 p-4">
      <SectionTitle>
        {title}
      </SectionTitle>

      <div className="mt-3 space-y-2">
        {values.map(
          (
            value,
            index,
          ) => (
            <div
              key={
                `${value}-${index}`
              }
              className="flex gap-2 text-sm leading-6 text-[var(--muted-light)]"
            >
              <Icon
                className={
                  type === "positive"
                    ? "mt-1 h-4 w-4 shrink-0 text-emerald-400"
                    : "mt-1 h-4 w-4 shrink-0 text-red-400"
                }
              />

              <span>
                {value}
              </span>
            </div>
          ),
        )}
      </div>
    </div>
  );
}


function Conclusion({
  text,
}: {
  text: unknown;
}) {
  if (
    typeof text !== "string"
    || !text
  ) {
    return null;
  }

  return (
    <div className="rounded-xl border border-[var(--border-soft)] bg-white/[0.02] p-4">
      <div className="flex gap-3">
        <Sparkles className="mt-0.5 h-4 w-4 shrink-0 text-emerald-400" />

        <div>
          <SectionTitle>
            Conclusion
          </SectionTitle>

          <p className="mt-2 text-sm leading-6 text-white/80">
            {text}
          </p>
        </div>
      </div>
    </div>
  );
}


function CaseCard({
  type,
  title,
  text,
}: {
  type:
    | "bull"
    | "bear";
  title: string;
  text: unknown;
}) {
  if (
    typeof text !== "string"
    || !text
  ) {
    return null;
  }

  const Icon =
    type === "bull"
      ? ArrowUpRight
      : ArrowDownRight;

  return (
    <div
      className={
        type === "bull"
          ? "rounded-xl border border-emerald-400/20 bg-emerald-400/[0.035] p-4"
          : "rounded-xl border border-red-400/20 bg-red-400/[0.035] p-4"
      }
    >
      <div className="flex items-center gap-2">
        <Icon
          className={
            type === "bull"
              ? "h-4 w-4 text-emerald-400"
              : "h-4 w-4 text-red-400"
          }
        />

        <span className="text-sm font-medium text-white">
          {title}
        </span>
      </div>

      <p className="mt-3 text-sm leading-6 text-[var(--muted-light)]">
        {text}
      </p>
    </div>
  );
}


function Badge({
  value,
}: {
  value: unknown;
}) {
  if (
    typeof value !== "string"
  ) {
    return null;
  }

  return (
    <span className="rounded-md border border-[var(--border-soft)] bg-white/[0.03] px-2 py-1 text-[10px] uppercase tracking-[0.08em] text-[var(--muted-light)]">
      {formatLabel(
        value
      )}
    </span>
  );
}


function toStringArray(
  value: unknown,
): string[] {
  if (
    !Array.isArray(
      value
    )
  ) {
    return [];
  }

  return value.filter(
    (
      item,
    ): item is string =>
      typeof item === "string",
  );
}


function formatLabel(
  value: unknown,
): string {
  if (
    typeof value !== "string"
  ) {
    return "—";
  }

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


function formatPercent(
  value: unknown,
): string {
  if (
    typeof value !== "number"
  ) {
    return "—";
  }

  return `${Math.round(
    value * 100
  )}%`;
}

function getCharts(
  data: Record<string, unknown>,
): Record<string, unknown> {
  const charts =
    data._charts;

  if (
    typeof charts !== "object"
    || charts === null
  ) {
    return {};
  }

  return charts as Record<
    string,
    unknown
  >;
}