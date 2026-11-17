---
title: "Erreurs"
weight: 6
---

# Erreurs

`error` est une valeur, elle rentre avec le résultat. `or return` la propage. Une panne de l'hôte arrête le processus : ce n'est pas une erreur que le programme rattrape.

> `error` est un type. `nil` veut dire pas d'erreur. `nil` est sa valeur zéro. `e := error` est `nil`. Une erreur se crée avec `error("solde")`. `error("")` est `nil`.

> Elle se compare avec `==`. `error("solde") == error("solde")` est vrai. `error("solde") == nil` est faux.

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

> `(T, error)` est la seule forme à plusieurs résultats. Le second type est `error`.

> `appel() or return` suit un appel. Si l'appel rend `(T, error)`, l'expression vaut `T`. `nil` laisse continuer. Sinon la fonction en cours retourne cette erreur.

> Dans une fonction `(T, error)`, `return v` rend `v` et `nil`. `return error("solde")` rend la valeur zéro de `T` et cette erreur.

**Diagnostic.** `or return : la fonction ne rend pas error` — `or return` dans une fonction qui ne rend pas `error`. `or return attendu` — un appel `(T, error)` utilisé comme `T` sans `or return`. `erreur ignorée` — une `error` ignorée, hors `defer` et hors `thread`.

> Une panne de l'hôte arrête le processus. Indice hors table, division par zéro, arène épuisée. Elle nomme le fichier, la ligne et la colonne : `why: fichier:ligne:colonne: message`. Elle ne se rattrape pas.

**Pas dans cette version.** `try`, `catch`, une panique rattrapable.
