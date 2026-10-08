import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';
import sharp from 'sharp';

function escapeXml(unsafe: string): string {
  return String(unsafe)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

function wrapText(text: string, maxChars = 34): string[] {
  const words = text.split(' ');
  const lines: string[] = [];
  let cur = '';
  for (const w of words) {
    if ((cur + ' ' + w).trim().length <= maxChars) {
      cur = (cur + ' ' + w).trim();
    } else {
      if (cur) lines.push(cur);
      cur = w;
    }
  }
  if (cur) lines.push(cur);
  return lines.slice(0, 3);
}

function determinePillar(id: string): string {
  if (id.includes('web-dev-design')) return 'WEB DEV DESIGN';
  if (id.includes('seo')) return 'SEO';
  if (id.includes('writer')) return 'WRITER';
  if (id.includes('data-analysis')) return 'DATA ANALYSIS';
  if (id.includes('methodology')) return '3-TIER PROOF';
  if (id.includes('case-studies')) return 'SYSTEMS VAULT';
  if (id.includes('monograf')) return 'MONOGRAPH';
  return 'SYSTEMS BLUEPRINT';
}

export async function getStaticPaths() {
  const docs = await getCollection('docs');
  const paths = docs.map((entry) => ({
    params: { slug: entry.id },
    props: {
      title: entry.data.title,
      description: entry.data.description || 'Verified engineering case study and system architecture blueprint.',
      pillar: determinePillar(entry.id),
    },
  }));

  // Include root homepage og/index.png
  paths.push({
    params: { slug: 'index' },
    props: {
      title: 'Zadit // Web Dev Design · SEO · Writer · Data Analysis',
      description: 'Verifiable systems architecture: deterministic High-Level Designs (HLD), failure-mode isolation, and deployable prototypes.',
      pillar: 'SYSTEMS & BLUEPRINTS',
    },
  });

  return paths;
}

export const GET: APIRoute = async ({ props }) => {
  const { title, description, pillar } = props as { title: string; description: string; pillar: string };

  const titleLines = wrapText(title, 34);
  let titleSpans = '';
  titleLines.forEach((line, idx) => {
    titleSpans += `<text x="0" y="${idx * 58}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="44" font-weight="800" fill="#ffffff" letter-spacing="-0.5">${escapeXml(line)}</text>`;
  });

  const descY = 175 + titleLines.length * 58 + 18;
  const descLines = wrapText(description, 68);
  let descSpans = '';
  descLines.forEach((line, idx) => {
    descSpans += `<text x="0" y="${idx * 28}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="20" fill="#94a3b8">${escapeXml(line)}</text>`;
  });

  const pillarText = escapeXml(pillar);
  const pillarWidth = Math.max(140, pillarText.length * 10 + 36);

  const svg = `<svg width="1200" height="630" viewBox="0 0 1200 630" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0b0f19" />
      <stop offset="50%" stop-color="#0f172a" />
      <stop offset="100%" stop-color="#0b0f19" />
    </linearGradient>
    <linearGradient id="blueGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#2563eb" />
      <stop offset="100%" stop-color="#60a5fa" />
    </linearGradient>
  </defs>

  <rect width="1200" height="630" fill="url(#bgGrad)" />
  <rect x="24" y="24" width="1152" height="582" rx="16" fill="none" stroke="#1e293b" stroke-width="2" />
  <rect x="26" y="26" width="1148" height="578" rx="14" fill="none" stroke="#334155" stroke-width="1" stroke-opacity="0.5" />
  <rect x="26" y="26" width="1148" height="4" rx="2" fill="url(#blueGrad)" />

  <g transform="translate(64, 76)">
    <rect width="320" height="34" rx="6" fill="#1e293b" stroke="#3b82f6" stroke-width="1" stroke-opacity="0.6" />
    <circle cx="16" cy="17" r="4" fill="#3b82f6" />
    <text x="32" y="22" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="13" font-weight="700" fill="#93c5fd" letter-spacing="1.5">ZADIT // SYSTEMS &amp; BLUEPRINTS</text>
  </g>

  <g transform="translate(${1200 - 64 - pillarWidth}, 76)">
    <rect width="${pillarWidth}" height="34" rx="6" fill="#172554" stroke="#2563eb" stroke-width="1" />
    <text x="${pillarWidth / 2}" y="22" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="13" font-weight="700" fill="#60a5fa" text-anchor="middle" letter-spacing="1.2">${pillarText}</text>
  </g>

  <g transform="translate(64, 175)">
    ${titleSpans}
  </g>

  <g transform="translate(64, ${descY})">
    ${descSpans}
  </g>

  <line x1="64" y1="520" x2="1136" y2="520" stroke="#1e293b" stroke-width="1" />

  <text x="64" y="558" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="15" font-weight="600" fill="#e2e8f0">PT PRISMA DIGITAL KREATIF</text>
  <text x="64" y="580" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="13" fill="#64748b">Verified Engineering Architecture · Failure-Mode Isolation · High-Level Design</text>

  <text x="1136" y="558" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="15" font-weight="700" fill="#60a5fa" text-anchor="end">Muhammad Khoiruzzadittaqwa</text>
  <text x="1136" y="580" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="13" fill="#64748b" text-anchor="end">Wikidata Q141474900 · ORCID 0000-0002-1594-9548</text>
</svg>`;

  const pngBuffer = await sharp(Buffer.from(svg)).png().toBuffer();

  return new Response(pngBuffer, {
    headers: {
      'Content-Type': 'image/png',
      'Cache-Control': 'public, max-age=31536000, immutable',
    },
  });
};
