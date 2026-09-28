import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import sitemap from '@astrojs/sitemap';
export default defineConfig({
  site: 'https://zadevpenseo.github.io',
  base: '/',
  trailingSlash: 'always',
  prefetch: {
    prefetchAll: true,
    defaultStrategy: 'hover',
  },
  build: {
    inlineStylesheets: 'auto',
  },
  integrations: [
    starlight({
      title: 'Zadit // Systems & Blueprints',
      description: 'Zadit | Web Dev Design · SEO · Writer · Data Analysis. Verified case studies, high-level architectures, and executable prototypes by Muhammad Khoiruzzadittaqwa.',
      defaultLocale: 'root',
      locales: {
        root: {
          label: 'English',
          lang: 'en',
        },
      },
      social: {
        github: 'https://github.com/zadevpenseo/zadevpenseo.github.io',
      },
      customCss: ['./src/styles/tokens.css', './src/styles/starlight.css'],
      components: {
        Header: './src/components/overrides/Header.astro',
        Footer: './src/components/overrides/Footer.astro',
        PageTitle: './src/components/overrides/PageTitle.astro',
        ThemeSelect: './src/components/overrides/ThemeSelect.astro',
        Head: './src/components/overrides/Head.astro',
      },
      tableOfContents: {
        minHeadingLevel: 2,
        maxHeadingLevel: 4,
      },
      sidebar: [
        {
          label: '1. Hub & Architecture',
          items: [
            { label: 'Master Case Studies Vault', link: '/case-studies/' },
            { label: '3-Tier Proof Methodology', link: '/case-studies/methodology/' },
          ],
        },
        {
          label: '2. Web Dev Design',
          items: [
            { label: 'Pillar Overview', link: '/case-studies/web-dev-design/' },
            { label: 'Gworky Edge Next.js Flagship', link: '/case-studies/web-dev-design/gworky-edge-web-app/' },
            { label: 'WooCommerce Platform Optimization', link: '/case-studies/web-dev-design/woocommerce-enhancement-659829/' },
            { label: 'DevPDF.in Engine & Conversion Architecture', link: '/case-studies/web-dev-design/pdf-tools-devpdf-repair-658700/' },
            { label: 'Interactive Web Audio & Canvas Engine', link: '/case-studies/web-dev-design/interactive-birthday-card-web-656043/' },
            { label: 'High-Performance Animated Landing Engine', link: '/case-studies/web-dev-design/animated-landing-page-659928/' },
            { label: 'Modular Fullstack Web Architecture', link: '/case-studies/web-dev-design/fullstack-custom-web-apps-659861/' },
            { label: 'Elementor JSON UI Architecture Engine', link: '/case-studies/web-dev-design/elementor-json-ui-engine/' },
          ],
        },
        {
          label: '3. SEO',
          items: [
            { label: 'Pillar Overview', link: '/case-studies/seo/' },
            { label: 'Programmatic SEO Edge Scale Engine', link: '/case-studies/seo/programmatic-seo-scale-engine/' },
            { label: 'Technical SEO & GA4 Audit (Vidio/Tirto)', link: '/case-studies/seo/technical-seo-vidio-tirto-audit/' },
            { label: 'National SEO Competition Award (WOM)', link: '/case-studies/seo/national-seo-competition-wom-finance/' },
            { label: 'Entity Knowledge Graph (Wikidata Tri-Node)', link: '/case-studies/seo/knowledge-graph-entity-architecture/' },
          ],
        },
        {
          label: '4. Writer',
          items: [
            { label: 'Pillar Overview', link: '/case-studies/writer/' },
            { label: 'Short-Form Script & Retention Engine', link: '/case-studies/writer/short-form-video-script-engine/' },
            { label: 'Executive Pitch Decks (JCG Partnership)', link: '/case-studies/writer/executive-pitch-decks-jcg-partnership/' },
            { label: 'Business Feasibility & Financial Models', link: '/case-studies/writer/business-feasibility-financial-models/' },
            { label: 'Peer-Reviewed Empirical Research (APA 7th)', link: '/case-studies/writer/peer-reviewed-empirical-publishing/' },
            { label: 'Cinematic 3D Direction & Narrative', link: '/case-studies/writer/cinematic-3d-birthday-video-659866/' },
          ],
        },
        {
          label: '5. Data Analysis',
          items: [
            { label: 'Pillar Overview', link: '/case-studies/data-analysis/' },
            { label: 'Enterprise Power BI & Power Query ETL', link: '/case-studies/data-analysis/power-bi-power-query-etl-650821/' },
            { label: 'Mathematical Modeling & Statistics (140 SKS)', link: '/case-studies/data-analysis/mathematical-modeling-and-statistics/' },
            { label: 'Psychometric & Survey Validation (Rasch/Aiken)', link: '/case-studies/data-analysis/psychometric-survey-validation-rasch/' },
            { label: 'Resilient CDP WebSocket Scraping Engine', link: '/case-studies/data-analysis/resilient-cdp-websocket-scraping/' },
            { label: 'Morpheus V2 Financial Simulation Model', link: '/case-studies/data-analysis/morpheus-v2-tax-simulation-659758/' },
            { label: 'DocuMorph PDF & Table Extraction Pipeline', link: '/case-studies/data-analysis/documorph-pdf-table-extraction/' },
            { label: 'Automated Jira Weekly Performance Pipeline', link: '/case-studies/data-analysis/jira-weekly-report-automation-40725359/' },
          ],
        },
      ],
      head: [
        {
          tag: 'meta',
          attrs: {
            name: 'author',
            content: 'Muhammad Khoiruzzadittaqwa (Zadit) - zadevpenseo',
          },
        },
        {
          tag: 'meta',
          attrs: {
            name: 'theme-color',
            content: '#0d0b10',
          },
        },
        {
          tag: 'meta',
          attrs: {
            name: 'apple-mobile-web-app-capable',
            content: 'yes',
          },
        },
        {
          tag: 'meta',
          attrs: {
            name: 'apple-mobile-web-app-status-bar-style',
            content: 'black-translucent',
          },
        },
        {
          tag: 'link',
          attrs: {
            rel: 'manifest',
            href: '/site.webmanifest',
          },
        },
        // DNS Prefetch & Preconnect for Google Fonts
        {
          tag: 'link',
          attrs: { rel: 'dns-prefetch', href: 'https://fonts.googleapis.com' },
        },
        {
          tag: 'link',
          attrs: { rel: 'dns-prefetch', href: 'https://fonts.gstatic.com' },
        },
        {
          tag: 'link',
          attrs: { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        },
        {
          tag: 'link',
          attrs: { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
        },
        {
          tag: 'link',
          attrs: {
            rel: 'stylesheet',
            href: 'https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap',
          },
        },
      ],
    }),
    sitemap({
      filter: (page) => !page.includes('/404'),
    }),
  ],
});
