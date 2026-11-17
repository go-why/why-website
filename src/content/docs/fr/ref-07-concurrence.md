---
title: "Concurrence"
weight: 7
---

# Concurrence

Le fil est celui du système. Why n'a pas d'ordonnanceur : le plafond reste celui du C. L'accolade qui lance attend : l'auteur n'écrit pas de poignée. Le canal copie ou déplace, pour qu'un pointeur n'entre pas dans l'arène d'un autre fil.

> Un fil se lance avec `thread appel`. Le fil a sa pile et son `arena thread`, qui meurt quand son appel retourne. Pas de goroutine. Pas de pile extensible. Pas de runtime d'ordonnancement.

> L'accolade qui contient le `thread` l'attend. Un `if`, un `else`, un `arena`, un bras de `select` et le corps d'une fonction sont de ces accolades. Le corps d'un `for` ne l'est pas.

> `chan[T](n)` ouvre `n` places. La file ne grandit pas. `n` nul est un rendez-vous : la valeur est copiée, puis les deux continuent.

> Le copier est `la garde ne se copie pas`. `=` et `return` le déplacent. La source devient vide. Le compilateur le ferme à la fin du nom qui le tient. L'auteur n'écrit pas `fermer`.

> `c.send(v)` rend `error`. La file pleine bloque. `nil` veut dire que `v` est entré. `c.receive()` rend `(T, error)`. La file vide bloque.

> `p := freeze(x)` déplace `x`. `freeze` marque le stockage. Une écriture qui atteint ce stockage est `freeze`.

> `arena shared nom { }` meurt à l'accolade, après l'attente des fils lancés dedans. `nom.make` et `nom.append` restent sur le fil qui a ouvert le bloc.

> `select` rend une `error`. Le premier bras prêt, dans l'ordre du texte, court. Pas de `default`.

**Diagnostic.** `thread attend un appel` — `thread` sans appel. `la garde ne se copie pas` — copier un canal. `garde déplacée` — envoyer ou recevoir sur un nom vide. `le canal reste un nom` — un canal dans un champ, une tranche ou une map. `le pointeur ne sort pas` — un argument qui ne survit pas à l'appel. `arène partagée` — passer une arène partagée à un `thread`. `select attend un bras` — `select` sans bras. `case hors select` — `case` hors `select`. `alias` — une écriture sur un stockage `freeze` qui a encore un alias mutable.

**Pas dans cette version.** `entree[T](n)` et `sortie[T](n)`. La goroutine. La pile extensible. L'ordonnanceur.
