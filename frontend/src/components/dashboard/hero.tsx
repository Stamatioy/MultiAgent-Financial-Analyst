import {
  Database,
  Network,
  ShieldCheck,
} from "lucide-react";


export function Hero() {
  return (
    <section
      className="
        relative
        overflow-hidden
        rounded-2xl
        border
        border-[var(--border)]
        bg-[var(--surface)]
        px-7
        py-9
        lg:px-10
        lg:py-11
      "
    >
      <div
        className="
          pointer-events-none
          absolute
          right-0
          top-0
          h-72
          w-72
          translate-x-1/3
          -translate-y-1/3
          rounded-full
          bg-emerald-400/[0.04]
          blur-3xl
        "
      />

      <div
        className="
          relative
          max-w-3xl
        "
      >
        <div
          className="
            mb-5
            inline-flex
            items-center
            gap-2
            rounded-full
            border
            border-emerald-400/20
            bg-emerald-400/[0.06]
            px-3
            py-1.5
            text-xs
            font-medium
            text-emerald-300
          "
        >
          <span
            className="
              h-1.5
              w-1.5
              rounded-full
              bg-emerald-400
            "
          />

          Local AI Research Engine
        </div>

        <h1
          className="
            max-w-3xl
            text-3xl
            font-semibold
            leading-tight
            tracking-[-0.035em]
            text-white
            md:text-4xl
            lg:text-5xl
          "
        >
          Institutional-style research,
          powered by specialist AI agents.
        </h1>

        <p
          className="
            mt-5
            max-w-2xl
            text-sm
            leading-7
            text-[var(--muted-light)]
            md:text-base
          "
        >
          Analyze market behavior, fundamentals,
          valuation, risk and relevant news before
          an Investment Committee synthesizes the
          evidence into a final research view.
        </p>

        <div
          className="
            mt-8
            flex
            flex-wrap
            gap-x-7
            gap-y-3
          "
        >
          <Feature
            icon={Network}
            text="Multi-agent"
          />

          <Feature
            icon={Database}
            text="Evidence grounded"
          />

          <Feature
            icon={ShieldCheck}
            text="Local inference"
          />
        </div>
      </div>
    </section>
  );
}


function Feature({
  icon: Icon,
  text,
}: {
  icon: React.ElementType;
  text: string;
}) {
  return (
    <div
      className="
        flex
        items-center
        gap-2
        text-xs
        text-[var(--muted)]
      "
    >
      <Icon
        className="
          h-4
          w-4
          text-emerald-400
        "
      />

      {text}
    </div>
  );
}