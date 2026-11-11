// lib/site.ts
const isProd = process.env.VERCEL_ENV === "production";

export const site = {
  brand: "Alabi",
  fullName: "Ezekiel Alabi",
  jobTitle: "Creative Technologist",
  location: "Lagos, Nigeria",
  // Canonical production URL. Must be the exact host chosen as primary (apex or www), https, no trailing slash.
  url: (process.env.NEXT_PUBLIC_SITE_URL ?? "https://ezekielalabi.com").replace(/\/$/, ""),
  title: "Alabi — Creative Technologist | Coming Soon",
  description:
    "Ezekiel Alabi (Alabi) is a creative technologist. The official portfolio is coming soon.",
  sameAs: [] as string[], // social profile URLs, when provided
  // Only the real production deployment is indexable.
  isProd,
} as const;
