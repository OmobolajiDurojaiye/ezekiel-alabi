# TRD — "Coming Soon" Page (Phase 1 of Personal Portfolio Website)

| | |
|---|---|
| **Doc type** | Technical Requirements Document |
| **Companion doc** | `PRD.md` (what & why — read it first; this doc is the how) |
| **Hosting** | Vercel |
| **Top priority** | SEO, then fidelity to the reference, then performance |

> Placeholders such as `[DOMAIN.COM]`, `[FULL_NAME]`, `[PROFESSION_OR_NICHE]` come from the PRD §7. If the real values aren't provided yet, centralize them in `lib/site.ts` so they're changed in exactly one place.

---

## 1. Architecture Decision

**Chosen: Next.js (App Router) + TypeScript + Tailwind CSS v4, fully statically prerendered, deployed on Vercel.**

| Option | Verdict | Reasoning |
|---|---|---|
| **Next.js App Router (static)** | ✅ **Chosen** | Static HTML is generated at build time with all SEO tags in the initial response (no JS needed to render). Built-in Metadata API, `sitemap`/`robots`/`manifest`/OG-image file conventions, `next/font` (self-hosted, zero layout shift) and `next/image` (AVIF/WebP, responsive, priority/preload). First-class on Vercel (CDN edge caching, image optimization, preview deploys). Phase 2 (portfolio pages, project case studies, blog/MDX) grows inside the same project with no rewrite. |
| Astro | Good, but not chosen | Ships even less JS and is excellent for content sites. However, Phase 2 will likely want React components, richer interactions, and tight Vercel integration; picking Next.js now avoids a later migration. |
| Vite/CRA SPA | ❌ Rejected | Client-side rendering is the wrong foundation for an SEO-first site. |
| Plain HTML | ❌ Rejected | Fast, but no growth path, no image/font pipeline. |

**Rendering strategy:** every route is **static (SSG)**. No API routes, no server actions, no middleware, no dynamic APIs (`cookies()`, `headers()`, `searchParams`), so `next build` must list `/` as `○ (Static)`.

**Client JS budget:** effectively zero. Everything on the page is a **Server Component**. No `"use client"` unless truly unavoidable (it isn't, for this page).

### Versions & tooling
- Next.js: latest stable major at build time (pin the exact version in `package.json`; use the current App Router conventions).
- React: the version that ships with that Next.js release.
- Node.js: current LTS (set `engines.node` and the Vercel project Node version to match).
- TypeScript `strict: true`. Tailwind CSS v4 (CSS-first config). ESLint (`next/core-web-vitals`) + Prettier. Package manager: **pnpm** (commit the lockfile).
- No UI libraries, no animation libraries, no icon libraries.

---

## 2. Repository Structure

```
.
├─ app/
│  ├─ layout.tsx            # <html>, fonts, global metadata, viewport
│  ├─ page.tsx              # the coming-soon page (Server Component)
│  ├─ globals.css           # Tailwind import, design tokens, page styles
│  ├─ not-found.tsx         # simple on-brand 404 (noindex)
│  ├─ robots.ts             # env-aware robots
│  ├─ sitemap.ts            # canonical home URL
│  ├─ manifest.ts           # web app manifest
│  ├─ opengraph-image.tsx   # 1200×630 social image (static at build)
│  ├─ twitter-image.tsx     # re-export of the OG image (or same file convention)
│  ├─ icon.png              # 512×512 (auto-served as favicon/icon)
│  ├─ apple-icon.png        # 180×180
│  └─ favicon.ico
├─ assets/                  # source images imported statically (get width/height/blur for free)
│  ├─ alabi-logo.png
│  └─ alabi-portrait.jpg
├─ components/
│  └─ JsonLd.tsx
├─ lib/
│  └─ site.ts               # single source of truth for site config
├─ scripts/
│  └─ process-assets.py     # one-off asset prep (see §6)
├─ .env.example
├─ next.config.ts
├─ package.json
└─ README.md
```

---

## 3. Site Config (`lib/site.ts`)

```ts
// lib/site.ts
const isProd = process.env.VERCEL_ENV === "production";

export const site = {
  brand: "Alabi",
  fullName: "[FULL_NAME]",
  jobTitle: "[PROFESSION_OR_NICHE]",
  location: "[CITY, COUNTRY]",
  // Canonical production URL. Must be the exact host chosen as primary (apex or www), https, no trailing slash.
  url: (process.env.NEXT_PUBLIC_SITE_URL ?? "https://[DOMAIN.COM]").replace(/\/$/, ""),
  title: "Alabi — [Profession] | Coming Soon",
  description:
    "[Full Name] (Alabi) is a [profession] in [location]. The official portfolio is coming soon.",
  sameAs: [] as string[], // social profile URLs, when provided
  // Only the real production deployment is indexable.
  isProd,
} as const;
```

`.env.example`
```
NEXT_PUBLIC_SITE_URL=https://[DOMAIN.COM]
NEXT_PUBLIC_GSC_VERIFICATION=   # optional Google Search Console meta token
```

> `VERCEL_ENV` is `production | preview | development` on Vercel. Locally it's undefined, which safely resolves to non-indexable.

---

## 4. Layout & Metadata (`app/layout.tsx`)

```tsx
import type { Metadata, Viewport } from "next";
import { Inter_Tight } from "next/font/google";
import { site } from "@/lib/site";
import "./globals.css";

const headline = Inter_Tight({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-headline",
  weight: ["500"], // load only what's used
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
    // image comes automatically from app/opengraph-image.tsx
  },
  twitter: { card: "summary_large_image", title: site.title, description: site.description },
  verification: process.env.NEXT_PUBLIC_GSC_VERIFICATION
    ? { google: process.env.NEXT_PUBLIC_GSC_VERIFICATION }
    : undefined,
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  themeColor: "#000000",
  colorScheme: "dark",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={headline.variable}>
      <body>{children}</body>
    </html>
  );
}
```

Notes:
- `title` ≤ 60 chars, `description` ≤ 155 chars (validate in CI or manually).
- OG/Twitter images are auto-wired by the file-based `opengraph-image` / `twitter-image` conventions, with absolute URLs resolved via `metadataBase`.

---

## 5. The Page (`app/page.tsx`)

```tsx
import Image from "next/image";
import logo from "@/assets/alabi-logo.png";
import portrait from "@/assets/alabi-portrait.jpg";
import { JsonLd } from "@/components/JsonLd";
import { site } from "@/lib/site";

export default function Home() {
  return (
    <>
      <JsonLd
        data={{
          "@context": "https://schema.org",
          "@graph": [
            {
              "@type": "WebSite",
              "@id": `${site.url}/#website`,
              url: site.url,
              name: site.brand,
              description: site.description,
              inLanguage: "en",
            },
            {
              "@type": "Person",
              "@id": `${site.url}/#person`,
              name: site.fullName,
              alternateName: site.brand,
              url: site.url,
              image: `${site.url}/opengraph-image`,
              jobTitle: site.jobTitle,
              ...(site.sameAs.length ? { sameAs: site.sameAs } : {}),
            },
          ],
        }}
      />

      <header className="site-header">
        {/* Logo is decorative-branding but also the brand name → alt = brand */}
        <Image src={logo} alt={site.brand} priority className="logo" sizes="160px" />
      </header>

      <main className="hero">
        <div className="glow" aria-hidden="true" />

        <div className="subject">
          <Image
            src={portrait}
            alt={`Portrait of ${site.fullName}, ${site.jobTitle}, in a grey pinstripe suit with a purple tie`}
            fill
            priority
            quality={80}
            sizes="(max-width: 639px) 150vw, 100vh"
            className="subject-img"
          />
        </div>
        <div className="scrim" aria-hidden="true" />

        {/* The one and only h1. Real text. */}
        <h1 className="headline">Coming Soon</h1>

        {/* Honest, non-stuffed context for screen readers and crawlers */}
        <p className="sr-only">{site.description}</p>
      </main>
    </>
  );
}
```

`components/JsonLd.tsx`
```tsx
export function JsonLd({ data }: { data: Record<string, unknown> }) {
  return (
    <script
      type="application/ld+json"
      // escape "<" to prevent breaking out of the script tag
      dangerouslySetInnerHTML={{ __html: JSON.stringify(data).replace(/</g, "\\u003c") }}
    />
  );
}
```

### Styles (`app/globals.css`)

```css
@import "tailwindcss";

@theme {
  --color-black: #000000;
  --color-white: #ffffff;
  --color-pink: #e5a0fd;
  --color-purple: #9900cc;
  --font-headline: var(--font-headline), ui-sans-serif, system-ui, sans-serif;
}

:root {
  --pink: #e5a0fd;
  --purple: #9900cc;
  --gradient: linear-gradient(135deg, var(--pink) 0%, var(--purple) 100%);
  --headline-z: 3; /* Treatment A (default): headline in front of the subject */
}

html, body { height: 100%; background: #000; color: #fff; }
body { margin: 0; overflow: hidden; -webkit-font-smoothing: antialiased; }
::selection { background: var(--purple); color: #fff; }

.sr-only {
  position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px;
  overflow: hidden; clip: rect(0, 0, 0, 0); white-space: nowrap; border: 0;
}

/* ── Header / logo ─────────────────────────────── */
.site-header {
  position: fixed; inset: 0 auto auto 0; z-index: 10;
  padding: clamp(20px, 4vw, 56px);
}
.logo { height: clamp(24px, 2.6vw, 36px); width: auto; display: block; }

/* ── Hero ──────────────────────────────────────── */
.hero {
  position: relative; isolation: isolate; overflow: hidden;
  height: 100dvh; min-height: 100svh; background: #000;
}

/* Brand-color atmosphere behind the subject */
.glow {
  position: absolute; z-index: 0; left: 50%; top: 32%;
  width: min(95vw, 1000px); aspect-ratio: 1;
  transform: translate(-50%, -40%);
  background: radial-gradient(closest-side,
    rgba(229, 160, 253, 0.38) 0%,
    rgba(153, 0, 204, 0.28) 45%,
    transparent 75%);
  filter: blur(70px);
  pointer-events: none;
}

/* Subject: square source, bottom-anchored, full viewport height */
.subject {
  position: absolute; z-index: 1; bottom: 0; left: 50%;
  height: 100dvh; aspect-ratio: 1 / 1; transform: translateX(-50%);
}
.subject-img {
  object-fit: cover; object-position: center bottom;
  /* feather side/top edges so JPEG edges never show against the page */
  -webkit-mask-image: radial-gradient(ellipse 70% 90% at 50% 60%, #000 55%, transparent 100%);
          mask-image: radial-gradient(ellipse 70% 90% at 50% 60%, #000 55%, transparent 100%);
}

/* Legibility scrim for white text over the grey suit */
.scrim {
  position: absolute; z-index: 2; inset: auto 0 0 0; height: 55%;
  background: linear-gradient(to top, rgba(0,0,0,.55), transparent);
  pointer-events: none;
}

/* Headline */
.headline {
  position: absolute; z-index: var(--headline-z); left: 0; right: 0; top: 62%;
  transform: translateY(-50%);
  margin: 0; text-align: center; white-space: nowrap;
  font-family: var(--font-headline);
  font-weight: 500; letter-spacing: -0.045em; line-height: 0.9;
  font-size: clamp(3rem, 12.8vw, 16rem);
  color: #fff;
  animation: rise 700ms cubic-bezier(.2,.7,.2,1) both;
}

@keyframes rise {
  from { opacity: 0; translate: 0 24px; }
  to   { opacity: 1; translate: 0 0; }
}
.glow { animation: breathe 9s ease-in-out infinite alternate; }
@keyframes breathe { from { opacity: .8; } to { opacity: 1; } }

/* ── Mobile ────────────────────────────────────── */
@media (max-width: 639px) {
  .subject { height: auto; width: 150vw; }
  .headline {
    white-space: normal; top: 66%;
    font-size: clamp(3rem, 22vw, 7rem); line-height: 0.88;
    padding-inline: 5vw;
  }
}

@media (prefers-reduced-motion: reduce) {
  .headline, .glow { animation: none; }
}
```

Implementation notes for the agent:
- **Do not animate the portrait's opacity** (it's likely the LCP element; animating it delays LCP). The headline fade/rise and the glow may animate. Keep the headline's animation ≤ 700 ms and with no delay.
- Tune the numbers (headline `top`, `font-size`, glow position, mask) **against the reference screenshot** at 1440×900, then 390×844. The values above are a starting point, not final.
- **Treatment B (optional, flag):** only with a clean transparent cutout of the subject (see §6). Set `--headline-z: 1` (behind), make `.subject` `z-index: 2`, drop/relax the scrim, and remove the radial `mask-image`. If any letter is more than ~20 % covered, revert to A.
- Test the layout under mobile browser chrome collapse (`dvh`), landscape phones, and 4:3 tablets.

---

## 6. Asset Pipeline

Source files are in `/mnt/user-data/uploads` (or the project's provided assets folder). Output goes to `assets/` and the icon locations. Do the prep once with `scripts/process-assets.py` and commit the results (don't process at build time).

### 6.1 Logo (`logo.jpg` → `alabi-logo.png`)
The source is a 1280×1280 black square with the wordmark small and off-center. Required:
1. **Auto-trim** the empty black margin, then add small, even padding (~4–6 % of height).
2. Make the black background **transparent** (alpha from luminance: for a colored mark on pure black, `alpha = max(r,g,b)/255` and un-premultiply the color), or, if the page background is exactly `#000`, an opaque trimmed PNG is visually identical. Prefer transparent.
3. Output PNG (or SVG if the client provides a vector, which is strongly preferred; if SVG, import it via `next/image` with `unoptimized` or inline it).
4. Ensure the output is ≥ 2× the displayed size (displayed height ≈ 36 px → source height ≥ 72 px; use ~160–240 px height for headroom).

### 6.2 Portrait (`photo_…_y.jpg` → `alabi-portrait.jpg`)
- The photo is already on a near-black background, so against the `#000` page it reads as seamless. **JPEG noise can leave the "black" slightly off (#020202–#0a0a0a)**. Crush near-blacks to pure `#000` (levels: input black point ≈ 10–12) so no rectangle is visible. Verify by zooming at the photo's edges on a calibrated/OLED screen and in a screenshot with boosted contrast. The CSS mask in §5 is a second safety net.
- Keep full resolution (1280×1280) as the source; Next will emit responsive AVIF/WebP. Don't pre-compress aggressively; `quality={80}` in `next/image` is enough.
- **For Treatment B only:** produce a transparent cutout (`alabi-portrait-cutout.png`) with a background-removal model (e.g. `rembg` with the `isnet-general-use` model) or Photoshop/Photopea, then manually clean hair/shoulder edges. Convert to WebP/AVIF with alpha.

### 6.3 Icons & OG image
- `icon.png` (512×512) and `apple-icon.png` (180×180): black background with the "A" from the wordmark (purple/gradient) or the trimmed logo centered with padding. `favicon.ico` (32×32 + 16×16).
- `opengraph-image.tsx` (static at build; uses `ImageResponse` from `next/og`): 1200×630, black bg, glow, portrait right-of-center or centered, logo top-left, "Coming Soon" in white. Read local images from disk with `fs` at build time and embed as data URIs; load the headline font file locally. Add `alt` export and `size`/`contentType` exports. `twitter-image` can re-export the same.
- Optional fallback: a pre-rendered static `og.png` committed to the repo if `ImageResponse` fonts become troublesome.

### 6.4 Sample prep script (adapt as needed)

```python
# scripts/process-assets.py  — pip install pillow numpy
from PIL import Image
import numpy as np

# --- Logo: trim + black→alpha ---
img = Image.open("logo.jpg").convert("RGB")
a = np.asarray(img).astype(np.float32)
alpha = a.max(axis=2) / 255.0
alpha = np.clip((alpha - 0.04) / 0.96, 0, 1)             # kill JPEG noise floor
rgb = np.where(alpha[..., None] > 0, a / np.maximum(alpha[..., None], 1e-3), 0)
rgba = np.dstack([np.clip(rgb, 0, 255), alpha * 255]).astype(np.uint8)
out = Image.fromarray(rgba, "RGBA")
out = out.crop(out.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox())
pad = int(out.height * 0.15)
canvas = Image.new("RGBA", (out.width + pad * 2, out.height + pad * 2), (0, 0, 0, 0))
canvas.paste(out, (pad, pad))
canvas.save("assets/alabi-logo.png", optimize=True)

# --- Portrait: crush near-black to pure black ---
p = np.asarray(Image.open("photo_6028165631812767835_y.jpg").convert("RGB")).astype(np.float32)
p = np.clip((p - 10) / (255 - 10), 0, 1) * 255
Image.fromarray(p.astype(np.uint8)).save("assets/alabi-portrait.jpg", quality=92, optimize=True)
```

---

## 7. SEO Implementation Checklist (maps to PRD §8)

| Requirement | Where / how |
|---|---|
| Static HTML with all tags in the initial response | SSG, Server Components only |
| Title, description, canonical, robots | `metadata` in `layout.tsx` |
| One real `<h1>` | `page.tsx` (`Coming Soon`) |
| `<html lang="en">`, landmarks | `layout.tsx`, `<header>`, `<main>` |
| Alt text | `page.tsx` |
| JSON-LD `Person` + `WebSite` | `JsonLd` component |
| OG/Twitter cards | `metadata` + `opengraph-image.tsx` |
| Favicon/manifest/theme-color | `app/icon.png`, `apple-icon.png`, `favicon.ico`, `manifest.ts`, `viewport` |
| `robots.txt` & `sitemap.xml` | `robots.ts`, `sitemap.ts` (below) |
| Preview deploys are `noindex` | `site.isProd` + `X-Robots-Tag` header (below) |
| 200 status, no 503 | default |
| 404 page `noindex` | `not-found.tsx` sets `robots: { index: false }` |
| HTTPS + single host | Vercel domain settings (§9) |

`app/robots.ts`
```ts
import type { MetadataRoute } from "next";
import { site } from "@/lib/site";

export default function robots(): MetadataRoute.Robots {
  if (!site.isProd) return { rules: { userAgent: "*", disallow: "/" } };
  return { rules: { userAgent: "*", allow: "/" }, sitemap: `${site.url}/sitemap.xml` };
}
```

`app/sitemap.ts`
```ts
import type { MetadataRoute } from "next";
import { site } from "@/lib/site";

export default function sitemap(): MetadataRoute.Sitemap {
  return [{ url: site.url, lastModified: "2026-11-11", changeFrequency: "monthly", priority: 1 }];
  // Use a fixed date; update it when content actually changes. Phase 2 routes get added here.
}
```

`app/manifest.ts`
```ts
import type { MetadataRoute } from "next";
import { site } from "@/lib/site";

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: site.brand, short_name: site.brand, description: site.description,
    start_url: "/", display: "standalone", background_color: "#000000", theme_color: "#000000",
    icons: [
      { src: "/icon.png", sizes: "512x512", type: "image/png" },
      { src: "/apple-icon.png", sizes: "180x180", type: "image/png" },
    ],
  };
}
```

`app/not-found.tsx` — minimal black page, white text "Page not found", link home; export `metadata = { title: "Not found", robots: { index: false } }`.

---

## 8. `next.config.ts`

```ts
import type { NextConfig } from "next";

const isProd = process.env.VERCEL_ENV === "production";

const nextConfig: NextConfig = {
  poweredByHeader: false,
  reactStrictMode: true,
  images: {
    formats: ["image/avif", "image/webp"],
    // imported static images need no remotePatterns
  },
  async headers() {
    const security = [
      { key: "X-Content-Type-Options", value: "nosniff" },
      { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
      { key: "X-Frame-Options", value: "DENY" },
      { key: "Permissions-Policy", value: "camera=(), microphone=(), geolocation=(), interest-cohort=()" },
    ];
    // Belt-and-braces: never index preview/dev deployments
    const robots = isProd ? [] : [{ key: "X-Robots-Tag", value: "noindex, nofollow" }];
    return [{ source: "/(.*)", headers: [...security, ...robots] }];
  },
};

export default nextConfig;
```

- HSTS: Vercel already serves HSTS on custom domains; don't duplicate unless required.
- Optional CSP: if added, it must allow `'self'` + the inline JSON-LD script (nonce or hash). Don't break the page for a minimal gain; verify in DevTools if enabled.
- No `output: "export"`: keep the default Vercel build so `next/image` optimization and headers work.

---

## 9. Vercel Deployment

1. Push repo to GitHub; import into Vercel. Framework preset: **Next.js** (auto). Build: `pnpm build`. Node: current LTS.
2. Environment variables (Production): `NEXT_PUBLIC_SITE_URL=https://[DOMAIN.COM]`, optional `NEXT_PUBLIC_GSC_VERIFICATION`. Preview needs none.
3. **Domain:** add apex and `www`; choose one as primary and set the other to **redirect (308 permanent)** to it; the primary host **must equal** `NEXT_PUBLIC_SITE_URL`. HTTPS is automatic.
4. Production branch: `main`. Every other branch/PR gets a preview URL that is `noindex` (verify with `curl -I`).
5. Optional: enable Vercel Web Analytics (cookieless, one tiny script) and Speed Insights. If enabled, re-check the "zero third-party requests / no cookie banner" requirement; both are first-party-served and cookieless. **Default is off**; ask the client.
6. After first production deploy: submit `https://[DOMAIN.COM]/sitemap.xml` in Google Search Console and Bing Webmaster Tools (verify via DNS TXT or the meta token), and use "Request indexing" for the home page.

Caching: Vercel caches static output on its CDN automatically; static asset URLs from `next/image` and `/_next/static` are immutable/versioned. Nothing custom needed.

---

## 10. Performance Rules

- Only **one** font file (Inter Tight 500, Latin subset), self-hosted via `next/font`.
- Portrait: `priority` (preload + `fetchpriority="high"`), accurate `sizes`, intrinsic dimensions from the static import → zero CLS. Logo: `priority` too (above the fold, tiny).
- No layout-affecting animation (transform/opacity only). No `backdrop-filter` or large animated blurs on mobile beyond the single static glow (watch GPU cost; if the blur causes jank on low-end Android, reduce blur radius or pre-render the glow as a small blurred PNG/CSS background instead).
- No JS bundles beyond Next's minimal runtime. Verify with `@next/bundle-analyzer` or the build output: first-load JS should be the framework baseline only.
- No third-party origins → no extra DNS/TLS.

---

## 11. Testing & QA

**Automated / CLI**
```bash
pnpm lint && pnpm build            # "/" must be ○ (Static)
pnpm start                         # then:
curl -sI http://localhost:3000     # 200, security headers present
curl -s  http://localhost:3000 | grep -E "<title>|<h1|application/ld\+json|canonical|og:image"
```
On the **production URL** (not localhost): run Lighthouse (mobile, throttled) and PageSpeed Insights; validate JSON-LD (Schema Markup Validator / Rich Results Test); check OG with a social debugger; confirm `robots.txt`, `sitemap.xml`, `manifest.webmanifest`, `/icon.png`, `/apple-icon.png`.

**Preview vs production check**
```bash
curl -sI https://<preview-url>.vercel.app | grep -i x-robots-tag   # noindex, nofollow
curl -s  https://<preview-url>.vercel.app/robots.txt                # Disallow: /
curl -sI https://[DOMAIN.COM]            | grep -i x-robots-tag    # (absent)
curl -s  https://[DOMAIN.COM]/robots.txt                           # Allow: / + Sitemap
```

**Visual QA matrix:** 1920×1080, 1440×900, 1280×720, 1024×768, 768×1024, 390×844, 360×740, 844×390 (landscape) on Chrome, Safari (iOS + macOS), Firefox, Edge. Check: no scrollbars/overflow, no visible photo rectangle, logo never collides with the headline, headline legible over the suit, reduced-motion disables animation.

---

## 12. Build Order for the Agent

1. Scaffold: `create-next-app` (TypeScript, Tailwind, App Router, ESLint, `src/` **off**, import alias `@/*`), pnpm, strict TS.
2. Add `lib/site.ts`, `.env.example`; configure `next.config.ts`.
3. Process assets (§6); place in `assets/`; generate icons.
4. Implement `layout.tsx`, `page.tsx`, `JsonLd`, `globals.css` (§4–5). Match the reference at 1440×900, then tablet and mobile.
5. Add `robots.ts`, `sitemap.ts`, `manifest.ts`, `not-found.tsx`, `opengraph-image.tsx`.
6. Run QA (§11), fix, re-measure with Lighthouse.
7. Write `README.md` (run, build, env vars, how assets were prepared, how to add Phase 2 routes + sitemap entries).
8. Deploy to Vercel, connect domain, run production checks, submit sitemap.

## 13. Definition of Done

All acceptance criteria in **PRD §12** pass on the production deployment, `/` builds as static, the first-load JS is the framework baseline, and the README is complete.

## 14. Phase 2 Hooks (don't build now)

- Add routes under `app/` (e.g. `/about`, `/work`, `/work/[slug]`, `/contact`) as static or ISR pages; use `generateMetadata` per page.
- Extend `sitemap.ts` from a route/content list; keep `lib/site.ts` as the metadata source.
- Content (case studies/blog) via MDX files or a headless CMS later; keep the same canonical host.
- Replace the coming-soon hero in place at `/` when launching; keep the URL unchanged.
