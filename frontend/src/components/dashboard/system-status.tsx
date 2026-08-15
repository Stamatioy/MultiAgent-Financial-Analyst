import {
  Bot,
  CircleCheck,
  Database,
  Server,
} from "lucide-react";


const services = [
  {
    label: "FastAPI",
    detail: "Backend API",
    icon: Server,
  },
  {
    label: "Qwen3-8B",
    detail: "Local LLM",
    icon: Bot,
  },
  {
    label: "DuckDB",
    detail: "Research store",
    icon: Database,
  },
];


export function SystemStatus() {
  return (
    <section
      className="
        rounded-2xl
        border
        border-[var(--border)]
        bg-[var(--surface)]
        p-6
      "
    >
      <div
        className="
          flex
          items-center
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
            System
          </h2>

          <p
            className="
              mt-1
              text-xs
              text-[var(--muted)]
            "
          >
            Local research stack
          </p>
        </div>

        <div
          className="
            flex
            items-center
            gap-2
            text-xs
            text-emerald-400
          "
        >
          <CircleCheck className="h-4 w-4" />

          Ready
        </div>
      </div>

      <div
        className="
          mt-6
          space-y-3
        "
      >
        {services.map(
          ({
            label,
            detail,
            icon: Icon,
          }) => (
            <div
              key={label}
              className="
                flex
                items-center
                justify-between
                rounded-xl
                border
                border-[var(--border-soft)]
                bg-white/[0.015]
                px-4
                py-3
              "
            >
              <div
                className="
                  flex
                  items-center
                  gap-3
                "
              >
                <Icon
                  className="
                    h-4
                    w-4
                    text-[var(--muted)]
                  "
                />

                <div>
                  <div
                    className="
                      text-xs
                      font-medium
                      text-white
                    "
                  >
                    {label}
                  </div>

                  <div
                    className="
                      text-[11px]
                      text-[var(--muted)]
                    "
                  >
                    {detail}
                  </div>
                </div>
              </div>

              <span
                className="
                  h-2
                  w-2
                  rounded-full
                  bg-emerald-400
                "
              />
            </div>
          ),
        )}
      </div>
    </section>
  );
}