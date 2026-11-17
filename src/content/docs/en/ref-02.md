---
title: "Values"
weight: 2
---

A single number, the machine-word integer. `string` is bytes, not Unicode text. The header of a slice or a map carries its arena, so that the life of the bytes has a name.

> | Kind | Note |
> |---|---|
> | `nil` | Absence. Only inhabitant of `error` without error. |
> | `bool` | `true`, `false`. |
> | `int` | Signed machine-word integer. Only number. |
> | `u8` | Byte. For buffers. |
> | `string` | Immutable bytes, known length. Not Unicode text. |
> | `error` | A value. Compared with `==`. Not an exception. |
> | struct | Value, copied on assignment. |
> | `*T` | Pointer to a `T` living in a visible arena. |
> | `[]T` | Slice: pointer, length, owning arena. |
> | `map[K]V` | Map. Same header as the slice. |
> | `chan[T]` | Bounded queue. Guard. A name. |
> | `entree[T]` | Write end. Copied. Born empty. |
> | `sortie[T]` | Read end. Copied. Born empty. |
> | interface | Pointer to the value, pointer to the vtable. |
> | `Id` | Index in a document table. Not a pointer. |

```
func somme(a, b int) int {
  return a + b
}

func main() int {
  q := 7 / 2
  r := 7 % 2
  u := 10 + (0 - 3)
  z := 10 + (0 - 7) / 2
  return somme(q, r) + u + z
}
```

`/` and `%` truncate toward zero. `-n` is the unary. `0 - n` is allowed. Operands evaluate left to right.

> `==` requires two values of the same kind. `!=`, `<`, `>`, `<=`, `>=` are the signs of C. `<`, `>`, `<=`, `>=` compare two integers. `&&` and `||` short-circuit.

> `if` takes a boolean. The block runs when it is true. `else` is the other block, on the same line as `}`. `else if` chains.

```
func main() int {
  n := 3
  if n > 1 {
    n = n + 39
  }
  return n
}
```

> `for` repeats the block while the boolean is true. The step is a statement of the body. No `break`.

> `for x in xs` copies the slice before the first turn. `x` is the element, a name of the body. `for i, x in xs` also binds the index before the element.

> `x[i]` reads. `i` is an `int`. The element of a slice has the type `T`. The element of a string is a `u8`. `len(x)` returns an `int`.

**Diagnostic.** `indice hors table` — an index outside `0 .. len-1`, including negative.

> `map[K]V` is a map. `K` is an `int` or a `string`. `m[k]` reads. `m[k] = v` writes a key already present. An absent key is a host fault. The map does not grow.

> `x = y` copies the value. `x` is a variable or a field. `x += y` is `x = x + y`. The same family: `-=`, `*=`, `/=`, `%=`.

> `p := *T` is the null pointer. `*p` reads. `*p = v` writes. Reading or writing the null pointer is the fault `pointeur nul`.

**Diagnostic.** `pointeur nul` — reading or writing the null pointer.

**Not in this version.** `**T`, or a pointer to a slice, a map, a string, an error or an interface. No float.
