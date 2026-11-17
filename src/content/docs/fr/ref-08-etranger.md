---
title: "Étranger"
weight: 8
---

# Étranger

`extern` est une signature écrite à la main. Why ne parse pas les en-têtes du C. `defer` rend ce que C a alloué, parce que l'arène ne libère que ce qu'elle a créé.

> `extern func` déclare une fonction C, signature écrite à la main. Why ne libère pas la mémoire allouée par C. `defer` le fait. Pas d'en-hête parsé.

> Un `extern` prend et rend `int`, `string` et `[]u8`. Un autre type est refusé.

> Une `string` passée à C est le pointeur des octets, puis leur nombre. Why n'ajoute pas l'octet nul.

> Un `[]u8` passé à C est le pointeur des octets, puis leur nombre. Ces octets survivent à l'appel. C écrit dedans. Il ne les alloue pas.

> Une `string` ou un `[]u8` rendu par C est le pointeur des octets, puis leur nombre. Why en fait une valeur. Il n'ajoute pas l'octet nul et ne rattache pas ces octets à une arène.

**Diagnostic.** `extern attend int, string ou []u8` — un type autre que `int`, `string` ou `[]u8` dans la signature.
