import { Analyzer } from "@/components/analyzer";
import { BrandWordmark } from "@/components/brand-wordmark";
import { SiteHeader } from "@/components/site-header";

export default function Home() {
  return (
    <main>
      <a className="skip-link" href="#main-content">Skip to content</a>
      <SiteHeader />
      <section className="hero shell" id="main-content" aria-labelledby="page-title">
        <div className="hero-copy">
          <p className="eyebrow"><span /> Resume feedback that makes sense</p>
          <h1 id="page-title">
            Make every <mark>glance</mark> count.
          </h1>
          <p className="hero-intro">
            See your resume the way a recruiter and their software will: what
            lands, what gets missed, and what to fix first.
          </p>
          <div className="hero-actions">
            <a className="primary-link" href="#analyze">Scan your resume</a>
            <span>PDF or DOCX · up to 10 MB</span>
          </div>
          <div className="hero-proof" aria-label="Product promises">
            <span>Clear scoring</span>
            <span>Specific fixes</span>
            <span>No black-box verdicts</span>
          </div>
        </div>
        <aside className="sample-card" aria-label="Sample resume analysis">
          <div className="sample-card-topline">
            <span>Sample scan</span>
            <span className="live-chip"><i /> complete</span>
          </div>
          <div className="sample-score">
            <mark>82</mark>
            <div>
              <strong>out of 100</strong>
              <span>looking good</span>
            </div>
          </div>
          <div className="sample-bars">
            <div><span>keywords</span><i><b style={{ width: "76%" }} /></i><strong>76</strong></div>
            <div><span>formatting</span><i><b style={{ width: "94%" }} /></i><strong>94</strong></div>
            <div><span>impact</span><i><b style={{ width: "71%" }} /></i><strong>71</strong></div>
          </div>
          <div className="sample-note">
            <span>high impact</span>
            <p>Add outcomes to your project bullets. “Built a dashboard” tells us what; <mark>show what changed.</mark></p>
          </div>
          <p className="sample-caption">A preview using example data—not your result.</p>
        </aside>
      </section>

      <section className="method-strip shell" id="how-it-works" aria-label="How Glance works">
        <div><span>01</span><p><strong>Add your resume</strong>PDF or DOCX. A job description makes the result sharper.</p></div>
        <div><span>02</span><p><strong>See what survives</strong>We check role skills and whether the document can be parsed cleanly.</p></div>
        <div><span>03</span><p><strong>Fix what matters</strong>Start with the gaps that make the biggest difference.</p></div>
      </section>

      <Analyzer />

      <footer className="site-footer shell">
        <BrandWordmark />
        <p>Built to explain the score, not mystify it.</p>
      </footer>
    </main>
  );
}
