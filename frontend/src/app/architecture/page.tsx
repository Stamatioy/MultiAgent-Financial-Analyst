import {
  BrainCircuit,
  Database,
  FileSearch,
  Newspaper,
  Network,
  ShieldCheck,
  Sigma,
} from "lucide-react";


export default function ArchitecturePage() {
  return (
    <div className="mx-auto max-w-6xl">
      <div>
        <div className="flex items-center gap-2 text-xs uppercase tracking-[0.16em] text-emerald-400">
          <Network className="h-4 w-4" />

          System Architecture
        </div>

        <h1 className="mt-3 text-3xl font-semibold tracking-tight text-white">
          How the Financial Analyst Works
        </h1>

        <p className="mt-3 max-w-3xl text-sm leading-7 text-[var(--muted-light)]">
          A local multi-agent financial research system that combines
          deterministic financial analytics, retrieval-augmented news
          intelligence and structured LLM analysis before producing a final
          Investment Committee assessment.
        </p>
      </div>


      <div className="mt-10 rounded-2xl border border-[var(--border)] bg-white/[0.015] p-6 lg:p-8">
        <SectionTitle>
          Research Pipeline
        </SectionTitle>

        <div className="mt-7 flex flex-col items-center">
          <ArchitectureNode
            icon={FileSearch}
            title="Research Request"
            description="Ticker, fiscal year, market horizon and news query"
          />

          <Connector />

          <ArchitectureNode
            icon={Network}
            title="Research Coordinator"
            description="Orchestrates deterministic services and specialist agents"
            highlighted
          />

          <Connector />

          <div className="grid w-full gap-4 md:grid-cols-2 xl:grid-cols-5">
            <SmallNode
              title="Market"
              subtitle="Price & trend"
            />

            <SmallNode
              title="Fundamentals"
              subtitle="SEC financials"
            />

            <SmallNode
              title="Valuation"
              subtitle="Multiples & yields"
            />

            <SmallNode
              title="Risk"
              subtitle="Volatility & downside"
            />

            <SmallNode
              title="News"
              subtitle="RAG intelligence"
            />
          </div>

          <Connector />

          <ArchitectureNode
            icon={BrainCircuit}
            title="Investment Committee"
            description="Synthesizes all specialist evidence into one final assessment"
            highlighted
          />

          <Connector />

          <ArchitectureNode
            icon={ShieldCheck}
            title="Investment Report"
            description="Recommendation, confidence, thesis, bull case, bear case and evidence"
          />
        </div>
      </div>


      <div className="mt-6 grid gap-5 lg:grid-cols-2">
        <ArchitectureCard
          icon={Sigma}
          title="Deterministic Analytics"
          description="Financial metrics are calculated in Python before the LLM sees them. The model interprets validated values rather than inventing calculations."
          items={[
            "Market returns and moving averages",
            "Fundamental ratios and growth",
            "Valuation multiples",
            "Risk and drawdown metrics",
          ]}
        />

        <ArchitectureCard
          icon={Newspaper}
          title="News + RAG"
          description="Relevant current and historical news is retrieved, ranked and converted into structured material events."
          items={[
            "Semantic retrieval",
            "Event deduplication",
            "Sentiment and materiality",
            "Traceable supporting articles",
          ]}
        />

        <ArchitectureCard
          icon={BrainCircuit}
          title="Local LLM"
          description="Qwen3-8B runs locally through llama.cpp and performs all specialist and committee reasoning."
          items={[
            "No cloud LLM API",
            "Structured JSON outputs",
            "Pydantic validation",
            "Local inference",
          ]}
        />

        <ArchitectureCard
          icon={Database}
          title="Persistence"
          description="DuckDB stores financial data, market prices, research history and the user watchlist."
          items={[
            "Cached market data",
            "SEC financial facts",
            "Research history",
            "Watchlist",
          ]}
        />
      </div>


      <div className="mt-6 rounded-2xl border border-[var(--border)] bg-white/[0.015] p-6">
        <SectionTitle>
          Evidence Flow
        </SectionTitle>

        <div className="mt-5 grid gap-4 md:grid-cols-3">
          <EvidenceStage
            number="01"
            title="Raw Data"
            text="Market prices, SEC fundamentals and retrieved news."
          />

          <EvidenceStage
            number="02"
            title="Validated Analysis"
            text="Python calculations and structured specialist outputs."
          />

          <EvidenceStage
            number="03"
            title="Committee Decision"
            text="Evidence-grounded synthesis with explicit risks and catalysts."
          />
        </div>
      </div>
    </div>
  );
}


function ArchitectureNode({
  icon: Icon,
  title,
  description,
  highlighted = false,
}: {
  icon: typeof Network;
  title: string;
  description: string;
  highlighted?: boolean;
}) {
  return (
    <div
      className={
        highlighted
          ? "w-full max-w-xl rounded-xl border border-emerald-400/30 bg-emerald-400/[0.05] p-5 text-center"
          : "w-full max-w-xl rounded-xl border border-[var(--border)] bg-black/10 p-5 text-center"
      }
    >
      <Icon
        className={
          highlighted
            ? "mx-auto h-5 w-5 text-emerald-400"
            : "mx-auto h-5 w-5 text-[var(--muted-light)]"
        }
      />

      <div className="mt-3 text-sm font-semibold text-white">
        {title}
      </div>

      <div className="mt-1 text-xs leading-5 text-[var(--muted)]">
        {description}
      </div>
    </div>
  );
}


function SmallNode({
  title,
  subtitle,
}: {
  title: string;
  subtitle: string;
}) {
  return (
    <div className="rounded-xl border border-[var(--border)] bg-black/10 p-4 text-center">
      <div className="text-sm font-medium text-white">
        {title}
      </div>

      <div className="mt-1 text-[11px] text-[var(--muted)]">
        {subtitle}
      </div>
    </div>
  );
}


function Connector() {
  return (
    <div className="h-8 w-px bg-gradient-to-b from-emerald-400/60 to-[var(--border)]" />
  );
}


function ArchitectureCard({
  icon: Icon,
  title,
  description,
  items,
}: {
  icon: typeof Database;
  title: string;
  description: string;
  items: string[];
}) {
  return (
    <div className="rounded-2xl border border-[var(--border)] bg-white/[0.015] p-6">
      <div className="flex items-center gap-3">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-400/[0.06] text-emerald-400">
          <Icon className="h-5 w-5" />
        </div>

        <div className="text-sm font-semibold text-white">
          {title}
        </div>
      </div>

      <p className="mt-4 text-sm leading-6 text-[var(--muted-light)]">
        {description}
      </p>

      <div className="mt-5 space-y-2">
        {items.map(
          (item) => (
            <div
              key={item}
              className="flex items-center gap-2 text-xs text-[var(--muted-light)]"
            >
              <div className="h-1.5 w-1.5 rounded-full bg-emerald-400" />

              {item}
            </div>
          ),
        )}
      </div>
    </div>
  );
}


function EvidenceStage({
  number,
  title,
  text,
}: {
  number: string;
  title: string;
  text: string;
}) {
  return (
    <div className="rounded-xl border border-[var(--border-soft)] bg-black/10 p-5">
      <div className="text-xs font-semibold text-emerald-400">
        {number}
      </div>

      <div className="mt-3 text-sm font-medium text-white">
        {title}
      </div>

      <p className="mt-2 text-xs leading-5 text-[var(--muted)]">
        {text}
      </p>
    </div>
  );
}


function SectionTitle({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <h2 className="text-xs font-medium uppercase tracking-[0.16em] text-[var(--muted)]">
      {children}
    </h2>
  );
}