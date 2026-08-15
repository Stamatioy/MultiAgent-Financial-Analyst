import {
  Search,
} from "lucide-react";

import {
  ResearchForm,
} from "@/components/dashboard/research-form";


export default function ResearchPage() {
  return (
    <div
      className="
        mx-auto
        max-w-4xl
      "
    >
      <div
        className="
          mb-7
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
          <Search
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
            Company Research
          </h1>

          <p
            className="
              mt-1
              text-sm
              text-[var(--muted)]
            "
          >
            Run the complete financial
            research pipeline.
          </p>
        </div>
      </div>

      <ResearchForm />
    </div>
  );
}