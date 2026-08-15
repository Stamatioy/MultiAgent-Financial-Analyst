"use client";

import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import {
  PriceHistoryPoint,
} from "@/lib/types";


export function PriceHistoryChart({
  data,
}: {
  data: PriceHistoryPoint[];
}) {
  if (data.length === 0) {
    return null;
  }

  return (
    <ChartShell
      title="Price & Moving Averages"
      description="Adjusted closing price with 50-day and 200-day moving averages."
    >
      <div className="h-80 w-full">
        <ResponsiveContainer
          width="100%"
          height="100%"
        >
          <LineChart
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
              width={60}
              tickFormatter={
                formatPrice
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
              labelStyle={{
                color:
                  "rgba(255,255,255,0.6)",
              }}
              formatter={(
                value,
                name,
              ) => [
                formatPrice(
                  Number(value)
                ),
                formatSeriesName(
                  String(name)
                ),
              ]}
            />

            <Line
              type="monotone"
              dataKey="close"
              name="Price"
              stroke="#ffffff"
              strokeWidth={2}
              dot={false}
              activeDot={{
                r: 4,
              }}
            />

            <Line
              type="monotone"
              dataKey="ma_50"
              name="MA 50"
              stroke="#34d399"
              strokeWidth={1.5}
              dot={false}
            />

            <Line
              type="monotone"
              dataKey="ma_200"
              name="MA 200"
              stroke="#f59e0b"
              strokeWidth={1.5}
              dot={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </ChartShell>
  );
}


function ChartShell({
  title,
  description,
  children,
}: {
  title: string;
  description: string;
  children: React.ReactNode;
}) {
  return (
    <div className="rounded-xl border border-[var(--border-soft)] bg-black/10 p-5">
      <div>
        <h4 className="text-sm font-medium text-white">
          {title}
        </h4>

        <p className="mt-1 text-xs text-[var(--muted)]">
          {description}
        </p>
      </div>

      <div className="mt-5">
        {children}
      </div>
    </div>
  );
}


function formatPrice(
  value: number,
) {
  return `$${value.toFixed(
    0
  )}`;
}


function formatSeriesName(
  value: string,
) {
  return value;
}