---
title: "Errors"
weight: 6
---

`error` is a value; it comes back with the result. `or return` propagates it. A host fault stops the process: it is not an error the program catches.

> `error` is a type. `nil` means no error. `nil` is its zero value. `e := error` is `nil`. An error is created with `error("solde")`. `error("")` is `nil`.

> It is compared with `==`. `error("solde") == error("solde")` is true. `error("solde") == nil` is false.

```
func bon() error {
  return nil
}

func solde() error {
  return error("solde")
}

func main() int {
  if bon() != nil {
    return 1
  }
  if solde() == error("solde") {
    return 42
  }
  return 0
}
```

> `(T, error)` is the only multi-result form. The second type is `error`.

> `appel() or return` follows a call. If the call returns `(T, error)`, the expression is `T`. `nil` lets it continue. Otherwise the current function returns this error.

> In a `(T, error)` function, `return v` returns `v` and `nil`. `return error("solde")` returns the zero value of `T` and this error.

**Diagnostic.** `or return : la fonction ne rend pas error` — `or return` in a function that does not return `error`. `or return attendu` — a `(T, error)` call used as `T` without `or return`. `erreur ignorée` — an ignored `error`, outside `defer` and outside `thread`.

> A host fault stops the process. Index out of bounds, division by zero, arena exhausted. It names the file, the line and the column: `why: file:line:column: message`. It is not caught.

**Not in this version.** `try`, `catch`, a catchable panic.
