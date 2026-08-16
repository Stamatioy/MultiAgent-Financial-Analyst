import {
  BrainCircuit,
  Building2,
  ChartNoAxesCombined,
  Newspaper,
  Scale,
  ShieldAlert,
  Sparkles,
} from "lucide-react";


const agents = [
  {
    name: "Market Analyst",
    icon: ChartNoAxesCombined,
    role: "Price Action & Momentum",
    description:
      "Interprets historical price behavior, momentum, trend positioning and volatility.",
    inputs: [
      "Historical prices",
      "Returns",
      "Moving averages",
      "Volatility",
      "Maximum drawdown",
    ],
    outputs: [
      "Momentum assessment",
      "Short-term view",
      "Long-term price view",
      "Positive signals",
      "Negative signals",
    ],
  },

  {
    name: "Fundamental Analyst",
    icon: Building2,
    role: "Business Quality",
    description:
      "Evaluates company growth, profitability, cash generation and balance-sheet strength.",
    inputs: [
      "Revenue",
      "Net income",
      "Operating income",
      "Free cash flow",
      "Assets and liabilities",
    ],
    outputs: [
      "Growth assessment",
      "Profitability assessment",
      "Cash-flow quality",
      "Strengths",
      "Weaknesses",
    ],
  },

  {
    name: "Valuation Analyst",
    icon: Scale,
    role: "Price vs. Fundamentals",
    description:
      "Evaluates whether the market price implies demanding, balanced or attractive expectations.",
    inputs: [
      "Share price",
      "Market capitalization",
      "Enterprise value",
      "Earnings",
      "Free cash flow",
    ],
    outputs: [
      "Overall valuation",
      "Valuation risk",
      "Valuation supports",
      "Valuation concerns",
    ],
  },

  {
    name: "Risk Analyst",
    icon: ShieldAlert,
    role: "Downside & Market Risk",
    description:
      "Measures volatility, benchmark sensitivity, tail risk, historical drawdowns and financial risk.",
    inputs: [
      "Price history",
      "Benchmark prices",
      "Volatility",
      "VaR / CVaR",
      "Debt and cash",
    ],
    outputs: [
      "Overall risk",
      "Market risk",
      "Downside risk",
      "Risk factors",
      "Risk mitigants",
    ],
  },

  {
    name: "News Analyst",
    icon: Newspaper,
    role: "News Intelligence & RAG",
    description:
      "Transforms retrieved current and historical articles into material company events.",
    inputs: [
      "Retrieved articles",
      "Semantic relevance",
      "Publication dates",
      "Article summaries",
    ],
    outputs: [
      "Material events",
      "Sentiment",
      "Positive developments",
      "Negative developments",
      "Supporting sources",
    ],
  },

  {
    name: "Investment Committee",
    icon: BrainCircuit,
    role: "Final Synthesis",
    description:
      "Reviews every specialist output and produces the final risk-adjusted investment assessment.",
    inputs: [
      "Market analysis",
      "Fundamental analysis",
      "Valuation analysis",
      "Risk analysis",
      "News intelligence",
    ],
    outputs: [
      "Recommendation",
      "Confidence",
      "Bull case",
      "Bear case",
      "Key catalysts",
      "Key risks",
    ],
  },
];


export default function AgentsPage() {
  return (
    <div className="mx-auto max-w-6xl">
      <div>
        <div className="flex items-center gap-2 text-xs uppercase tracking-[0.16em] text-emerald-400">
          <Sparkles className="h-4 w-4" />

          AI Research Team
        </div>

        <h1 className="mt-3 text-3xl font-semibold tracking-tight text-white">
          Specialist Agents
        </h1>

        <p className="mt-3 max-w-3xl text-sm leading-7 text-[var(--muted-light)]">
          Each agent receives a focused subset of validated evidence and
          produces a structured specialist assessment. The Investment
          Committee combines these views instead of relying on a single
          general-purpose prompt.
        </p>
      </div>


      <div className="mt-9 flex flex-col gap-4">
        {agents.map(
          (agent, index) => (
            <AgentCard
              key={agent.name}
              agent={agent}
              index={index + 1}
            />
          ),
        )}
      </div>


      <div className="mt-8 rounded-2xl border border-emerald-400/20 bg-emerald-400/[0.03] p-6">
        <div className="flex gap-4">
          <BrainCircuit className="mt-0.5 h-5 w-5 shrink-0 text-emerald-400" />

          <div>
            <div className="text-sm font-semibold text-white">
              One local model, multiple specialist roles
            </div>

            <p className="mt-2 max-w-4xl text-sm leading-6 text-[var(--muted-light)]">
              All agents use the same locally hosted Qwen3-8B model through
              llama.cpp. Their behavior differs through specialist prompts,
              input context and validated output schemas rather than separate
              model deployments.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}


function AgentCard({
  agent,
  index,
}: {
  agent: typeof agents[number];
  index: number;
}) {
  const Icon =
    agent.icon;

  return (
    <div className="rounded-2xl border border-[var(--border)] bg-white/[0.015] p-6">
      <div className="flex flex-wrap items-start justify-between gap-5">
        <div className="flex gap-4">
          <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-emerald-400/[0.06] text-emerald-400">
            <Icon className="h-5 w-5" />
          </div>

          <div>
            <div className="text-[10px] uppercase tracking-[0.14em] text-[var(--muted)]">
              Agent {String(index).padStart(2, "0")}
            </div>

            <h2 className="mt-1 text-lg font-semibold text-white">
              {agent.name}
            </h2>

            <div className="mt-1 text-xs text-emerald-400">
              {agent.role}
            </div>
          </div>
        </div>
      </div>


      <p className="mt-5 max-w-4xl text-sm leading-6 text-[var(--muted-light)]">
        {agent.description}
      </p>


      <div className="mt-6 grid gap-4 lg:grid-cols-2">
        <AgentList
          title="Inputs"
          values={agent.inputs}
        />

        <AgentList
          title="Outputs"
          values={agent.outputs}
        />
      </div>
    </div>
  );
}


function AgentList({
  title,
  values,
}: {
  title: string;
  values: string[];
}) {
  return (
    <div className="rounded-xl border border-[var(--border-soft)] bg-black/10 p-4">
      <div className="text-[10px] uppercase tracking-[0.14em] text-[var(--muted)]">
        {title}
      </div>

      <div className="mt-3 flex flex-wrap gap-2">
        {values.map(
          (value) => (
            <span
              key={value}
              className="rounded-md border border-[var(--border-soft)] bg-white/[0.02] px-2.5 py-1.5 text-xs text-[var(--muted-light)]"
            >
              {value}
            </span>
          ),
        )}
      </div>
    </div>
  );
}