---
title: "Concurrency"
weight: 7
---

The thread is that of the system. Why has no scheduler: the ceiling stays that of C. The brace that launches waits: the author writes no handle. The channel copies or moves, so that a pointer does not enter another thread's arena.

> A thread is launched with `thread call`. The thread has its stack and its `arena thread`, which dies when its call returns. No goroutine. No growable stack. No scheduling runtime.

> The brace that contains the `thread` waits for it. An `if`, an `else`, an `arena`, a `select` arm and the body of a function are such braces. The body of a `for` is not.

> `chan[T](n)` opens `n` slots. The queue does not grow. `n` zero is a rendezvous: the value is copied, then both continue.

> Copying is `la garde ne se copie pas`. `=` and `return` move it. The source becomes empty. The compiler closes it at the end of the name that holds it. The author does not write `close`.

> `c.send(v)` returns `error`. A full queue blocks. `nil` means `v` entered. `c.receive()` returns `(T, error)`. An empty queue blocks.

> `p := freeze(x)` moves `x`. `freeze` marks the storage. A write that reaches this storage is `freeze`.

> `arena shared name { }` dies at the brace, after waiting for the threads launched inside. `name.make` and `name.append` stay on the thread that opened the block.

> `select` returns an `error`. The first ready arm, in text order, runs. No `default`.

**Diagnostic.** `thread attend un appel` — `thread` without a call. `la garde ne se copie pas` — copying a channel. `garde déplacée` — sending or receiving on an empty name. `le canal reste un nom` — a channel in a field, a slice or a map. `le pointeur ne sort pas` — an argument that does not survive the call. `arène partagée` — passing a shared arena to a `thread`. `select attend un bras` — `select` without an arm. `case hors select` — `case` outside `select`. `alias` — a write to a `freeze` storage that still has a mutable alias.

**Not in this version.** `entree[T](n)` and `sortie[T](n)`. The goroutine. The growable stack. The scheduler.
