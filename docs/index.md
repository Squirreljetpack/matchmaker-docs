<div class="linear-hero">
  <div class="linear-badge">
    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
    <span>Documentation</span>
  </div>
  <h1 class="linear-hero-title">Matchmaker Documentation</h1>
  <p class="linear-hero-subtitle">
    <strong>Matchmaker</strong> (binary <code>mm</code>) is a fast, configurable and intuitive fuzzy searcher for the terminal. Pipe lines in, filter them with fzf-style fuzzy matching, and print the selections back out — with a full TUI, configurable columns, previews, and scripting on top.
  </p>
  <div class="linear-quick-chips">
    <a href="./01-getting-started" class="linear-chip">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="13 17 18 12 13 7"/><polyline points="6 17 11 12 6 7"/></svg>
      <span>Getting started</span>
    </a>
    <a href="./02-core-workflows" class="linear-chip">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
      <span>Core workflows</span>
    </a>
    <a href="./08-configuration" class="linear-chip">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
      <span>Configuration</span>
    </a>
    <a href="./11-binds-and-actions" class="linear-chip">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="4 6 20 6"/><line x1="4" y1="12" x2="20" y2="12"/><polyline points="4 18 20 18"/></svg>
      <span>Binds & actions</span>
    </a>
  </div>
</div>

<div class="linear-callout">
  <div class="linear-callout-icon">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
  </div>
  <div class="linear-callout-content">
    <strong>Apology for this documentation.</strong> These pages are an AI-drafted, incomplete scaffold — the prose will be rewritten by hand later. The reference pages (10–13) are the verbatim in-app docs from <code>mm --doc</code>.
  </div>
</div>

<div class="linear-sections-grid">

  <div class="linear-section-card">
    <div class="linear-section-header">
      <div class="linear-section-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16v16H4z"/><polyline points="9 8 15 12 9 16"/></svg>
      </div>
      <h3 class="linear-section-title">Getting started</h3>
    </div>
    <p class="linear-section-desc">Install, first run, and the everyday workflows.</p>
    <ul class="linear-link-list">
      <li class="linear-link-item">
        <a href="./01-getting-started">
          <span>01 – Getting started</span>
          <span class="arrow">→</span>
        </a>
      </li>
      <li class="linear-link-item">
        <a href="./02-core-workflows">
          <span>02 – Core workflows</span>
          <span class="arrow">→</span>
        </a>
      </li>
    </ul>
  </div>

  <div class="linear-section-card">
    <div class="linear-section-header">
      <div class="linear-section-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><line x1="3" y1="9" x2="21" y2="9"/></svg>
      </div>
      <h3 class="linear-section-title">The interface</h3>
    </div>
    <p class="linear-section-desc">The TUI, its data sources, columns and preview panel.</p>
    <ul class="linear-link-list">
      <li class="linear-link-item">
        <a href="./03-interface">
          <span>03 – Interface overview</span>
          <span class="arrow">→</span>
        </a>
      </li>
      <li class="linear-link-item">
        <a href="./04-input-and-data">
          <span>04 – Input & data sources</span>
          <span class="arrow">→</span>
        </a>
      </li>
      <li class="linear-link-item">
        <a href="./05-columns">
          <span>05 – Columns</span>
          <span class="arrow">→</span>
        </a>
      </li>
      <li class="linear-link-item">
        <a href="./06-preview">
          <span>06 – Preview</span>
          <span class="arrow">→</span>
        </a>
      </li>
      <li class="linear-link-item">
        <a href="./07-querying">
          <span>07 – Queries & matching</span>
          <span class="arrow">→</span>
        </a>
      </li>
    </ul>
  </div>

  <div class="linear-section-card">
    <div class="linear-section-header">
      <div class="linear-section-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 1 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
      </div>
      <h3 class="linear-section-title">Configuration</h3>
    </div>
    <p class="linear-section-desc">Config files, presets, and ready-made workflows.</p>
    <ul class="linear-link-list">
      <li class="linear-link-item">
        <a href="./08-configuration">
          <span>08 – Configuration files</span>
          <span class="arrow">→</span>
        </a>
      </li>
      <li class="linear-link-item">
        <a href="./09-presets">
          <span>09 – Presets & workflows</span>
          <span class="arrow">→</span>
        </a>
      </li>
    </ul>
  </div>

  <div class="linear-section-card">
    <div class="linear-section-header">
      <div class="linear-section-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
      </div>
      <h3 class="linear-section-title">References</h3>
    </div>
    <p class="linear-section-desc">The built-in documentation, exactly as printed by <code>mm --doc</code>.</p>
    <ul class="linear-link-list">
      <li class="linear-link-item">
        <a href="./10-command-line">
          <span>10 – Command line (mm --doc options)</span>
          <span class="arrow">→</span>
        </a>
      </li>
      <li class="linear-link-item">
        <a href="./11-binds-and-actions">
          <span>11 – Binds & actions (mm --doc binds)</span>
          <span class="arrow">→</span>
        </a>
      </li>
      <li class="linear-link-item">
        <a href="./12-templates">
          <span>12 – Templates (mm --doc template)</span>
          <span class="arrow">→</span>
        </a>
      </li>
      <li class="linear-link-item">
        <a href="./13-queries-and-misc">
          <span>13 – Queries & misc (mm --doc other)</span>
          <span class="arrow">→</span>
        </a>
      </li>
    </ul>
  </div>

  <div class="linear-section-card">
    <div class="linear-section-header">
      <div class="linear-section-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="4 17 10 11 4 5"/><line x1="12" y1="19" x2="20" y2="19"/></svg>
      </div>
      <h3 class="linear-section-title">Scripting & development</h3>
    </div>
    <p class="linear-section-desc">Scripts, Lua, embedding the library, and diagnostics.</p>
    <ul class="linear-link-list">
      <li class="linear-link-item">
        <a href="./14-scripting">
          <span>14 – Scripting</span>
          <span class="arrow">→</span>
        </a>
      </li>
      <li class="linear-link-item">
        <a href="./15-lua">
          <span>15 – Lua commands</span>
          <span class="arrow">→</span>
        </a>
      </li>
      <li class="linear-link-item">
        <a href="./16-library">
          <span>16 – Using the library</span>
          <span class="arrow">→</span>
        </a>
      </li>
      <li class="linear-link-item">
        <a href="./17-diagnostics">
          <span>17 – Diagnostics & logging</span>
          <span class="arrow">→</span>
        </a>
      </li>
    </ul>
  </div>

</div>
