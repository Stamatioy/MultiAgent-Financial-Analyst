import type {
  Metadata,
} from "next";

import "./globals.css";

import { AppShell } from "@/components/layout/app-shell";


export const metadata: Metadata = {
  title: "Financial AI",
  description: (
    "Local multi-agent financial research terminal"
  ),
};


export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <AppShell>
          {children}
        </AppShell>
      </body>
    </html>
  );
}
