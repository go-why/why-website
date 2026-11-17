---
title: "Document"
weight: 10
---

A `.oo` document is a possibility. SemCards, the prototype, may use it. The card has a name, a prototype, slots, methods. It is not Why: `arena` is not a word of `.oo`.

> A `.oo` file is a sequence of objects. The indentation is the block. `//` comments to the end of the line. The image loaded at boot is the copy. The file remains the truth. The program does not create an object, does not free one, and does not inspect itself.

```
object Stack : Part
  qty: 0
  value: 0
  on take (q):
    me.moved = 0
    if me.qty > 0:
      me.moved = me.value * q / me.qty
    me.value = me.value - me.moved
    me.qty = me.qty - q

object MillIn : Stack
  qty: 2000000
  value: 16320
```

> An object has a name, an optional prototype, slots and methods. `object MillIn : Stack` reads `qty` on `Stack` until `MillIn` writes it. The write always falls on the receiver.

> A method is `on name (params):`. There is no function, no `return`. The value of the method is the last value computed.

> The values are `nothing`, `true`, `false`, the integer, the text, the list, the object, the canvas.

> The list is the only aggregate. `[a, b]`. `add`, `remove`, `length`, `at`. `for x in liste:` copies the list before walking.

> The canvas is not built by the program. The host passes it to `draw`. The methods (`rect`, `text`, `frame`, `hit`, `chrome`, `card`) record orders the host replays. They return `nothing`.

> An error is a host fault: absent slot, wrong number of arguments, division by zero, call deeper than 48. The program does not catch it.

**Diagnostic.** `slot absent` — reading a slot that does not exist. `arguments : n` — wrong number of arguments. `division par zéro` — dividing by zero. `profondeur` — a call deeper than 48.

**Not in this version.** The pointer, the allocation, the concurrency, the class, the generic in a document.
