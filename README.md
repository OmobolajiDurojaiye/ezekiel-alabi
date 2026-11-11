# ezekiel-alabi

Official personal brand and portfolio website for **Ezekiel Alabi** ("Alabi").

Phase 1 features a full-screen, minimalist, high-impact "Coming Soon" landing page crafted with visual fidelity to the Soleve reference design, featuring subtle atmospheric lighting in the brand's pink and purple accents, high contrast typography, and top-tier SEO and Core Web Vitals optimization.

---

## 🎨 Visual & Brand Architecture

- **Primary Colors**: Black (`#000000`) and White (`#FFFFFF`)
- **Accents**: Light Pink (`#E5A0FD`) to Deep Purple (`#9900CC`) signature gradient
- **Composition**:
  - Wordmark logo top-left
  - Centered bottom-anchored portrait of Ezekiel Alabi
  - Large geometric headline `Coming Soon` in white Inter Tight
  - Atmospheric pink/purple ambient glow behind head & shoulders

---

## 🚀 Tech Stack

- **Framework**: [Next.js 15](https://nextjs.org/) (App Router, React 19)
- **Styling**: [Tailwind CSS v4](https://tailwindcss.com/)
- **Typography**: Self-hosted `Inter Tight` via `next/font/local` (zero external font requests at runtime)
- **Rendering**: 100% Static Site Generation (`○ Static`) for sub-second delivery
- **Package Manager**: `pnpm`
- **Hosting Target**: [Vercel](https://vercel.com/)

---

## 🛠️ Getting Started

### Prerequisites

- Node.js 20+ or 22+
- `pnpm` (install via `npm install -g pnpm`)

### Installation

```bash
pnpm install
```

### Development

```bash
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Production Build

```bash
pnpm build
pnpm start
```

---

## 🔍 SEO & Technical Architecture

- **Semantic Landmark Structure**: Valid `<header>`, `<main>`, `<h1 class="headline">Coming Soon</h1>`, and screen-reader context `<p class="sr-only">`.
- **Structured Data**: JSON-LD with `WebSite` and `Person` schemas (`jobTitle`, `alternateName`, `image`, `url`).
- **OpenGraph & Twitter Cards**: Dynamic 1200×630 composite social banner generated and served statically.
- **Environment-Aware Indexing**:
  - Production (`VERCEL_ENV=production`): Returns `index, follow`, HTTP 200, and enables `sitemap.xml`.
  - Preview & Local: Enforces `noindex, nofollow` via meta tags and `X-Robots-Tag` header.
- **Icons & Manifest**: Complete favicon suite (`favicon.ico`, `icon.png` 512×512, `apple-icon.png` 180×180) and web manifest (`manifest.webmanifest`).

---

## 📁 Project Structure

```
.
├── app/
│   ├── apple-icon.png         # 180x180 Apple touch icon
│   ├── favicon.ico            # Favicon
│   ├── globals.css            # Tailwind CSS v4 design tokens and page styles
│   ├── icon.png               # 512x512 site icon
│   ├── layout.tsx             # Root layout with fonts, viewport, and metadata
│   ├── manifest.ts            # Web app manifest
│   ├── not-found.tsx          # On-brand 404 page (noindex)
│   ├── opengraph-image.png    # 1200x630 social card
│   ├── page.tsx               # Coming Soon hero page (Server Component)
│   ├── robots.ts              # Env-aware robots.txt
│   ├── sitemap.ts             # Canonical XML sitemap
│   └── twitter-image.png      # Twitter summary card
├── assets/
│   ├── alabi-logo.png         # Trimmed transparent logo
│   ├── alabi-portrait.jpg     # Calibrated hero portrait
│   └── fonts/                 # Self-hosted Inter Tight
├── components/
│   └── JsonLd.tsx             # Structured schema component
├── lib/
│   └── site.ts                # Central configuration source of truth
├── scripts/
│   ├── generate-og.py         # OG composite graphic generator
│   └── process-assets.py      # Asset preparation script
├── .env.example
├── next.config.ts
├── package.json
└── README.md
```

---

## 🔮 Phase 2: Expanding to Full Portfolio

When transitioning from Phase 1 (Coming Soon) to Phase 2 (Full Portfolio):
1. **Retain Domain & Canonical URL**: The canonical URL remains `https://ezekielalabi.com/`.
2. **Add Routes**: Create new App Router directories (e.g. `app/about/page.tsx`, `app/work/page.tsx`, `app/contact/page.tsx`).
3. **Update Homepage**: Replace `app/page.tsx` coming-soon hero with the complete portfolio homepage layout.
4. **Update Sitemap**: Add new routes to `app/sitemap.ts`.
5. **Centralized Metadata**: Update `lib/site.ts` with social links (`sameAs`) and updated descriptions without changing site foundations.
