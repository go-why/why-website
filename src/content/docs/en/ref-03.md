---
title: "Memory"
weight: 3
---

The `arena` block is the added idea. The author names the brace that is the death; he does not write `free`. The stack, the block and `arena thread` are the three deaths one can point to.

> The block `arena name { … }` creates an arena. Everything allocated in the block dies at the close of the brace. The author does not free. The compiler inserts the release.

```
func main() int {
  arena tab {
    xs := tab.make([]int, 3)
    xs[0] = 10
    xs[1] = 20
    xs[2] = 12
    return xs[0] + xs[1] + xs[2]
  }
}
```

The literal `[]T{…}` lives in the `arena name` block and dies with it. Without that block, including in `arena thread`, it is the call stack. A slice born there does not leave the call.

> `defer` will run the call at the exit of the block, before the release of the arena. It frees what C allocated, because the arena only frees what it created.

> `arena thread` launches a thread. The brace waits for the thread before the release. The thread has its own stack.

> `arena shared name { … }` is an arena that two threads read by `freeze` or by channel. `name.make` and `name.append` stay on the thread that opened the block.

**Diagnostic.** `arène partagée` — passing a shared arena to a `thread`.

**Not in this version.** A destructor written by the author. A garbage collector. A borrow checker.
