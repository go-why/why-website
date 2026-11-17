---
title: "Mémoire"
weight: 3
---

# Mémoire

Le bloc `arena` est l'idée ajoutée. L'auteur nomme l'accolade qui est la mort, il n'écrit pas `free`. La pile, le bloc et `arena thread` sont les trois morts qu'on peut montrer du doigt.

> Le bloc `arena nom { … }` crée une arène. Tout ce qui est alloué dans le bloc meurt à la fermeture de l'accolade. L'auteur ne libère pas. Le compilateur insère la libération.

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

Le littéral `[]T{…}` vit dans le bloc `arena nom` et meurt avec lui. Sans ce bloc, y compris dans `arena thread`, c'est la pile de l'appel. Une tranche née là ne sort pas de l'appel.

> `defer` exécutera l'appel à la sortie du bloc, avant la libération de l'arène. Il rend ce que C a alloué, parce que l'arène ne libère que ce qu'elle a créé.

> `arena thread` lance un fil. L'accolade attend le fil avant la libération. Le fil a sa propre pile.

> `arena shared nom { … }` est une arène que deux fils lisent par `freeze` ou par canal. `nom.make` et `nom.append` restent sur le fil qui a ouvert le bloc.

**Diagnostic.** `arène partagée` — passer une arène partagée à un `thread`.

**Pas dans cette version.** Un destructeur écrit par l'auteur. Un ramasse-miettes. Un borrow checker.
