---
title: "Paquet C"
weight: 25
---

# Paquet C — Guide de l'auteur

Construire un paquet C est un copier-coller. Le template fournit la structure ; vous écrivez la shim.

## Démarrer

```sh
cp -r templates/c-paquet mon-paquet
cd mon-paquet
```

## Étape 1 — Renommer

Le préfixe `ex_` dans le template est un exemple. Remplacez-le par votre domaine :

| Domaine | Préfixe | Fichier C |
|---|---|---|
| système | `os_` | `os.c` |
| LMDB | `lmdb_` | `lmdb.c` |
| snapshot | `snap_` | `snap.c` |

Renommez les fonctions dans `shim.c` et dans les `extern func` de `main.wc`.

## Étape 2 — Écrire la shim C

La shim est le pont entre Why et le système. Chaque fonction suit le même pattern :

```c
// os.c — préfixe os_

#include <stdint.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>

struct why_raw {
    uint8_t *p;
    intptr_t n;
};

// extern func os_open(nom string) int
intptr_t os_open(const uint8_t *v_nom, intptr_t v_nom_n) {
    char nom[256];
    if (v_nom_n >= 256) return -2; // refuse
    memcpy(nom, v_nom, (size_t)v_nom_n);
    nom[v_nom_n] = '\0';

    int fd = open(nom, O_RDONLY);
    if (fd < 0) return -1; // absent
    return fd;
}

// extern func os_close(h int) int
intptr_t os_close(intptr_t v_h) {
    if (close((int)v_h) < 0) return -5; // ferme
    return 0;
}

// extern func os_lire(h int, buf []u8) int
intptr_t os_lire(intptr_t v_h, uint8_t *v_buf, intptr_t v_buf_n) {
    ssize_t r = read((int)v_h, v_buf, (size_t)v_buf_n);
    if (r < 0) return -3; // coupe
    return (intptr_t)r;
}
```

### Règles de la shim

1. **Le nom C** est exactement le nom dans `extern func`. Why ne préfixe pas.
2. **Les paramètres** suivent le pattern `v_nom` (valeur) et `v_nom_n` (longueur).
3. **Le retour `int`** est un `intptr_t`. Négatif = erreur, positif ou zéro = valeur.
4. **Le retour `string`/`[]u8`** est un `struct why_raw`. Le C reste propriétaire de la mémoire.
5. **Pas d'allocation cachée.** Si la shim alloue, elle doit le dire dans le nom.

## Étape 3 — Écrire l'API Why

Le fichier `main.wc` enveloppe la shim dans une API Why propre :

```
// main.wc

extern func os_open(nom string) int
extern func os_close(h int) int
extern func os_lire(h int, buf []u8) int

struct Fichier { fd int }

func Ouvrir(nom string) (Fichier, error) {
  fd := os_open(nom)
  if fd == -2 {
    return error("refuse")
  }
  if fd < 0 {
    return error("absent")
  }
  f := Fichier
  f.fd = fd
  return f
}

func (me *Fichier) Fermer() error {
  if os_close(me.fd) < 0 {
    return error("ferme")
  }
  return nil
}

func (me *Fichier) Lire(buf []u8) (int, error) {
  n := os_lire(me.fd, buf)
  if n == -3 {
    return error("coupe")
  }
  if n < 0 {
    return error("refuse")
  }
  return n
}

func main() {
  f := Ouvrir("donnees.txt") or return
  defer f.Fermer()
  arena a {
    buf := a.make([]u8, 256)
    n := f.Lire(buf) or return
    afficher(n)
  }
}
```

### Pattern d'erreur

Chaque appel `extern` est suivi d'un mapping des codes négatifs :

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

## Étape 4 — Lien (si nécessaire)

Si votre shim dépend d'une bibliothèque C externe, remplissez le fichier `link` :

```
-L/usr/local/lib
-lmdb
-I/usr/local/include
```

Un drapeau par ligne. Les drapeaux sont passés au compilateur et au linker dans l'ordre.

## Étape 5 — Builder et exécuter

```sh
why build .
./mon-paquet.wo
```

Le code de sortie `0` signifie succès. Tout autre code est une erreur.

## Exemple complet : compteur

Un compteur C avec état, wrapper Why, et épreuve.

### `compteur.c`

```c
#include <stdint.h>

static int next_id = 1;

intptr_t cp_nouveau(void) {
    return next_id++;
}

intptr_t cp_incr(intptr_t v_id) {
    return v_id + 1;
}

intptr_t cp_val(intptr_t v_id) {
    return v_id;
}
```

### `main.wc`

```
extern func cp_nouveau() int
extern func cp_incr(id int) int
extern func cp_val(id int) int

struct Compteur { id int }

func Nouveau() Compteur {
  c := Compteur
  c.id = cp_nouveau()
  return c
}

func (me *Compteur) Incr() int {
  me.id = cp_incr(me.id)
  return me.id
}

func (me *Compteur) Val() int {
  return cp_val(me.id)
}

func preuve() error {
  c := Nouveau()
  c.Incr()
  c.Incr()
  if c.Val() != 3 {
    return error("non")
  }
  return nil
}

func main() {
  if preuve() != nil {
    return
  }
}
```

## Vérifier

Le template et les trois exemples de `testdata/` passent la suite de tests :

```sh
go test ./internal/build/ -run TestPrograms
```

Les trois paquets de test :

| Paquet | Ce qu'il couvre |
|---|---|
| `c-paquet-compteur` | État C, wrapper Why, épreuve |
| `c-paquet-multi` | Plusieurs fichiers C dans un paquet |
| `c-paquet-chaine` | Mutation de `string`/`[]u8` par C |

## Référence

La spécification complète est dans `c-paquet.md` à la racine du repo. La référence du langage est dans [Étranger](ref-08-etranger.md).
