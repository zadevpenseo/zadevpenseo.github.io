# Contributing to Zadit // Systems & Blueprints

Thank you for your interest in contributing to the **Zadit Systems Architecture Vault**. We welcome technical corrections, case study improvements, documentation enhancements, and discussions on high-level system design.

## Code & Markup Standards

1. **Astro & MDX Syntax**:
   - Do NOT use raw HTML comments (`<!-- ... -->`) inside `.mdx` files as they fail MDX rollup compilation. Use JSX comments `{/* ... */}` or omit comments entirely.
   - All interactive embeds must include accessible titles, proper ARIA labels, and responsive wrapper styles.
2. **Anti-AI Slop & Tone**:
   - Write with clarity, precision, and active voice (William Strunk Jr. rules).
   - Omit generic buzzwords (`cutting-edge`, `game-changer`, `seamlessly`, `delve`).
   - Ground all architectural claims in verifiable benchmarks, code, or mathematics.
3. **Public Portfolio Separation**:
   - Case studies are public enterprise portfolio showcases. Never submit internal platform tender IDs (e.g. `#123456`) or proposal cover letters into public case study MDX files.

## Development Workflow

```bash
# 1. Fork and clone the repository
git clone https://github.com/<your-username>/zadevpenseo.github.io.git
cd zadevpenseo.github.io

# 2. Install dependencies
npm install

# 3. Start local development server
npm run dev

# 4. Verify build and Pagefind index generation
npm run build
```

Every PR must pass `npm run build` with zero errors prior to review.
