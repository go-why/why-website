---
title: "Lexique"
weight: 1
---

# Lexique

Un fichier se lit seul. Deux espaces, un saut de ligne, `//`. La majuscule est la frontière du paquet. Un nom ne cache pas un autre : le lecteur voit le seul sens.

> Un fichier `.wc` est UTF-8. L'indentation est de deux espaces. Une tabulation est refusée. `//` commente jusqu'au bout de la ligne. Pas de préprocesseur, pas d'en-tête, pas de macro, pas de point-virgule. Un saut de ligne termine un énoncé. Après un opérateur infixe, il continue l'expression.

```
func somme(a, b int) int {
  return a + b
}

func main() int {
  return somme(10, 20)
}
```

`:=` déclare, `=` affecte, `==` compare. Le type suit le nom. Plusieurs noms du même type partagent le type : `a, b int`.

> Un nom exporté commence par une majuscule. Le paquet est le répertoire. Un nom se résout dans le bloc, puis dans le fichier, puis dans les autres fichiers du paquet, puis dans les paquets importés. Un nom ne cache pas un autre. `:=` ou un paramètre qui répète un nom déjà visible est une erreur.

```
import "../lib" lib

func main() int {
  return lib.Reponse()
}
```

**Diagnostic.** `basse : minuscule, pas visible hors du paquet` — un nom minuscule d'un autre paquet est refusé. Deux imports du même nom sont une erreur. Un cycle d'imports est une erreur. Un paquet importé qui a un `main` est refusé : `import lib : le paquet a un main`.

**Mots réservés.** `func struct interface arena defer if else for return or nil true false extern freeze shared thread map chan select case import entree sortie garde`

**Pas dans cette version.** La tabulation, le point-virgule, le commentaire de bloc, le préprocesseur.
