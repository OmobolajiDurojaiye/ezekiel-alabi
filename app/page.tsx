import Image from "next/image";
import logo from "@/assets/alabi-logo.png";
import portrait from "@/assets/alabi-portrait.png";
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
              name: site.fullName,
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
        <Image
          src={logo}
          alt={site.fullName}
          priority
          className="logo"
          sizes="320px"
        />
      </header>

      <main className="hero">
        <div className="glow" aria-hidden="true" />

        {/* Layer 1: Behind the subject - "Coming" passes through the back in black */}
        <div className="headline-layer headline-back" aria-hidden="true">
          <span className="word-coming">Coming</span>
          <span className="word-space">&nbsp;</span>
          <span className="word-soon-ghost">Soon</span>
        </div>

        {/* Subject: Cutout portrait anchored at z-index 2 */}
        <div className="subject">
          <Image
            src={portrait}
            alt={`Portrait of ${site.fullName}, ${site.jobTitle}, in a grey pinstripe suit with a purple tie`}
            fill
            priority
            quality={90}
            sizes="(max-width: 639px) 145vw, (max-width: 1023px) 110vh, 100vh"
            className="subject-img"
          />
        </div>

        {/* Layer 2: In front of the subject - single H1 landmark with half-white/half-black "Soon" */}
        <h1 className="headline-layer headline-front">
          <span className="word-coming-ghost" aria-hidden="true">Coming</span>
          <span className="word-space" aria-hidden="true">&nbsp;</span>
          <span className="word-soon-front">Soon</span>
        </h1>

        {/* Visually-hidden descriptive text for screen readers & crawlers */}
        <p className="sr-only">{site.description}</p>
      </main>
    </>
  );
}
