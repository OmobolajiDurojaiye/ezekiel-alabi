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
          sizes="280px"
        />
      </header>

      <main className="hero">
        <div className="glow" aria-hidden="true" />

        {/* The single h1 landmark placed in layered depth */}
        <h1 className="headline">Coming Soon</h1>

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

        {/* Visually-hidden descriptive text for screen readers & crawlers */}
        <p className="sr-only">{site.description}</p>
      </main>
    </>
  );
}
