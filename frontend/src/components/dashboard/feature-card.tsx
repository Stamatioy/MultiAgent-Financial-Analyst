import {
  LucideIcon,
} from "lucide-react";


interface FeatureCardProps {
  title: string;
  description: string;
  icon: LucideIcon;
}


export function FeatureCard({
  title,
  description,
  icon: Icon,
}: FeatureCardProps) {
  return (
    <div
      className="
        rounded-2xl
        border
        border-[var(--border)]
        bg-[var(--surface)]
        p-5
        transition
        hover:border-[#2a3748]
        hover:bg-[var(--surface-raised)]
      "
    >
      <div
        className="
          flex
          h-9
          w-9
          items-center
          justify-center
          rounded-lg
          bg-white/[0.04]
        "
      >
        <Icon
          className="
            h-4
            w-4
            text-emerald-400
          "
        />
      </div>

      <h3
        className="
          mt-5
          text-sm
          font-medium
          text-white
        "
      >
        {title}
      </h3>

      <p
        className="
          mt-2
          text-xs
          leading-6
          text-[var(--muted)]
        "
      >
        {description}
      </p>
    </div>
  );
}