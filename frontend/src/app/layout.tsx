import type { Metadata } from "next";
import { Providers } from './providers';
import { Layout } from '@/components/Layout';
import "./globals.css";

export const metadata: Metadata = {
  title: "アカシックAI占い",
  description: "AIが導く、あなたの運命の道",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ja">
      <body>
        <Providers>
          <Layout>{children}</Layout>
        </Providers>
      </body>
    </html>
  );
}
