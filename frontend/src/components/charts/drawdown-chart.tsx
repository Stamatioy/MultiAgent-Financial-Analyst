"use client";

import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import {
  DrawdownPoint,
} from "@/lib/types";


export function DrawdownChart({
  data,
}: {
  data: DrawdownPoint[];
}) {
  if (data.length === 0) {
    return null;
  }

  return (
    <div className="rounded-xl border border-[var(--border-soft)] bg-black/10 p-5">
      <h4 className="text-sm font-medium text-white">
        Historical Drawdown
      </h4>

      <p className="mt-1 text-xs text-[var(--muted)]">
        Percentage decline from the previous historical peak.
      </p>

      <div className="mt-5 h-72 w-full">
        <ResponsiveContainer
          width="100%"
          height="100%"
        >
          <AreaChart
            data={data}
          >
            <CartesianGrid
              stroke="rgba(255,255,255,0.06)"
              vertical={false}
            />

            <XAxis
              dataKey="date"
              tick={{
                fill:
                  "rgba(255,255,255,0.45)",
                fontSize: 11,
              }}
              tickLine={false}
              axisLine={false}
              minTickGap={50}
            />

            <YAxis
              tick={{
                fill:
                  "rgba(255,255,255,0.45)",
                fontSize: 11,
              }}
              tickLine={false}
              axisLine={false}
              tickFormatter={
                formatPercent
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
              ) => [
                formatPercent(
                  Number(value)
                ),
                "Drawdown",
              ]}
            />

            <Area
              type="monotone"
              dataKey="drawdown"
              stroke="#f87171"
              fill="#f87171"
              fillOpacity={0.12}
              strokeWidth={1.5}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}


function formatPercent(
  value: number,
) {
  return `${(
    value * 100
  ).toFixed(0)}%`;
}