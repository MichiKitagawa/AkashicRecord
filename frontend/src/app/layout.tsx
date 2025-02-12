import type { Metadata } from "next";
import { Providers } from './providers';
import { Layout } from '@/components/Layout';
import "./globals.css";
import Navigation from '@/components/Navigation';
import { ErrorBoundary } from '@/components/error/ErrorBoundary';
import { Analytics } from '@vercel/analytics/react';
import { SpeedInsights } from '@vercel/speed-insights/next';

export const metadata: Metadata = {
  title: {
    default: "アカシックAI占い",
    template: "%s | アカシックAI占い"
  },
  description: "AIが導く、あなたの運命の道。アカシックレコードの叡智をAIが読み解き、あなたの人生の道しるべを提供します。",
  keywords: ["AI占い", "アカシックレコード", "運勢診断", "無料占い", "オンライン占い"],
  authors: [{ name: "アカシックAI占い" }],
  openGraph: {
    title: "アカシックAI占い",
    description: "AIが導く、あなたの運命の道",
    url: "https://your-domain.com",
    siteName: "アカシックAI占い",
    images: [
      {
        url: "/og-image.jpg",
        width: 1200,
        height: 630,
        alt: "アカシックAI占い",
      },
    ],
    locale: "ja_JP",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "アカシックAI占い",
    description: "AIが導く、あなたの運命の道",
    images: ["/og-image.jpg"],
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ja">
      <body>
        <ErrorBoundary>
          <Navigation />
          <Providers>
            <Layout>{children}</Layout>
          </Providers>
        </ErrorBoundary>
        <Analytics />
        <SpeedInsights />
      </body>
    </html>
  );
}
