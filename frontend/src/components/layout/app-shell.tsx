import {
  ReactNode,
} from "react";

import { Sidebar } from "./sidebar";
import { Topbar } from "./topbar";


interface AppShellProps {
  children: ReactNode;
}


export function AppShell({
  children,
}: AppShellProps) {
  return (
    <div
      className="
        min-h-screen
        bg-[var(--background)]
        text-[var(--foreground)]
      "
    >
      <Sidebar />

      <div className="lg:pl-64">
        <Topbar />

        <main
          className="
            mx-auto
            w-full
            max-w-[1500px]
            px-6
            py-8
            lg:px-8
            lg:py-10
          "
        >
          {children}
        </main>
      </div>
    </div>
  );
}