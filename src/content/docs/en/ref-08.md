---
title: "Foreign"
weight: 8
---

`extern` is a hand-written signature. Why does not parse C headers. `defer` frees what C allocated, because the arena only frees what it created.

> `extern func` declares a C function, hand-written signature. Why does not free memory allocated by C. `defer` does. No parsed header.

> An `extern` takes and returns `int`, `string` and `[]u8`. Any other type is refused.

> A `string` passed to C is the pointer to the bytes, then their count. Why does not add the null byte.

> A `[]u8` passed to C is the pointer to the bytes, then their count. These bytes survive the call. C writes into them. It does not allocate them.

> A `string` or a `[]u8` returned by C is the pointer to the bytes, then their count. Why makes a value of it. It does not add the null byte and does not attach these bytes to an arena.

**Diagnostic.** `extern attend int, string ou []u8` — a type other than `int`, `string` or `[]u8` in the signature.

## C-Package

A C-package is a directory that binds C to Why. The C is hand-written. Why does not parse headers. The build compiles the C and links it to the binary.

### Layout

| File | Required | Role |
|---|---|---|
| `*.wc` | ✅ | The `extern func` + the Why API (struct, methods, errors) |
| `*.c` | ✅ | The C shim, hand-written |
| `link` | optional | One linker flag per line |
| `data` | optional | Test data for `preuve()` |

The `.c` name follows the domain: `os.c`, `lmdb.c`, `snap.c`. An imported package has no `main`; the proof that has a `main` is the program.

### Type mapping

| Why | C (parameter) | C (return) |
|---|---|---|
| `int` | `intptr_t v_nom` | `intptr_t` |
| `string` | `const uint8_t *v_nom, intptr_t v_nom_n` | `struct why_raw` |
| `[]u8` | `uint8_t *v_nom, intptr_t v_nom_n` | `struct why_raw` |

The C name is `v_` followed by the Why name. The length is `v_` followed by the name and `_n`. A `string` has no null byte; C copies and adds the null if the system requires it.

### The return struct

```c
struct why_raw {
    uint8_t *p;    // pointer to the bytes
    intptr_t n;    // byte count
};
```

C does not return a pointer taken from an argument. It may return a pointer to static memory. Why does not attach these bytes to an arena. C remains the owner.

### Naming

C functions use a domain prefix to avoid collisions with system C. The prefix is short, lowercase, followed by an underscore. It is the same for all functions in the package.

| Why | C |
|---|---|
| `Open` | `os_open` |
| `Read` | `os_read` |
| `Close` | `os_close` |

The C name is the name written in `extern func`. Why does not prefix it.

### Error codes

Error codes are negative. They are defined by the package.

| Code | Meaning | Why |
|---|---|---|
| `-1` | absent | `error("absent")` |
| `-2` | refused | `error("refuse")` |
| `-3` | truncated | `error("coupe")` |
| `-4` | full | `error("plein")` |
| `-5` | closed | `error("ferme")` |

The mapping is done in Why, after each `extern` call:

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

### Build

| Aspect | Rule |
|---|---|
| C standard | `-std=c11 -fwrapv -fno-strict-aliasing -O2` |
| C++ standard | `-std=c++17` (`.cc`, `.cpp`, `.cxx` files) |
| Compiler | `CC` or `cc` (C); `CXX` or `c++` (C++) |
| Link | Flags from the `link` file, one per line |
| Library | Package with sidecars but no `main` → `.o` |
| Import | `import` recompiles the imported package's `.c` into the host binary |

`.cc`, `.cpp`, `.cxx` files must use `extern "C"` on their functions, otherwise the name is mangled and linking fails.

### Memory

- C owns its memory.
- Why does not attach C memory to an arena.
- `defer` can call a C cleanup function.
- No hidden allocations.

### Reference

The full specification is in `c-paquet.md` at the repo root. The author's guide is in [C-Package](c-paquet.md).
