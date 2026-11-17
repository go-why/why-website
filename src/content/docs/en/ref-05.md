---
title: "Interfaces and composition"
weight: 5
---

The interface is the list of methods. The struct stays in its package, the caller sees only the methods. Composition names the field: `Boite` is not a `Compte`. No inheritance.

> An interface is a list of methods. It does not repeat the receiver. It is satisfied if the concrete type has these methods, with the same parameters and the same results. No `implements`.

```
interface Stockeur {
  lire(k string) ([]u8, error)
  ecrire(k string, v []u8) error
}
```

> If the concrete type is known at the call, the call is direct. If it is not, the call goes through the vtable.

> A concrete value is passed where an interface is expected when the methods match, parameters and result. The value passed is a copy. The interface points to this copy and to the vtable. The copy lives for the duration of the call.

> No inheritance. Composition is a field.

```
struct Boite { c Compte, etiquette string }
```

`Boite` does not have the methods of `Compte`. One writes `b.c.debiter(1)`. Promoting the field's methods is refused. The author names the field.

**Diagnostic.** `les méthodes ne s'accordent pas` — the concrete methods do not agree on the arrangement of a value. The empty interface is refused. No type assertion. An interface without a value is a host fault.

**Not in this version.** Inheritance. Type assertion.
