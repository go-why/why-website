---
title: "Functions and methods"
weight: 4
---

A single form, `func`. The method is that form with a receiver `me`. `or return` propagates the error, instead of a comparison after each call.

> `x = y` copies the value. `x` is a variable or a field. `x += y` is `x = x + y`. The same family: `-=`, `*=`, `/=`, `%=`.

> `x.m(...)` calls the method `m` of the type of `x`. `me` has the type `T` or `*T`, where `T` is the type of `x`. If `me` is a `*T` and `x` is a value `T`, the call passes the address of `x`. There is no `&` operator.

```
struct Compteur { n int }

func (me *Compteur) incrementer() {
  me.n = me.n + 1
}

func main() int {
  c := Compteur
  c.incrementer()
  c.incrementer()
  return c.n
}
```

> `nom := Type` declares the zero value of `Type`. A zero `int` is 0. A zero `bool` is `false`. A zero struct has its fields to zero.

> `or return` propagates an error. `or` is not a boolean operator.

```
func bon() error {
  return nil
}

func main() int {
  if bon() != nil {
    return 1
  }
  return 0
}
```

> A parameter may carry the name of a field: the field is written `me.nom`.

**Diagnostic.** `s'appelle me` — the receiver must be named `me`.

**Not in this version.** Name overloading (several `func f()` with different signatures).
