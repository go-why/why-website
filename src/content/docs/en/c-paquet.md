---
title: "C-Package"
weight: 25
---

# C-Package — Author's Guide

Building a C-package is a copy-paste. The template provides the structure; you write the shim.

## Start

```sh
cp -r templates/c-paquet my-package
cd my-package
```

## Step 1 — Rename

The `ex_` prefix in the template is an example. Replace it with your domain:

| Domain | Prefix | C file |
|---|---|---|
| system | `os_` | `os.c` |
| LMDB | `lmdb_` | `lmdb.c` |
| snapshot | `snap_` | `snap.c` |

Rename the functions in `shim.c` and in the `extern func` declarations in `main.wc`.

## Step 2 — Write the C shim

The shim is the bridge between Why and the system. Each function follows the same pattern:

```c
// os.c — prefix os_

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
    if (v_nom_n >= 256) return -2; // refused
    memcpy(nom, v_nom, (size_t)v_nom_n);
    nom[v_nom_n] = '\0';

    int fd = open(nom, O_RDONLY);
    if (fd < 0) return -1; // absent
    return fd;
}

// extern func os_close(h int) int
intptr_t os_close(intptr_t v_h) {
    if (close((int)v_h) < 0) return -5; // closed
    return 0;
}

// extern func os_lire(h int, buf []u8) int
intptr_t os_lire(intptr_t v_h, uint8_t *v_buf, intptr_t v_buf_n) {
    ssize_t r = read((int)v_h, v_buf, (size_t)v_buf_n);
    if (r < 0) return -3; // truncated
    return (intptr_t)r;
}
```

### Shim rules

1. **The C name** is exactly the name in `extern func`. Why does not prefix it.
2. **Parameters** follow the pattern `v_nom` (value) and `v_nom_n` (length).
3. **Return `int`** is an `intptr_t`. Negative = error, positive or zero = value.
4. **Return `string`/`[]u8`** is a `struct why_raw`. C remains the owner of the memory.
5. **No hidden allocations.** If the shim allocates, it must say so in the name.

## Step 3 — Write the Why API

The `main.wc` file wraps the shim in a clean Why API:

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

### Error pattern

Each `extern` call is followed by a mapping of the negative codes:

```
h := os_open(nom)
if h == -4 {
  return error("plein")
}
if h < 0 {
  return error("absent")
}
```

The most specific code first, then the catch-all `h < 0`.

## Step 4 — Link (if needed)

If your shim depends on an external C library, fill in the `link` file:

```
-L/usr/local/lib
-lmdb
-I/usr/local/include
```

One flag per line. The flags are passed to the compiler and linker in order.

## Step 5 — Build and run

```sh
why build .
./my-package.wo
```

Exit code `0` means success. Any other code is an error.

## Full example: counter

A C counter with state, a Why wrapper, and a proof.

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

## Verify

The template and the three examples in `testdata/` pass the test suite:

```sh
go test ./internal/build/ -run TestPrograms
```

The three test packages:

| Package | What it covers |
|---|---|
| `c-paquet-compteur` | C state, Why wrapper, proof |
| `c-paquet-multi` | Multiple C files in one package |
| `c-paquet-chaine` | `string`/`[]u8` mutation by C |

## Reference

The full specification is in `c-paquet.md` at the repo root. The language reference is in [Foreign](ref-08.md).
