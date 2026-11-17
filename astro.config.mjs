import { defineConfig } from 'astro/config';

// Site de comparaison Astro — même contenu que le site Hugo (../site).
// i18n fr (défaut) + en, préfixé, pour des URLs identiques: /fr/... /en/...
export default defineConfig({
  site: 'http://localhost:4321',
  i18n: {
    defaultLocale: 'fr',
    locales: ['fr', 'en'],
    routing: { prefixDefaultLocale: true },
  },
});
