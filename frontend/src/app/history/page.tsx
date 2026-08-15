import {
  Clock3,
} from "lucide-react";


export default function HistoryPage() {
  return (
    <div>
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
          <Clock3
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
            Research History
          </h1>

          <p
            className="
              mt-1
              text-sm
              text-[var(--muted)]
            "
          >
            Saved analyses will appear
            here in Milestone 20.
          </p>
        </div>
      </div>

      <div
        className="
          mt-7
          rounded-2xl
          border
          border-dashed
          border-[var(--border)]
          bg-[var(--surface)]
          px-6
          py-16
          text-center
        "
      >
        <div
          className="
            text-sm
            text-[var(--muted-light)]
          "
        >
          No saved research yet.
        </div>
      </div>
    </div>
  );
}