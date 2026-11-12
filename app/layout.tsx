import type { Metadata, Viewport } from "next";
import localFont from "next/font/local";
import { site } from "@/lib/site";
import "./globals.css";

const geist = localFont({
  src: "../assets/fonts/Geist-Variable.ttf",
  display: "swap",
  variable: "--font-geist",
  weight: "100 900",
});

export const metadata: Metadata = {
  metadataBase: new URL(site.url),
  title: { default: site.title, template: `%s | ${site.brand}` },
  description: site.description,
  applicationName: site.brand,
  authors: [{ name: site.fullName, url: site.url }],
  creator: site.fullName,
  alternates: { canonical: "/" },
  robots: site.isProd
    ? { index: true, follow: true, googleBot: { index: true, follow: true, "max-image-preview": "large" } }
    : { index: false, follow: false },
  openGraph: {
    type: "website",
    url: "/",
    siteName: site.brand,
    title: site.title,
    description: site.description,
    locale: "en_US",
  },
  twitter: { card: "summary_large_image", title: site.title, description: site.description },
  verification: process.env.NEXT_PUBLIC_GSC_VERIFICATION
    ? { google: process.env.NEXT_PUBLIC_GSC_VERIFICATION }
    : undefined,
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  themeColor: "#ffffff",
  colorScheme: "light",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={geist.variable}>
      <body>{children}</body>
    </html>
  );
}
