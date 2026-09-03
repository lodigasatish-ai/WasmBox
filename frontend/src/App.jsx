import Editor from "@monaco-editor/react";
import "./App.css";

const code = `def main():
    print("Hello from WasmBox!")

if __name__ == "__main__":
    main()`;

function App() {
  return (
    <div className="app">
      {/* TOP BAR */}
      <header className="topbar">
        <div className="brand">
          <div className="brand-icon">◇</div>
          <span>WasmBox</span>
        </div>

        <div className="divider" />

        <div className="subtitle">Secure Python Plugin Sandbox</div>

        <div className="sandbox-selector">
          <span className="status-dot" />
          SANDBOX: LOCAL <span>⌄</span>
        </div>

        <div className="top-actions">
          <div className="ready">
            <span />
            EDITOR READY
          </div>
          <div className="top-icon">☼</div>
          <div className="top-icon">?</div>
          <div className="top-icon">♧</div>
          <div className="avatar">WB</div>
        </div>
      </header>

      <div className="layout">
        {/* SIDEBAR */}
        <aside className="sidebar">
          <nav>
            <div className="nav-item active">
              <span>&lt;/&gt;</span>
              Editor
            </div>

            <div className="nav-item">
              <span>□</span>
              Explorer
            </div>

            <div className="nav-item">
              <span>♧</span>
              Plugins
            </div>

            <div className="nav-item">
              <span>♢</span>
              Security
            </div>

            <div className="nav-item">
              <span>⚙</span>
              Settings
            </div>

            <div className="nav-item">
              <span>▤</span>
              Docs
            </div>

            <div className="nav-item">
              <span>ⓘ</span>
              About
            </div>
          </nav>

          <div className="sidebar-bottom">
            <div className="sidebar-card">
              <div className="cube">◇</div>

              <h3>
                ISOLATED.
                <br />
                SECURE.
                <br />
                POWERFUL.
              </h3>

              <p>
                Every plugin runs in a WebAssembly sandbox with zero trust.
              </p>

              <button>Learn more →</button>
            </div>

            <div className="engine-card">
              <span className="engine-icon">⬡</span>

              <div>
                <small>WASM ENGINE</small>
                <strong>v1.0.0</strong>
              </div>

              <span className="online" />
            </div>
          </div>
        </aside>

        {/* MAIN */}
        <main className="main">
          {/* HERO */}
          <section className="hero">
            <div className="hero-text">
              <small>SECURE DEVELOPMENT ENVIRONMENT</small>

              <h1>
                Build without <span>boundaries.</span>
              </h1>

              <p>
                Write, test, and prepare secure Python plugins
                <br />
                inside a fully isolated WebAssembly sandbox.
              </p>
            </div>

            <div className="security-cards">
              <SecurityCard
                icon="◎"
                title="NETWORK"
                status="BLOCKED"
                text="No outbound connections"
                type="purple"
              />

              <SecurityCard
                icon="□"
                title="FILESYSTEM"
                status="ISOLATED"
                text="Read-only sandbox"
                type="blue"
              />

              <SecurityCard
                icon="♢"
                title="SECURITY"
                status="100% ISOLATED"
                text="WASM Sandbox Active"
                type="green"
              />
            </div>
          </section>

          {/* WORKSPACE */}
          <section className="workspace">
            {/* EDITOR */}
            <div className="editor-panel">
              <div className="editor-header">
                <div className="file-tab">
                  <span className="python-icon">🐍</span>
                  <span>plugin.py</span>
                  <span className="close">×</span>
                </div>

                <span className="plus">+</span>

                <div className="language">
                  🐍 Python <span>⌄</span>
                </div>

                <span className="more">⋮</span>
              </div>

              <Editor
                height="430px"
                defaultLanguage="python"
                defaultValue={code}
                theme="vs-dark"
                options={{
                  minimap: {
                    enabled: true,
                  },
                  fontSize: 15,
                  lineHeight: 25,
                  padding: {
                    top: 16,
                  },
                  automaticLayout: true,
                  scrollBeyondLastLine: false,
                  fontFamily: "JetBrains Mono, Menlo, monospace",
                  smoothScrolling: true,
                  cursorSmoothCaretAnimation: "on",
                  renderLineHighlight: "all",
                }}
              />

              <div className="editor-status">
                <span>Ln 1, Col 1</span>
                <span>Spaces: 4</span>
                <span>UTF-8</span>
                <span>LF</span>
                <span>🐍 Python 3.11</span>
                <span>♢ WASM Sandbox</span>
                <span className="issues">✓ No issues</span>
              </div>
            </div>

            {/* RIGHT PANEL */}
            <aside className="right-panel">
              <div className="info-card sandbox-status">
                <h3>SANDBOX STATUS</h3>

                <div className="shield">♢</div>

                <strong>SECURE</strong>

                <p>
                  Environment is locked down
                  <br />
                  and ready for code.
                </p>
              </div>

              <div className="info-card runtime-card">
                <h3>RUNTIME INFO</h3>

                <InfoRow icon="🐍" name="Python" value="3.11.7" />
                <InfoRow icon="WA" name="WebAssembly" value="wasmtime" />
                <InfoRow icon="⚙" name="Engine" value="wasmtime-py" />
              </div>

              <div className="info-card shortcuts-card">
                <h3>SHORTCUTS</h3>

                <Shortcut name="Format Code" keys="⇧  ⌥  F" />
                <Shortcut name="Run" keys="⌘ Enter" />
                <Shortcut name="Toggle Comments" keys="⌘ /" />
                <Shortcut name="Auto Complete" keys="⌃ Space" />
              </div>
            </aside>
          </section>

          {/* RUN BAR */}
          <section className="run-bar">
            <button className="run-button">
              ▶ &nbsp; Run Plugin
            </button>

            <div className="run-info">
              <span className="run-dot" />

              <div>
                <strong>Sandbox ready</strong>
                <p>Your plugin is ready to execute securely.</p>
              </div>
            </div>

            <div className="run-graphic">◇</div>
          </section>
        </main>
      </div>
    </div>
  );
}

function SecurityCard({ icon, title, status, text, type }) {
  return (
    <div className="security-card">
      <div className={`security-icon ${type}`}>{icon}</div>

      <div>
        <small>{title}</small>
        <strong className={type}>{status}</strong>
        <p>{text}</p>
      </div>
    </div>
  );
}

function InfoRow({ icon, name, value }) {
  return (
    <div className="info-row">
      <span>{icon}</span>
      <label>{name}</label>
      <strong>{value}</strong>
    </div>
  );
}

function Shortcut({ name, keys }) {
  return (
    <div className="shortcut">
      <span>{name}</span>
      <kbd>{keys}</kbd>
    </div>
  );
}

export default App;