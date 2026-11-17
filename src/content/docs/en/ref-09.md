---
title: "Product"
weight: 9
---

The `.wo` is a native binary, without a Why runtime. `why run` on a directory compiles and runs. `why run monde.oo` passes a document to the `.wo` already there. Editing that file does not recompile the program.

> `why build [directory]` reads the `.wc` of a directory and writes a `.wo`. Without `main`, the `.wo` is a lib. With `main`, it is a binary. A binary can link `.wo` libs. The format is a single file, without a Why runtime. The arenas are calls inserted by the compiler, not a dynamic library.

> `why run [directory]` writes the same `.wo` as `why build`, then runs it. The exit code is its own.

> `why run monde.oo` loads the current `.wo` and passes it the document. It does not compile. The path of the document is the argument of the process.

```
why build testdata/arith
why run testdata/arith
```

> `why play` serves a local page. Each page is a fragment with a `main`; the result is the exit code, or the diagnostic.

> The `.oo` is not linked in the `.wo`. Replacing it does not recompile the program.

**Diagnostic.** `il manque le .wo` — `why run monde.oo` without a `.wo` in the current directory. `document absent` — the `.oo` file does not exist.

**State.** Compiled: functions, structs, methods, interfaces, slices, maps, `arena`, `arena thread`, `defer`, `error`, `or return`, stored pointer, guard, generics, `thread call`, `chan[T](n)`, `for v in c`, `select`, `freeze`, `arena shared`, `import`, `+=` and the same family.

**Not yet compiled.** The `.oo` document as a target of `why build`.
