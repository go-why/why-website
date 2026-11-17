---
title: "Produit"
weight: 9
---

# Produit

Le `.wo` est un binaire natif, sans runtime Why. `why run` sur un répertoire compile et lance. `why run monde.oo` passe un document au `.wo` déjà là. Éditer ce fichier ne recompile pas le programme.

> `why build [répertoire]` lit les `.wc` d'un répertoire et écrit un `.wo`. Sans `main`, le `.wo` est une lib. Avec `main`, c'est un binaire. Un binaire peut lier des libs `.wo`. Le format est un seul fichier, sans runtime Why. Les arènes sont des appels insérés par le compilateur, pas une bibliothèque dynamique.

> `why run [répertoire]` écrit le même `.wo` que `why build`, puis le lance. Le code de sortie est le sien.

> `why run monde.oo` charge le `.wo` courant et lui passe le document. Il ne compile pas. Le chemin du document est l'argument du processus.

```
why build testdata/arith
why run testdata/arith
```

> `why play` sert une page locale. Chaque page est un fragment avec un `main` ; le résultat est le code de sortie, ou le diagnostic.

> Le `.oo` n'est pas lié dans le `.wo`. Le remplacer ne recompile pas le programme.

**Diagnostic.** `il manque le .wo` — `why run monde.oo` sans `.wo` dans le répertoire courant. `document absent` — le fichier `.oo` n'existe pas.

**État.** Compilé : fonctions, structs, méthodes, interfaces, tranches, maps, `arena`, `arena thread`, `defer`, `error`, `or return`, pointeur stocké, garde, génériques, `thread appel`, `chan[T](n)`, `for v in c`, `select`, `freeze`, `arena shared`, `import`, `+=` et la même famille.

**Pas encore compilé.** Le document `.oo` comme cible de `why build`.
