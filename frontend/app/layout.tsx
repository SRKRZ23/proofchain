import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "PROOFCHAIN — Cryptographic audit trail for AI agents on the live web",
  description:
    "Drop-in MCP provenance layer. Every web fetch returns content + Ed25519-signed evidence packet. EU AI Act Article 12 compliant.",
  metadataBase: new URL("https://proofchain.dev"),
  openGraph: {
    title: "PROOFCHAIN",
    description: "Anthropic owns MCP. We own the audit trail.",
    type: "website",
    url: "https://proofchain.dev",
  },
  twitter: {
    card: "summary_large_image",
    title: "PROOFCHAIN",
    description: "Cryptographic audit trail for AI agents on the live web",
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          rel="stylesheet"
          href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap"
        />
      </head>
      <body>{children}</body>
    </html>
  );
}
