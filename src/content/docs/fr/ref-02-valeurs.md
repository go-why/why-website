---
title: "Valeurs"
weight: 2
---

# Valeurs

Un seul nombre, l'entier du mot machine. `string` est des octets, pas un texte Unicode. L'en-tête d'une tranche ou d'une map porte son arène, pour que la vie des octets ait un nom.

> | Genre | Note |
> |---|---|
> | `nil` | Absence. Seul habitant de `error` sans erreur. |
> | `bool` | `true`, `false`. |
> | `int` | Entier signé du mot machine. Seul nombre. |
> | `u8` | Octet. Pour les tampons. |
> | `string` | Octets immuables, longueur connue. Pas un texte Unicode. |
> | `error` | Une valeur. Comparée avec `==`. Pas une exception. |
> | struct | Valeur, copiée à l'affectation. |
> | `*T` | Pointeur vers un `T` vivant dans une arène visible. |
> | `[]T` | Tranche : pointeur, longueur, arène propriétaire. |
> | `map[K]V` | Map. Même en-tête que la tranche. |
> | `chan[T]` | File bornée. Garde. Un nom. |
> | `entree[T]` | Prise d'écriture. Copiée. Née vide. |
> | `sortie[T]` | Prise de lecture. Copiée. Née vide. |
> | interface | Pointeur vers la valeur, pointeur vers la vtable. |
> | `Id` | Indice dans une table du document. Pas un pointeur. |

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

`/` et `%` tronquent vers zéro. `-n` est l'unaire. `0 - n` est admis. Les opérandes s'évaluent de gauche à droite.

> `==` exige deux valeurs de même genre. `!=`, `<`, `>`, `<=`, `>=` sont les signes du C. `<`, `>`, `<=`, `>=` comparent deux entiers. `&&` et `||` court-circuitent.

> `if` prend un booléen. Le bloc court quand il est vrai. `else` est l'autre bloc, sur la même ligne que `}`. `else if` enchaîne.

```
func main() int {
  n := 3
  if n > 1 {
    n = n + 39
  }
  return n
}
```

> `for` répète le bloc tant que le booléen est vrai. Le pas est une instruction du corps. Pas de `break`.

> `for x in xs` copie la tranche avant le premier tour. `x` est l'élément, un nom du corps. `for i, x in xs` lie aussi l'indice avant l'élément.

> `x[i]` lit. `i` est un `int`. L'élément d'une tranche a le type `T`. L'élément d'une chaîne est un `u8`. `len(x)` rend un `int`.

**Diagnostic.** `indice hors table` — l'indice hors de `0 .. len-1`, y compris négatif.

> `map[K]V` est une map. `K` est un `int` ou une `string`. `m[k]` lit. `m[k] = v` écrit une clé déjà présente. Une clé absente est une panne hôte. La map ne grandit pas.

> `x = y` copie la valeur. `x` est une variable ou un champ. `x += y` est `x = x + y`. La même famille : `-=`, `*=`, `/=`, `%=`.

> `p := *T` est le pointeur nul. `*p` lit. `*p = v` écrit. Lire ou écrire le pointeur nul est la panne `pointeur nul`.

**Diagnostic.** `pointeur nul` — lire ou écrire le pointeur nul.

**Pas dans cette version.** `**T`, ou un pointeur vers une tranche, une map, une chaîne, une erreur ou une interface. Pas de flottant.
