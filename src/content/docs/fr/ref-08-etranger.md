---
title: "Étranger"
weight: 8
---

# Étranger

`extern` est une signature écrite à la main. Why ne parse pas les en-têtes du C. `defer` rend ce que C a alloué, parce que l'arène ne libère que ce qu'elle a créé.

> `extern func` déclare une fonction C, signature écrite à la main. Why ne libère pas la mémoire allouée par C. `defer` le fait. Pas d'en-tête parsé.

> Un `extern` prend et rend `int`, `string` et `[]u8`. Un autre type est refusé.

> Une `string` passée à C est le pointeur des octets, puis leur nombre. Why n'ajoute pas l'octet nul.

> Un `[]u8` passé à C est le pointeur des octets, puis leur nombre. Ces octets survivent à l'appel. C écrit dedans. Il ne les alloue pas.

> Une `string` ou un `[]u8` rendu par C est le pointeur des octets, puis leur nombre. Why en fait une valeur. Il n'ajoute pas l'octet nul et ne rattache pas ces octets à une arène.

**Diagnostic.** `extern attend int, string ou []u8` — un type autre que `int`, `string` ou `[]u8` dans la signature.

## Paquet C

Un paquet C est un répertoire qui lie du C à du Why. Le C est écrit à la main. Why ne parse pas les en-têtes. Le build compile le C et le lie au binaire.

### Layout

| Fichier | Requis | Rôle |
|---|---|---|
| `*.wc` | ✅ | Les `extern func` + l'API Why (struct, méthodes, erreurs) |
| `*.c` | ✅ | La shim C, écrite à la main |
| `link` | optionnel | Un drapeau de lien par ligne |
| `data` | optionnel | Données de test pour `preuve()` |

Le nom du `.c` suit le domaine : `os.c`, `lmdb.c`, `snap.c`. Un paquet importé n'a pas de `main` ; l'épreuve qui a un `main` est le programme.

### Correspondance des types

| Why | C (paramètre) | C (retour) |
|---|---|---|
| `int` | `intptr_t v_nom` | `intptr_t` |
| `string` | `const uint8_t *v_nom, intptr_t v_nom_n` | `struct why_raw` |
| `[]u8` | `uint8_t *v_nom, intptr_t v_nom_n` | `struct why_raw` |

Le nom C est `v_` suivi du nom Why. La longueur est `v_` suivi du nom et de `_n`. Une `string` n'a pas d'octet nul ; le C copie et ajoute le nul si le système l'exige.

### Le struct de retour

```c
struct why_raw {
    uint8_t *p;    // pointeur vers les octets
    intptr_t n;    // nombre d'octets
};
```

Le C ne rend pas un pointeur pris sur un argument. Il peut rendre un pointeur vers la mémoire statique. Why ne rattache pas ces octets à une arène. Le C reste propriétaire.

### Nommage

Les fonctions C ont un préfixe domaine pour éviter la collision avec le C système. Le préfixe est court, en bas de casse, suivi d'un underscore. Il est le même pour toutes les fonctions du paquet.

| Why | C |
|---|---|
| `Open` | `os_open` |
| `Read` | `os_read` |
| `Close` | `os_close` |

Le nom C est le nom écrit dans `extern func`. Why ne le préfixe pas.

### Codes d'erreur

Les codes d'erreur sont négatifs. Ils sont définis par le paquet.

| Code | Sens | Why |
|---|---|---|
| `-1` | absent | `error("absent")` |
| `-2` | refuse | `error("refuse")` |
| `-3` | coupe | `error("coupe")` |
| `-4` | plein | `error("plein")` |
| `-5` | ferme | `error("ferme")` |

Le mapping est fait dans le Why, après chaque appel `extern` :

```
h := os_open(nom)
if h == -4 {
  return error("plein")
}
if h < 0 {
  return error("absent")
}
```

Le code le plus spécifique d'abord, puis la catch-all `h < 0`.

### Build

| Aspect | Règle |
|---|---|
| Standard C | `-std=c11 -fwrapv -fno-strict-aliasing -O2` |
| Standard C++ | `-std=c++17` (fichiers `.cc`, `.cpp`, `.cxx`) |
| Compilateur | `CC` ou `cc` (C) ; `CXX` ou `c++` (C++) |
| Lien | Drapeaux du fichier `link`, un par ligne |
| Bibliothèque | Paquet avec sidecars mais sans `main` → `.o` |
| Import | `import` recompile les `.c` du paquet importé dans le binaire hôte |

Les fichiers `.cc`, `.cpp`, `.cxx` doivent porter `extern "C"` sur leurs fonctions, sinon le nom est mangé et le lien échoue.

### Mémoire

- Le C est propriétaire de sa mémoire.
- Why ne rattache pas la mémoire C à une arène.
- `defer` peut appeler une fonction C de nettoyage.
- Pas d'allocation cachée.

### Référence

La spécification complète est dans `c-paquet.md` à la racine du repo. Le guide de l'auteur est dans [Paquet C](c-paquet.md).
