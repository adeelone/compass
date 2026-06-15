import type { Metadata } from "next";
import "../styles/globals.css";

export const metadata: Metadata = {
  title: "Compass",
  description: "AI-augmented job search, resume intelligence, and career OS.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

