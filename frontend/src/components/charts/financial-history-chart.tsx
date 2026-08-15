"use client";

import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import {
  FinancialHistoryPoint,
} from "@/lib/types";


export function FinancialHistoryChart({
  data,
}: {
  data: FinancialHistoryPoint[];
}) {
  if (data.length === 0) {
    return null;
  }

  return (
    <div className="rounded-xl border border-[var(--border-soft)] bg-black/10 p-5">
      <h4 className="text-sm font-medium text-white">
        Financial Performance
      </h4>

      <p className="mt-1 text-xs text-[var(--muted)]">
        Annual revenue, net income and free cash flow.
      </p>

      <div className="mt-5 h-80 w-full">
        <ResponsiveContainer
          width="100%"
          height="100%"
        >
          <BarChart
            data={data}
          >
            <CartesianGrid
              stroke="rgba(255,255,255,0.06)"
              vertical={false}
            />

            <XAxis
              dataKey="fiscal_year"
              tick={{
                fill:
                  "rgba(255,255,255,0.45)",
                fontSize: 11,
              }}
              tickLine={false}
              axisLine={false}
            />

            <YAxis
              tick={{
                fill:
                  "rgba(255,255,255,0.45)",
                fontSize: 11,
              }}
              tickLine={false}
              axisLine={false}
              width={70}
              tickFormatter={
                formatMoney
              }
            />

            <Tooltip
              contentStyle={{
                background:
                  "#0d1117",
                border:
                  "1px solid rgba(255,255,255,0.1)",
                borderRadius:
                  "10px",
              }}
              formatter={(
                value,
                name,
              ) => [
                formatMoney(
                  Number(value)
                ),
                String(name),
              ]}
            />

            <Legend />

            <Bar
              dataKey="revenue"
              name="Revenue"
              fill="#60a5fa"
              radius={[
                3,
                3,
                0,
                0,
              ]}
            />

            <Bar
              dataKey="net_income"
              name="Net Income"
              fill="#34d399"
              radius={[
                3,
                3,
                0,
                0,
              ]}
            />

            <Bar
              dataKey="free_cash_flow"
              name="Free Cash Flow"
              fill="#f59e0b"
              radius={[
                3,
                3,
                0,
                0,
              ]}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}


function formatMoney(
  value: number,
) {
  const absolute =
    Math.abs(value);

  if (
    absolute >= 1_000_000_000
  ) {
    return `$${(
      value
      / 1_000_000_000
    ).toFixed(1)}B`;
  }

  if (
    absolute >= 1_000_000
  ) {
    return `$${(
      value
      / 1_000_000
    ).toFixed(1)}M`;
  }

  return `$${value.toFixed(
    0
  )}`;
}