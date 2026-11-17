---
title: "Document"
weight: 10
---

# Document

Un document `.oo` est une possibilité. SemCards, le prototype, peut s'en servir. La carte a un nom, un prototype, des slots, des méthodes. Ce n'est pas du Why : `arena` n'est pas un mot de `.oo`.

> Un fichier `.oo` est une suite d'objets. L'indentation est le bloc. `//` commente jusqu'au bout de la ligne. L'image chargée au boot est la copie. Le fichier reste la vérité. Le programme ne crée pas d'objet, n'en libère pas, et ne s'inspecte pas.

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

> Un objet a un nom, un prototype optionnel, des slots et des méthodes. `object MillIn : Stack` lit `qty` sur `Stack` tant que `MillIn` ne l'a pas écrit. L'écriture tombe toujours sur le receveur.

> Une méthode est `on nom (params):`. Il n'y a pas de fonction, pas de `return`. La valeur de la méthode est la dernière valeur calculée.

> Les valeurs sont `nothing`, `true`, `false`, l'entier, le texte, la liste, l'objet, le canevas.

> La liste est le seul agrégat. `[a, b]`. `add`, `remove`, `length`, `at`. `for x in liste:` copie la liste avant de marcher.

> Le canevas n'est pas construit par le programme. L'hôte le passe à `draw`. Les méthodes (`rect`, `text`, `frame`, `hit`, `chrome`, `card`) enregistrent des ordres que l'hôte rejoue. Elles rendent `nothing`.

> Une erreur est une panne de l'hôte : slot absent, mauvais nombre d'arguments, division par zéro, appel plus profond que 48. Le programme ne la rattrape pas.

**Diagnostic.** `slot absent` — lire un slot qui n'existe pas. `arguments : n` — mauvais nombre d'arguments. `division par zéro` — diviser par zéro. `profondeur` — appel plus profond que 48.

**Pas dans cette version.** Le pointeur, l'allocation, la concurrence, la classe, le générique dans un document.
