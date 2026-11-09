import { useState } from "react";
import { rewriteMessage } from "./api/rewriter";

const MAX_LENGTH = 5000;

const tones = [
  ["professional", "Professional"],
  ["friendly", "Friendly"],
  ["formal", "Formal"],
  ["polite", "Polite"],
  ["persuasive", "Persuasive"],
  ["casual", "Casual"],
];

const lengths = [
  ["concise", "Concise"],
  ["balanced", "Balanced"],
  ["detailed", "Detailed"],
];

const recipients = [
  ["professor", "Professor"],
  ["recruiter", "Recruiter"],
  ["senior", "Senior"],
  ["colleague", "Colleague"],
  ["friend", "Friend"],
];

function App() {
  const [message, setMessage] = useState("");
  const [tone, setTone] = useState("professional");
  const [length, setLength] = useState("balanced");
  const [recipient, setRecipient] = useState("colleague");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [copied, setCopied] = useState(false);

  const remaining = MAX_LENGTH - message.length;
  const canRewrite = message.trim().length > 0 && !loading && message.length <= MAX_LENGTH;

  async function handleRewrite() {
    if (!canRewrite) return;
    setLoading(true);
    setError("");
    setCopied(false);
    setResult("");

    try {
      const rewritten = await rewriteMessage(message, {
        tone,
        length,
        recipient,
      });
      setResult(rewritten);
    } catch (error) {
        setError(
          error instanceof Error
            ? error.message
            : "The rewrite could not be completed. Please try again.",
        );
      }finally {
      setLoading(false);
    }
  }

  async function handleCopy() {
    if (!result) return;
    try {
      await navigator.clipboard.writeText(result);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1800);
    } catch {
      setError("Clipboard access was blocked. You can select and copy the text manually.");
    }
  }

  function handleClear() {
    setMessage("");
    setResult("");
    setError("");
    setCopied(false);
  }

  return (
    <div className="site-shell">
      <aside className="sidebar">
        <a className="brand" href="#top" aria-label="Rewrite home">
          <span className="brand-name">rewrite<span>.</span></span>
          <span className="brand-caption">MESSAGE EDITOR</span>
        </a>

        <div className="sidebar-intro">
          <span className="eyebrow">A TOOL FOR EVERYDAY WRITING</span>
          <p>A clearer way<br />to say it.</p>
        </div>

        <nav className="side-nav" aria-label="Main navigation">
          <a className="nav-link active" href="#studio"><span>01</span> THE EDITOR</a>
          <a className="nav-link" href="#approach"><span>02</span> HOW IT WORKS</a>
        </nav>

        <div className="sidebar-bottom">
          <div className="availability"><i /> EDITOR READY</div>
          <div className="sidebar-location">
            BUILT FOR CLEARER COMMUNICATION.<br />
            POWERED BY YOUR INTENT.
          </div>
          <a className="sidebar-contact" href="#studio">OPEN EDITOR <span>↗</span></a>
        </div>
      </aside>

      <main className="main-content" id="top">
        <header className="topbar">
          <span className="eyebrow">SMART MESSAGE REWRITER</span>
          <span className="topbar-index">EDITOR&nbsp;&nbsp; / &nbsp;&nbsp;001</span>
        </header>

        <section className="intro" id="approach">
          <div className="intro-copy">
            <div className="eyebrow section-kicker"><i /> MESSAGE EDITOR / 01</div>
            <h1>Rewrite your message.<br /><em>Keep your meaning.</em></h1>
            <p className="intro-description">
              Choose a tone, length, and recipient. Refine the wording while keeping the original message intact.
            </p>
          </div>
          <div className="intro-note">
            <span className="note-number">01 — 03</span>
            <span>TONE. LENGTH.<br />AUDIENCE.</span>
          </div>
        </section>

        <section className="studio" id="studio">
          <div className="section-heading">
            <div>
              <span className="eyebrow">01 / YOUR DRAFT</span>
              <h2>Your message.</h2>
            </div>
            <span className="section-aside">PASTE OR WRITE YOUR DRAFT.</span>
          </div>

          <div className="workspace">
            <div className="editor-panel">
              <div className="panel-topline">
                <label htmlFor="original-message" className="eyebrow">YOUR DRAFT</label>
                <span className="eyebrow">DRAFT</span>
              </div>
              <textarea
                id="original-message"
                value={message}
                onChange={(event) => {
                  setMessage(event.target.value.slice(0, MAX_LENGTH));
                  setResult("");
                  setError("");
                }}
                maxLength={MAX_LENGTH}
                placeholder="Type or paste the message you want to rewrite..."
                spellCheck
              />
              <div className="editor-footer">
                <span className="helper-copy">Up to 5,000 characters.</span>
                <span className={remaining < 200 ? "char-count warning" : "char-count"}>
                  {message.length.toLocaleString()} / {MAX_LENGTH.toLocaleString()}
                </span>
              </div>
            </div>

            <div className="preferences-panel">
              <div className="panel-topline">
                <span className="eyebrow">02 / PREFERENCES</span>
                <span className="eyebrow">STYLE</span>
              </div>

              <div className="preference-field">
                <label htmlFor="tone">TONE</label>
                <select id="tone" value={tone} onChange={(e) => setTone(e.target.value)}>
                  {tones.map(([value, label]) => <option key={value} value={value}>{label}</option>)}
                </select>
              </div>
              <div className="preference-field">
                <label htmlFor="length">LENGTH</label>
                <select id="length" value={length} onChange={(e) => setLength(e.target.value)}>
                  {lengths.map(([value, label]) => <option key={value} value={value}>{label}</option>)}
                </select>
              </div>
              <div className="preference-field">
                <label htmlFor="recipient">WRITING TO</label>
                <select id="recipient" value={recipient} onChange={(e) => setRecipient(e.target.value)}>
                  {recipients.map(([value, label]) => <option key={value} value={value}>{label}</option>)}
                </select>
              </div>

              <button className="rewrite-button" onClick={handleRewrite} disabled={!canRewrite}>
                <span>{loading ? "REFINING YOUR MESSAGE" : "REWRITE MESSAGE"}</span>
                <span className={loading ? "button-arrow loading-arrow" : "button-arrow"}>{loading ? "···" : "↗"}</span>
              </button>
              <p className="privacy-note">AI-POWERED MESSAGE REWRITING</p>
            </div>
          </div>

          <div className="result-section">
            <div className="result-heading">
              <div>
                <span className="eyebrow">03 / RESULT</span>
                <h2>Rewritten message</h2>
              </div>
              {result && (
                <button className="copy-button" onClick={handleCopy}>
                  {copied ? "COPIED ✓" : "COPY TEXT ↗"}
                </button>
              )}
            </div>

            <div className={`result-panel ${result ? "has-result" : ""}`}>
              {loading ? (
                <div className="result-placeholder loading-state">
                  <span className="loading-line" />
                  <span className="loading-line short" />
                  <p className="eyebrow">GIVING YOUR WORDS A MOMENT...</p>
                </div>
              ) : result ? (
                <>
                  <p className="result-text">{result}</p>
                  <div className="result-meta">
                    <span className="eyebrow">AI-POWERED REWRITE</span>
                    <span className="eyebrow">READY TO USE</span>
                  </div>
                </>
              ) : (
                <div className="result-placeholder">
                  <span className="placeholder-mark">“</span>
                  <p>Your rewritten message will appear here.</p>
                  <span className="eyebrow">WRITE A DRAFT AND SELECT REWRITE MESSAGE.</span>
                </div>
              )}
            </div>
            {error && <p className="error-message" role="alert">{error}</p>}
            <div className="result-actions">
              <button className="text-button" onClick={handleClear} disabled={!message && !result}>CLEAR WORKSPACE <span>↗</span></button>
              <span className="eyebrow">CHECK THE RESULT BEFORE YOU USE IT.</span>
            </div>
          </div>
        </section>

        <footer className="page-footer">
          <span>REWRITE<span className="red-dot">.</span> — MESSAGE EDITOR</span>
          <span>POWERED BY GROQ</span>
          <a href="#top">BACK TO TOP ↑</a>
        </footer>
      </main>
    </div>
  );
}

export default App;