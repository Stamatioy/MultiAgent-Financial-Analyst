"use client";

import Link from "next/link";
import {
  Activity,
  Bot,
  Clock3,
  Cpu,
  LayoutDashboard,
  Search,
  Star,
  Workflow,
} from "lucide-react";

import { usePathname } from "next/navigation";


const navigation = [
  {
    label: "Dashboard",
    href: "/",
    icon: LayoutDashboard,
  },
  {
    label: "Research",
    href: "/research",
    icon: Search,
  },
  {
    label: "Watchlist",
    href: "/watchlist",
    icon: Star,
  },
  {
    label: "History",
    href: "/history",
    icon: Clock3,
  },
];


const systemNavigation = [
  {
    label: "Agents",
    href: "/agents",
    icon: Bot,
  },
  {
    label: "Architecture",
    href: "/architecture",
    icon: Workflow,
  },
];


export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside
      className="
        fixed
        inset-y-0
        left-0
        hidden
        w-64
        border-r
        border-[var(--border-soft)]
        bg-[#090d13]
        lg:flex
        lg:flex-col
      "
    >
      <div
        className="
          flex
          h-20
          items-center
          gap-3
          border-b
          border-[var(--border-soft)]
          px-6
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
            border
            border-emerald-400/20
            bg-emerald-400/10
          "
        >
          <Activity
            className="
              h-5
              w-5
              text-emerald-400
            "
          />
        </div>

        <div>
          <div
            className="
              text-sm
              font-semibold
              tracking-wide
              text-white
            "
          >
            FINANCIAL AI
          </div>

          <div
            className="
              text-xs
              text-[var(--muted)]
            "
          >
            Research Terminal
          </div>
        </div>
      </div>

      <div
        className="
          flex-1
          overflow-y-auto
          px-3
          py-6
        "
      >
        <div
          className="
            mb-2
            px-3
            text-[10px]
            font-semibold
            uppercase
            tracking-[0.18em]
            text-[var(--muted)]
          "
        >
          Workspace
        </div>

        <nav className="space-y-1">
          {navigation.map(
            ({
              label,
              href,
              icon: Icon,
            }) => {
              const active =
                href !== "#" &&
                pathname === href;

              return (
                <Link
                  key={label}
                  href={href}
                  className={`
                    flex
                    items-center
                    gap-3
                    rounded-lg
                    px-3
                    py-2.5
                    text-sm
                    transition
                    ${
                      active
                        ? "bg-white/[0.07] text-white"
                        : "text-[var(--muted-light)] hover:bg-white/[0.04] hover:text-white"
                    }
                  `}
                >
                  <Icon className="h-4 w-4" />

                  {label}
                </Link>
              );
            },
          )}
        </nav>

        <div
          className="
            mb-2
            mt-8
            px-3
            text-[10px]
            font-semibold
            uppercase
            tracking-[0.18em]
            text-[var(--muted)]
          "
        >
          AI System
        </div>

        <nav className="space-y-1">
          {systemNavigation.map(
            ({
              label,
              href,
              icon: Icon,
            }) => {
              const active =
                href !== "#" &&
                pathname === href;

              return (
                <Link
                  key={label}
                  href={href}
                  className={`
                    flex
                    items-center
                    gap-3
                    rounded-lg
                    px-3
                    py-2.5
                    text-sm
                    transition
                    ${
                      active
                        ? "bg-white/[0.07] text-white"
                        : "text-[var(--muted-light)] hover:bg-white/[0.04] hover:text-white"
                    }
                  `}
                >
                  <Icon className="h-4 w-4" />

                  {label}
                </Link>
              );
            },
          )}
        </nav>
      </div>

      <div
        className="
          border-t
          border-[var(--border-soft)]
          p-4
        "
      >
        <div
          className="
            rounded-xl
            border
            border-[var(--border)]
            bg-[var(--surface)]
            p-4
          "
        >
          <div
            className="
              flex
              items-center
              gap-3
            "
          >
            <div
              className="
                relative
                flex
                h-8
                w-8
                items-center
                justify-center
                rounded-lg
                bg-white/[0.05]
              "
            >
              <Cpu
                className="
                  h-4
                  w-4
                  text-[var(--muted-light)]
                "
              />

              <span
                className="
                  absolute
                  -right-1
                  -top-1
                  h-2.5
                  w-2.5
                  rounded-full
                  border-2
                  border-[#0e131b]
                  bg-emerald-400
                "
              />
            </div>

            <div>
              <div
                className="
                  text-xs
                  font-medium
                  text-white
                "
              >
                Qwen3-8B
              </div>

              <div
                className="
                  text-[11px]
                  text-[var(--muted)]
                "
              >
                Local inference
              </div>
            </div>
          </div>
        </div>
      </div>
    </aside>
  );
}