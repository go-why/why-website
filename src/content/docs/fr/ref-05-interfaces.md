---
title: "Interfaces et composition"
weight: 5
---

# Interfaces et composition

L'interface est la liste des méthodes. Le struct reste dans son paquet, l'appelant ne voit que les méthodes. La composition nomme le champ : `Boite` n'est pas un `Compte`. Pas d'héritage.

> Une interface est une liste de méthodes. Elle ne répète pas le receveur. Elle est satisfaite si le type concret a ces méthodes, avec les mêmes paramètres et les mêmes résultats. Pas de `implements`.

```
interface Stockeur {
  lire(k string) ([]u8, error)
  ecrire(k string, v []u8) error
}
```

> Si le type concret est connu à l'appel, l'appel est direct. S'il ne l'est pas, l'appel passe par la vtable.

> Une valeur concrète est passée là où une interface est attendue quand les méthodes correspondent, paramètres et résultat. La valeur passée est une copie. L'interface pointe vers cette copie et vers la vtable. La copie vit le temps de l'appel.

> Pas d'héritage. La composition est un champ.

```
struct Boite { c Compte, etiquette string }
```

`Boite` n'a pas les méthodes de `Compte`. On écrit `b.c.debiter(1)`. Promouvoir les méthodes du champ est refusé. L'auteur nomme le champ.

**Diagnostic.** `les méthodes ne s'accordent pas` — les méthodes concrètes ne s'accordent pas sur le rangement d'une valeur. L'interface vide est refusée. Pas d'assertion de type. Une interface sans valeur est une panne hôte.

**Pas dans cette version.** L'héritage. L'assertion de type.
