import {
  ArrowDown,
  BrainCircuit,
  ChartNoAxesCombined,
  Database,
  Newspaper,
  ShieldAlert,
  Workflow,
} from "lucide-react";


const specialists = [
  {
    label: "Market",
    icon: ChartNoAxesCombined,
  },
  {
    label: "Fundamentals",
    icon: Database,
  },
  {
    label: "News + RAG",
    icon: Newspaper,
  },
  {
    label: "Risk",
    icon: ShieldAlert,
  },
];


export default function ArchitecturePage() {
  return (
    <div
      className="
        mx-auto
        max-w-5xl
      "
    >
      <div
        className="
          flex
          items-center
          gap-4
        "
      >
        <div
          className="
            flex
            h-11
            w-11
            items-center
            justify-center
            rounded-xl
            border
            border-[var(--border)]
            bg-[var(--surface)]
          "
        >
          <Workflow
            className="
              h-5
              w-5
              text-emerald-400
            "
          />
        </div>

        <div>
          <h1
            className="
              text-xl
              font-semibold
              text-white
            "
          >
            System Architecture
          </h1>

          <p
            className="
              mt-1
              text-sm
              text-[var(--muted)]
            "
          >
            How specialist research becomes
            an investment assessment.
          </p>
        </div>
      </div>

      <div
        className="
          mt-8
          rounded-2xl
          border
          border-[var(--border)]
          bg-[var(--surface)]
          p-8
        "
      >
        <ArchitectureBox
          title="Research Coordinator"
          subtitle="Deterministic orchestration"
          icon={Workflow}
        />

        <Arrow />

        <div
          className="
            grid
            gap-3
            sm:grid-cols-2
            lg:grid-cols-4
          "
        >
          {specialists.map(
            ({
              label,
              icon,
            }) => (
              <ArchitectureBox
                key={label}
                title={label}
                subtitle="Specialist agent"
                icon={icon}
              />
            ),
          )}
        </div>

        <Arrow />

        <ArchitectureBox
          title="Investment Committee"
          subtitle="Evidence-grounded synthesis"
          icon={BrainCircuit}
          emphasized
        />
      </div>
    </div>
  );
}


function Arrow() {
  return (
    <div
      className="
        flex
        justify-center
        py-5
      "
    >
      <ArrowDown
        className="
          h-5
          w-5
          text-[var(--muted)]
        "
      />
    </div>
  );
}


function ArchitectureBox({
  title,
  subtitle,
  icon: Icon,
  emphasized = false,
}: {
  title: string;
  subtitle: string;
  icon: React.ElementType;
  emphasized?: boolean;
}) {
  return (
    <div
      className={`
        rounded-xl
        border
        p-5
        text-center
        ${
          emphasized
            ? "border-emerald-400/25 bg-emerald-400/[0.05]"
            : "border-[var(--border)] bg-[#0a0f16]"
        }
      `}
    >
      <Icon
        className={`
          mx-auto
          h-5
          w-5
          ${
            emphasized
              ? "text-emerald-400"
              : "text-[var(--muted-light)]"
          }
        `}
      />

      <div
        className="
          mt-3
          text-sm
          font-medium
          text-white
        "
      >
        {title}
      </div>

      <div
        className="
          mt-1
          text-[11px]
          text-[var(--muted)]
        "
      >
        {subtitle}
      </div>
    </div>
  );
}