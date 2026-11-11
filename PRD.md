# PRD — "Coming Soon" Page (Phase 1 of Personal Portfolio Website)

| | |
|---|---|
| **Doc type** | Product Requirements Document |
| **Companion doc** | `TRD.md` (technical implementation) |
| **Status** | Ready for build |
| **Deploy target** | Vercel |
| **Priority pillars** | 1) SEO 2) Visual fidelity to the reference 3) Performance |

> **Placeholders** to be filled before launch are written as `[LIKE_THIS]`. Collect them from the client; do not invent values.

---

## 1. Summary

Build a single-page, full-screen **Coming Soon** site for a personal brand ("**Alabi**", per the supplied logo). It is the first phase of a larger portfolio website that will be built on the same codebase and domain later.

The visual direction is copied from the attached reference (`Soleve` coming-soon page: full-bleed hero, subject photo in the center, a huge white "Coming Soon" headline, logo top-left) with everything non-essential removed.

**The page contains exactly three visible elements:**

1. The logo (image), top-left
2. The client's photo, centered
3. The words "Coming Soon", set very large

Nothing else is visible. No newsletter, no email field, no paragraph, no nav, no menu icon, no year, no location, no socials.

---

## 2. Goals

| # | Goal | How we'll know |
|---|------|----------------|
| G1 | Look like the reference, in the client's brand | Side-by-side visual review with the reference at 1440, 1024, 768 and 390 px widths |
| G2 | Be indexable and ready to rank from day one, so the domain has history when the portfolio launches | All SEO acceptance criteria in §8 pass |
| G3 | Load instantly | Lighthouse mobile: Performance ≥ 95, LCP < 1.5 s, CLS = 0, TBT ≈ 0 |
| G4 | Become the foundation of the full portfolio with no rewrite | Same repo, same domain, same URL structure; portfolio pages are added, nothing is thrown away |

## 3. Non-goals (explicitly out of scope)

- Email capture / newsletter / waitlist / any form
- Any visible text other than "Coming Soon"
- Navigation, hamburger/menu icon, footer, copyright, location, social links
- CMS, database, auth, API routes
- Third-party scripts (chat widgets, pixels, tag managers, etc.)
- Cookie banner (not needed because nothing sets cookies — keep it that way)
- Multiple pages (the portfolio pages come in Phase 2)

---

## 4. Brand & Assets

### 4.1 Colors

Main colors are **black and white**. Pink and purple are **accents only**, used either as a gradient or individually.

| Token | Hex | Role |
|---|---|---|
| `--black` | `#000000` | Page background (primary) |
| `--white` | `#FFFFFF` | Headline text (primary) |
| `--pink` | `#E5A0FD` | Accent (light) — gradient start, glows, highlights |
| `--purple` | `#9900CC` | Accent (deep) — gradient end, glows, focus ring |

Signature gradient: `linear-gradient(135deg, #E5A0FD 0%, #9900CC 100%)`.

**Usage rules**
- Black and white carry the page. Accents must stay subtle: they should read as light and atmosphere, not as paint.
- Do not use pink/purple for the "Coming Soon" text fill by default (see §6.4 for the optional variant).
- No other hues. Greys are fine for secondary shading only.

### 4.2 Asset inventory

| File (as uploaded) | What it is | Use | Notes for the agent |
|---|---|---|---|
| `logo.jpg` | Wordmark "Alabi", purple italic serif on a black 1280×1280 canvas | Top-left logo | The wordmark sits in the lower-right of a mostly empty square. **Trim the empty black space** so only the word (plus small even padding) remains. Ideally request an SVG/PNG-with-transparency from the client; until then, trim and convert the JPG. |
| `photo_6028165631812767835_y.jpg` | Portrait of the client: grey pinstripe double-breasted suit, purple tie and pocket square, smiling, on a solid black background, cropped at the waist, 1280×1280 | Center hero image | Already on black, so it blends with the black page. See TRD §6 for the cutout/edge handling. The crop bleeds off the bottom edge, which is the intended look (same as the reference). |
| `colors.jpg` | Two color swatches | Reference only | **Do not ship.** Values are captured in §4.1. |
| `1794433647493_image.png` | Reference design (Soleve) | Reference only | **Do not ship.** |

> Rename shipped assets to clean, SEO-friendly names: `alabi-logo`, `alabi-portrait` (see TRD §6).

---

## 5. Reference analysis (what to copy, what to drop)

| Reference element | Decision |
|---|---|
| Full-viewport, edge-to-edge hero | **Keep** |
| Subject photo centered, bleeding off the bottom | **Keep** |
| Huge "Coming Soon" headline, tight tracking, white, spanning most of the viewport width, sitting at about chest height of the subject | **Keep** |
| Soft, atmospheric color wash behind the subject | **Keep, but in brand colors**: black base with a faint pink→purple glow behind the subject instead of the reference's blue-grey |
| Logo top-left | **Keep** (uses the client's logo image) |
| "©2025" and double-line menu icon top-right | **Drop** |
| Paragraph copy bottom-right | **Drop** |
| Email field + Subscribe button | **Drop** |
| Globe icon + "Tbilisi — Georgia" bottom-left | **Drop** |

---

## 6. Functional & Visual Requirements

### 6.1 Layout (desktop ≥ 1024 px)

- Page is exactly one viewport tall (`100svh`), no scrolling, no scrollbars.
- **Logo:** top-left, ~`clamp(24px, 4vw, 56px)` from the top and left edges. Height ≈ 28–36 px on desktop. Links nowhere on this page (it's not a link; `/` is the only URL).
- **Photo:** horizontally centered, anchored to the bottom edge, as tall as the viewport (square source, so ≈ viewport height wide). The head sits in the upper-middle of the screen, the torso bleeds off the bottom.
- **Headline "Coming Soon":** one line, centered horizontally, vertically placed roughly at the subject's chest (about 55–70 % of viewport height from the top, same relative position as in the reference). Font size scales fluidly so the line spans ≈ 85–92 % of viewport width.
- Layer order (back → front): black background → accent glow → subject → headline (default; see §6.3) → logo.

### 6.2 Responsive behavior

| Breakpoint | Behavior |
|---|---|
| ≥ 1024 px | As above |
| 640–1023 px | Same composition; headline still one line; photo may scale to ~100–110 % of viewport height |
| < 640 px (mobile) | Photo is scaled so the subject fills the width (may crop slightly at the sides), still bottom-anchored and centered. Headline may wrap to two lines ("Coming" / "Soon"), left-aligned or centered (pick whichever matches the reference feel best), still at chest height. Logo stays top-left, smaller. |
| Landscape phones / very short viewports | Must not break: use `svh`/`dvh`, no overlapping of logo with headline |

All of the above must also work with mobile browser UI collapsing/expanding (no layout jump).

### 6.3 Headline treatment

- Text: **"Coming Soon"** (exact casing as in the reference).
- White (`#FFFFFF`), very large, medium weight, tight negative letter-spacing, clean geometric/neo-grotesk sans (default: *Inter Tight* or similar; the reference uses a geometric sans). Final font choice is the agent's call within that description; it must be self-hosted via the framework's font optimization (no external font requests at runtime).
- **Default treatment (A, ship this):** headline sits **in front of** the subject. Add a very soft black gradient at the bottom of the photo (scrim) so white text stays legible over the grey suit. Large-text contrast must be ≥ 3:1 against whatever is behind it.
- **Stretch treatment (B, behind a CSS variable/flag, only if a clean transparent cutout of the subject exists):** headline sits **behind** the subject so the shoulders/collar slightly overlap the top of the letters, mimicking the reference's layered look. Must not hurt legibility; if more than ~20 % of any letter is hidden, fall back to A.

### 6.4 Accent usage (pink / purple)

Required:
- A soft **radial glow** behind the subject's head/shoulders using the pink→purple gradient at low opacity (target ≈ 25–40 %), heavily blurred. It should look like atmosphere, not a spotlight with visible edges.
- `theme-color` meta, text selection color, and focus ring use the accents.

Optional (only if it looks good and stays classy):
- A subtle slow drift/pulse on the glow.
- Gradient fill on the word "Soon" only. If used, keep "Coming" white.

### 6.5 Motion

- On load: a short fade-in/slide-up (≈ 600–900 ms) for headline and photo, logo fades in. CSS only.
- Optional: very slow glow movement.
- Everything must be disabled under `prefers-reduced-motion: reduce`.
- **Critical:** animation must never delay or hide the LCP element from crawlers/SEO tools. The hero image and headline must be present in the initial HTML and visible without JavaScript (opacity animation must be CSS-driven and must start from a state that doesn't break rendering for no-JS/bots).

### 6.6 Interactions

None. No hover states needed other than default cursor. Text on the page should be selectable.

---

## 7. Content

| Item | Value |
|---|---|
| Visible text | `Coming Soon` (only) |
| Brand/Person name | `Alabi` (from logo). Full name: `[FULL_NAME]` |
| Profession/niche (for metadata only) | `[PROFESSION_OR_NICHE]` e.g. "Software engineer", "Lawyer", "Designer" |
| Domain | `[DOMAIN.COM]` |
| Location (metadata only, optional) | `[CITY, COUNTRY]` |

### Metadata copy (draft, confirm with the client)

- **Title (≤ 60 chars):** `Alabi — [Profession] | Coming Soon`
- **Meta description (≤ 155 chars):** `[Full Name] ([Alabi]) is a [profession] in [location]. The official portfolio is coming soon.`
- **Open Graph / Twitter title:** same as title
- **OG image:** 1200×630, black background, portrait, logo, and "Coming Soon" (composite of the three visible elements)

---

## 8. SEO Requirements (top priority)

The page is minimal visually, but it must be a complete, well-formed SEO document.

**Indexing & crawling**
- [ ] The production site is **indexable** (`index, follow`) and returns **HTTP 200**. (Do not use `noindex`; do not use a 503 "maintenance" response. Establishing the domain early helps later ranking.)
- [ ] **Non-production deployments** (Vercel preview/branch URLs) are `noindex, nofollow` (meta tag + `X-Robots-Tag` header) so duplicates never get indexed.
- [ ] `/robots.txt` and `/sitemap.xml` are served and correct (sitemap contains the canonical home URL).
- [ ] A single canonical URL (`https://[DOMAIN]/`). `www` ↔ apex redirects with a 301 to one chosen host, HTTPS enforced.

**On-page**
- [ ] `<html lang="en">`.
- [ ] Unique `<title>` and meta description (see §7).
- [ ] **Exactly one `<h1>`**: the visible "Coming Soon" text. It is real text in the DOM (not an image, not canvas, not CSS content).
- [ ] The page has a `<main>` landmark and a `<header>` containing the logo.
- [ ] The portrait `<img>` has a descriptive, honest `alt` (e.g. `Portrait of [Full Name], [profession], in a grey pinstripe suit`). The logo `alt` is the brand name (`Alabi`).
- [ ] Because visible text is minimal, add a short **visually-hidden (sr-only) descriptive sentence** inside `<main>` for screen readers and crawlers that restates the meta description honestly. No keyword stuffing, no hidden text that differs from what the page communicates.

**Social & structured data**
- [ ] Open Graph and Twitter Card tags (`summary_large_image`) with the 1200×630 image, absolute URLs.
- [ ] **JSON-LD** `Person` (and `WebSite`) schema: `name`, `url`, `image`, `jobTitle`, and `sameAs` (social profiles, `[SOCIAL_URLS]`, if the client supplies them).
- [ ] Favicon set: `favicon.ico`, SVG/PNG icon, `apple-touch-icon` (180×180), and a web manifest. Derived from the logo/monogram.
- [ ] `theme-color` = `#000000`.

**Technical SEO**
- [ ] Core Web Vitals in the "good" range on mobile (see §9).
- [ ] Zero console errors, zero broken links/assets, correct 404 page (simple, on-brand, `noindex`).
- [ ] Search Console and Bing Webmaster verification supported (via DNS TXT or meta tag), added once the client provides the code.

---

## 9. Performance & Quality Targets

| Metric | Target (mobile, throttled) |
|---|---|
| Lighthouse Performance | ≥ 95 |
| Lighthouse SEO / Best Practices / Accessibility | 100 / 100 / ≥ 95 |
| LCP | < 1.5 s (LCP element = hero image or headline) |
| CLS | 0 |
| INP / TBT | ~0 (page ships effectively no client JS) |
| Total page weight | < 250 KB ideal (hero image in AVIF/WebP is the bulk) |
| Third-party requests | 0 |

## 10. Accessibility

- Text contrast ≥ 3:1 for the large headline over its actual background (check over the suit region), ≥ 4.5:1 for any small text (there is none).
- Respect `prefers-reduced-motion`.
- Keyboard: nothing focusable except (optionally) nothing; no focus traps.
- Meaningful `alt` text, semantic landmarks, correct heading order.

## 11. Browser / Device Support

Latest two versions of Chrome, Safari (including iOS Safari), Firefox, Edge; Samsung Internet. Test on at least: 1920×1080, 1440×900, 1280×720, 1024×768, 768×1024, 390×844, 360×740, and a landscape phone (844×390).

---

## 12. Acceptance Criteria (definition of done)

1. Visually matches the reference composition using the client's assets and brand colors at all test sizes; **only** logo, photo, and "Coming Soon" are visible.
2. Every box in §8 is checked and verifiable (view-source shows all tags, one `h1`, JSON-LD validates in Google's Rich Results / Schema Markup Validator).
3. Lighthouse targets in §9 are met on the production Vercel deployment (not just locally).
4. No scrollbars, no layout shift, no horizontal overflow at any test size.
5. Preview deployments are `noindex`; production is indexable.
6. Domain connected, HTTPS valid, `www`/apex redirect works.
7. README documents how to run, build, and deploy, and how Phase 2 pages will be added.

## 13. Phase 2 (informational, don't build now)

The full portfolio (About, Work/Projects, Services, Contact, possibly a blog) will live in the same project. Keep the code structure and metadata utilities reusable so adding routes needs no restructuring. When Phase 2 launches, the home URL stays the same (no redirect), and "Coming Soon" is replaced in place.

## 14. Open Questions for the Client

1. Full name, profession/niche, location for metadata and schema?
2. Final domain?
3. Logo as SVG or transparent PNG (better than the current padded JPG)?
4. A transparent-background version of the portrait (PNG/PSD) for the layered headline effect (§6.3 B)?
5. Social profile URLs for `sameAs`?
6. Any preferred typeface for the headline?
