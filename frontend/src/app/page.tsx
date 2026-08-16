import {
  BrainCircuit,
  ChartNoAxesCombined,
  Database,
  Newspaper,
  ShieldAlert,
  Scale,
} from "lucide-react";

import {
  FeatureCard,
} from "@/components/dashboard/feature-card";

import {
  Hero,
} from "@/components/dashboard/hero";

import {
  ResearchForm,
} from "@/components/dashboard/research-form";

import {
  SystemStatus,
} from "@/components/dashboard/system-status";


const agents = [
  {
    title: "Market Intelligence",
    description:
      "Analyzes momentum, historical returns, moving averages and volatility.",

    icon:
      ChartNoAxesCombined,
  },

  {
    title: "Fundamental Research",
    description:
      "Evaluates SEC financial statements, growth, profitability and cash generation.",

    icon:
      Database,
  },

  {
    title: "Valuation Analysis",
    description:
      "Evaluates whether the market price implies demanding, balanced or attractive expectations.",

    icon:
      Scale,
  },

  {
    title: "News Intelligence",
    description:
      "Uses semantic retrieval to identify relevant developments and material events.",

    icon:
      Newspaper,
  },

  {
    title: "Risk Analysis",
    description:
      "Measures market sensitivity, tail risk, drawdowns and balance-sheet risk.",

    icon:
      ShieldAlert,
  },

  {
    title: "Investment Committee",
    description:
      "Synthesizes specialist research into an evidence-grounded final assessment.",

    icon:
      BrainCircuit,
  },
];


export default function Home() {
  return (
    <div className="space-y-7">
      <Hero />

      <div
        className="
          grid
          gap-7
          xl:grid-cols-[minmax(0,1fr)_360px]
        "
      >
        <ResearchForm />

        <SystemStatus />
      </div>

      <section>
        <div
          className="
            mb-4
            flex
            items-end
            justify-between
          "
        >
          <div>
            <h2
              className="
                text-sm
                font-semibold
                text-white
              "
            >
              Research System
            </h2>

            <p
              className="
                mt-1
                text-xs
                text-[var(--muted)]
              "
            >
              Specialist agents working
              from validated data.
            </p>
          </div>
        </div>

        <div
          className="
            grid
            gap-4
            md:grid-cols-2
            xl:grid-cols-6
          "
        >
          {agents.map(
            (agent) => (
              <FeatureCard
                key={agent.title}
                {...agent}
              />
            ),
          )}
        </div>
      </section>
    </div>
  );
}