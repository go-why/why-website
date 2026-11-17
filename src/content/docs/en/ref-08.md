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
