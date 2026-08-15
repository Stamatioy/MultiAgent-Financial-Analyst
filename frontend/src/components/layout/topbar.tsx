import {
  CircleHelp,
} from "lucide-react";
import {
  FaGithub,
} from "react-icons/fa";

export function Topbar() {
  return (
    <header
      className="
        sticky
        top-0
        z-30
        flex
        h-20
        items-center
        justify-between
        border-b
        border-[var(--border-soft)]
        bg-[#080b10]/90
        px-6
        backdrop-blur-xl
        lg:px-8
      "
    >
      <div>
        <div
          className="
            text-xs
            uppercase
            tracking-[0.16em]
            text-[var(--muted)]
          "
        >
          Multi-Agent
        </div>

        <div
          className="
            mt-1
            text-sm
            font-medium
            text-white
          "
        >
          Financial Research System
        </div>
      </div>

      <div
        className="
          flex
          items-center
          gap-2
        "
      >
        <button
          className="
            flex
            h-9
            w-9
            items-center
            justify-center
            rounded-lg
            border
            border-[var(--border)]
            text-[var(--muted-light)]
            transition
            hover:bg-white/[0.04]
            hover:text-white
          "
        >
          <CircleHelp className="h-4 w-4" />
        </button>

        <button
          className="
            flex
            h-9
            w-9
            items-center
            justify-center
            rounded-lg
            border
            border-[var(--border)]
            text-[var(--muted-light)]
            transition
            hover:bg-white/[0.04]
            hover:text-white
          "
        >
          <FaGithub className="h-4 w-4" />
        </button>
      </div>
    </header>
  );
}