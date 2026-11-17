---
title: "Fonctions et méthodes"
weight: 4
---

# Fonctions et méthodes

Une seule forme, `func`. La méthode est cette forme avec un receveur `me`. `or return` propage l'erreur, au lieu d'une comparaison après chaque appel.

> `x = y` copie la valeur. `x` est une variable ou un champ. `x += y` est `x = x + y`. La même famille : `-=`, `*=`, `/=`, `%=`.

> `x.m(...)` appelle la méthode `m` du type de `x`. `me` a le type `T` ou `*T`, où `T` est le type de `x`. Si `me` est un `*T` et que `x` est une valeur `T`, l'appel passe l'adresse de `x`. Il n'y a pas d'opérateur `&`.

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

> `nom := Type` déclare la valeur zéro de `Type`. Un `int` zéro vaut 0. Un `bool` zéro vaut `false`. Un struct zéro a ses champs à zéro.

> `or return` propage une erreur. `or` n'est pas un opérateur booléen.

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

> Un paramètre peut porter le nom d'un champ : le champ s'écrit `me.nom`.

**Diagnostic.** `s'appelle me` — le receveur doit s'appeler `me`.

**Pas dans cette version.** La surcharge de nom (plusieurs `func f()` avec des signatures différentes).
