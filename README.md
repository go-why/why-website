# Site de documentation Why — variante Astro

Deuxième site de documentation du langage **Why**, construit en **Astro**, pour **comparer** avec le site **Hugo** existant (`../site/`). Même contenu bilingue (FR / EN), même feuille de style : seul le moteur change, pour que la comparaison soit juste.

Le site Hugo reste intact ; ce dossier `site-astro/` est autonome.

## Pourquoi un second site ?

Le site Hugo souffre d'un **bug connu de Hugo multilingue** : les **enfants d'un « branch bundle »** (un dossier avec un `index.md`) ne se rendent pas. Résultat, les 10 pages `ref/01..10` (Lexique, Valeurs, Mémoire, …) **disparaissent** du build Hugo (5 pages/langue seulement).

Astro ne connaît pas cette limitation : ici les **15 pages/langue** sont bien rendues, et l'arborescence de la référence a été **aplatie** (`ref.md` + `ref-01…ref-10.md`) pour rester propre et éviter l'ambiguïté dossier/frère.

## `dist/` est le dossier de build ?

**Oui.** `site-astro/dist/` est la **sortie de build** d'Astro (HTML/CSS statique : `index.html`, `fr/`, `en/`, `css/`). Il est régénéré à chaque `npm run build` et **ne doit pas être commité** (hors git, voir `.gitignore`). De même, `.astro/` (cache) et `node_modules/` sont des artefacts à ignorer.

## Arborescence

```
site-astro/
├── astro.config.mjs       # i18n : fr (défaut) + en, préfixé → /fr/… /en/…
├── content.config.ts      # collection « docs » : front matter typé (title, weight)
├── package.json           # scripts dev / build / preview
├── tsconfig.json
├── src/
│   ├── styles.css         # CSS réutilisé depuis le site Hugo (static/css/site.css)
│   ├── content.config.ts
│   ├── content/docs/
│   │   ├── fr/            # FR — index, spec, lib, perf, ref, ref-01…ref-10 (à plat)
│   │   └── en/            # EN — même structure
│   ├── layouts/Doc.astro  # layout : header (bascule langue), nav (par weight), footer
│   └── pages/
│       ├── index.astro    # racine → redirige vers /fr/
│       ├── fr/index.astro # accueil FR
│       ├── fr/[...slug].astro
│       ├── en/index.astro
│       └── en/[...slug].astro
├── public/                # (vide) assets publics statiques
└── dist/                  # ⚠ SORTIE DE BUILD — non commitée
```

## Modèle de contenu

- **Contenu inliné** dans `src/content/docs/{fr,en}/*.md` (copié depuis la racine du repo + `site/content/` Hugo pour la parité). C'est volontairement un snapshot fiable, pas un chargeur en direct.
  - FR canonique : `README.md` (accueil), `why.md` (spec), `lib-spec.md` (lib), `ref/` (référence) à la racine, + `perf` depuis `site/content/fr/perf/`.
  - EN : copié depuis `site/content/en/`.
  - **Référence aplatie** : `ref.md` (index) + `ref-01…ref-10*.md` (en FR : `ref-01-lexique.md` … `ref-10-document.md`).
- **Front matter** : `title` + `weight` (ordonne la nav, comme Hugo).
- **Nav** : `spec` → `ref` (+ 10 enfants) → `lib` → `perf`, ordre par `weight`.

## Utiliser le site

### Prérequis
- Node ≥ 18 (ici : Node 26 / npm 11). Réseau pour `npm install` une première fois.

### Commandes courtes

```bash
cd site-astro

npm install          # première fois (installe Astro)
npm run dev          # serveur de dev + live-reload (http://localhost:4321/fr/)
npm run build        # build statique → dist/
npm run preview      # sert le build (dist/)
```

### Ouvrir le résultat

- Serveur de dev : http://localhost:4321/fr/ — FR par défaut, bascule EN en haut à droite.
- Ou le build statique directement : `open dist/index.html` (redirige vers `/fr/`).

## Comparaison Hugo ↔ Astro

| Critère | Hugo (`../site/`) | Astro (`site-astro/`) |
| --- | --- | --- |
| Pages FR | **5** (les 10 `ref/01..10` perdues) | **15** (toutes rendues) |
| Pages EN | **5** | **15** |
| Cause | bug branch-bundle multilingue Hugo 0.169 | pas de limitation équivalente |
| Build | `hugo` → `public/` | `npm run build` → `dist/` |
| Arborescence ref | `ref/01..10` (dossier, cassée) | `ref.md` + `ref-01…10` (à plat) |
| CSS | `static/css/site.css` | réutilisé (`src/styles.css`) |

> Verdict : pour ce contenu, Astro rend **tout** là où Hugo en **perd** la moitié de la référence.
> Le choix reste à arbitrer (Hugo = écosystème/maturité, Astro = DX moderne + pas de ce bug).

## Build propre & git

- Ne pas committer : `site-astro/dist/`, `site-astro/.astro/`, `site-astro/node_modules/`.
- Vérification : `git status --short site-astro/` ne doit lister que le contenu source (jamais `dist/`, `.astro/`, `node_modules/`).
