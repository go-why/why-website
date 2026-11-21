---
title: "Why"
weight: 0
---

# Why

Why est un langage de programmation. Sa surface est proche de Go : les signes sont ceux du C, les déclarations sont celles de Go (le nom, puis le type). L'objet est un struct copié, sans héritage. Le produit est un binaire natif, sans runtime.

L'idée ajoutée — la seule — est le bloc `arena`. L'auteur nomme l'accolade qui est la mort ; le compilateur insère la libération. Il n'y a pas de ramasse-miettes, pas de borrow checker, pas d'héritage, pas de destructeur écrit par l'auteur.

| Extension | Rôle |
|---|---|
| `.wc` | Le code source Why. |
| `.wo` | Le binaire ou la bibliothèque que `why build` produit. |
| `.oo` | Un document. Chargé par un programme, pas compilé. (Pas encore implémenté.) |

Le binaire s'appelle `why`. La spécification qui fait référence est [why.md](why.md).

## Le why

Le langage s'appelle Why parce que chaque concept dit sa raison. La règle tranche ; la raison explique. Elle est écrite dans [why.md](why.md), au début de chaque section, et reprise ici.

### Trois fichiers

Le code source (`.wc`) se compile en un binaire (`.wo`). Un binaire peut, à l'exécution, charger un document (`.oo`). Modifier le document ne requiert pas de recompilation du binaire. Le fichier reste la source de vérité ; l'image en mémoire en est la copie.

### Lexique

Un fichier `.wc` se lit sans préprocesseur : deux espaces d'indentation, un saut de ligne termine un énoncé, `//` commente jusqu'à la fin de la ligne. Un nom qui commence par une majuscule est exporté — c'est la frontière du paquet, sans mot-clé `public`. Un nom ne masque pas un autre nom visible : le lecteur voit toujours un seul sens.

### Valeurs

Why a un seul type numérique : l'entier du mot machine. `string` est une séquence d'octets de longueur connue, pas un texte Unicode. L'en-tête d'une tranche ou d'une map porte le nom de l'arène qui l'a allouée, pour que la durée de vie des octets soit visible dans le texte. Une map ne grandit pas : accéder à une clé absente est une panne, pas une allocation cachée.

### Mémoire — le bloc `arena`

Le bloc `arena` est l'unique idée ajoutée par Why. L'auteur nomme l'accolade fermante qui libère la mémoire ; il n'écrit pas `free`. Trois niveaux de libération existent :

- **La pile de l'appel** — libérée au retour de la fonction.
- **Le bloc `arena`** — libéré à la fermeture du bloc, par une libération que le compilateur insère.
- **`arena thread`** — libérée à la mort du fil.

```
func main() {
  arena doc {
    buf := read("a.txt") or return
    ls := parse(buf)
    afficher(ls)
  } // une libération, pour tout le document
}
```

### Garde

Une garde est un struct qui possède son stockage (une tranche, une map, un canal). Le compilateur insère la libération à la fin de la portée du nom qui détient la garde. L'auteur n'écrit pas cette libération : ce n'est pas un destructeur. `return` et `=` déplacent la garde ; la source devient vide.

### Fonctions et méthodes

Il n'y a qu'une seule forme, `func`. Une méthode est cette forme avec un receveur `me`. `or return` propage l'erreur, au lieu d'une comparaison après chaque appel.

```
func (me *Compte) debiter(m int) error {
  if me.solde < m { return ErrSolde }
  me.solde -= m
  return nil
}
```

### Interfaces et composition

Une interface est une liste de méthodes. Le struct reste dans son paquet ; l'appelant ne voit que les méthodes. La composition nomme le champ : `Boite` n'est pas un `Compte`. Pas d'héritage, pas de promotion de méthodes.

### Génériques

Un type générique comme `Pile[T]` est instancié en fonctions concrètes à la compilation. Le code C généré ne voit que ces fonctions. La seule contrainte qu'on peut imposer à `T` est une interface : il n'y a pas un second langage de contraintes.

### Erreurs

`error` est une valeur, comme les autres. Une fonction renvoie `(T, error)` ; l'appelant compare avec `==`. `or return` propage l'erreur de la fonction en cours. Une panne de l'hôte (indice hors table, division par zéro, arène épuisée) arrête le processus : ce n'est pas une erreur que le programme peut rattraper.

### Concurrence

Why utilise les fils du système, pas de goroutines, pas d'ordonnanceur. Le plafond de performance reste celui du C. Un canal copie ou déplace les valeurs, pour qu'un pointeur n'entre pas dans l'arène d'un autre fil.

- `thread appel` lance un fil et l'attend à l'accolade.
- `chan[T](n)` ouvre une file bornée de `n` places.
- `for v in c` reçoit jusqu'à la fermeture du canal.
- `select` attend des bras de canal ; le premier prêt, dans l'ordre du texte, court.
- `freeze` marque un stockage comme immuable ; une écriture qui y atteint est une erreur.
- `arena shared` permet à deux fils de lire une même arène par `freeze` ou par canal.

### Appel du C

`extern` déclare une fonction C avec une signature écrite à la main. Why ne parse pas les en-têtes C. `defer` permet de libérer la mémoire allouée par C, car l'arène ne libère que ce qu'elle a elle-même créé.

### Produit

Le fichier `.wo` est un binaire natif, sans runtime Why. `why run [répertoire]` compile et lance le programme. `why run monde.oo` lance le `.wo` déjà écrit dans le répertoire courant et lui passe le document. Éditer le `.oo` ne recompile pas.

### Document `.oo` — une possibilité, pas encore implémentée

Un document `.oo` est une possibilité offerte aux programmes Why. La carte a un nom, un prototype, des slots, des méthodes. Ce n'est pas du Why : l'auteur d'une carte ne choisirait pas une arène. Le graphe d'objets serait une table d'identifiants dans une arène, pour que plusieurs noms visent la même carte. La libération du graphe serait au rechargement, une fois pour toute la table.

### Refus

Un ramasse-miettes, un borrow checker, un héritage ou un destructeur écrit par l'auteur cacheraient la mort que le bloc `arena` nomme. C'est pourquoi Why les refuse.

### Interpréteur

Un interpréteur écrit en Why serait le même programme, plus sec. Le plafond du C sur une méthode de quelques lignes n'est pas l'objectif. On ne réécrit pas le langage pour accélérer un prototype dont le sujet est un document.

## Tour

Le tour est une exécution interactive dans le navigateur. On l'ouvre sur [play.why.noematic.eu](https://play.why.noematic.eu).

Les défis sont l'entraînement : chaque niveau donne un objectif et une contrainte, et c'est toi qui écris le code. On les ouvre sur [defi.why.noematic.eu](https://defi.why.noematic.eu).

Chaque page a un titre, une leçon en français, une leçon en anglais, et un fragment de code avec un `main`. La page montre le code de sortie, ou le diagnostic si la construction est refusée.

Le projet n'est pas open source pour le moment. Une question, ou un intérêt pour le code : [contact@noematic.eu](mailto:contact@noematic.eu).

## Référence

Trois textes ont trois rôles.

**`why.md`** décide. Un comportement qui manque s'y ajoute dans le même changement que le code. Le compilateur ne décrit pas un comportement que cette spec ne fixe pas.

**Le tour** fait exécuter une construction, une page à la fois, sur le sous-ensemble déjà compilé.

**La référence** s'écrit pour être lue. Elle suit l'ordre de `why.md`. Chaque page commence par le why du concept, puis reprend la phrase de la spec, un fragment du tour ou de `testdata/`, et le diagnostic quand la construction est refusée. Une construction écrite mais pas encore compilée est marquée `pas dans cette version`. Les fichiers, le réseau, le JSON et le formatage sont une bibliothèque ; ils n'entrent pas dans la référence du langage. Voir [ref/](ref/README.md).

### État de cette version

Compilé : fonctions, structs, méthodes, interfaces, tranches, maps, bloc `arena`, `arena thread`, `defer`, `error`, `or return`, pointeur stocké, garde, paramètres de type sur un struct et sur une fonction, la seule contrainte étant une interface, `thread appel`, `chan[T](n)`, `for v in c`, `select`, `freeze`, `arena shared`, `import`.

Pas encore compilé : le document `.oo`.

## Quatre langages

La surface proche est celle de Go. Le plafond visé est celui du C. L'objet est un struct copié. La construction que ces quatre langages n'ont pas ensemble est le bloc qui libère.

| | C | C++ | Java | Go | Why |
|---|---|---|---|---|---|
| Mémoire | `malloc`, `free` | destructeur, RAII | ramasse-miettes | ramasse-miettes | pile de l'appel, bloc `arena`, `arena thread`, garde |
| Fonction | une forme, macros à côté | surcharge | méthode dans la classe, surcharge | `func`, méthode hors du type | une forme, `func`. Méthode `func (me *T) nom` |
| Assemblage | `struct` | classe, héritage | classe, héritage, interface nommée | `struct`, embedding, interface structurelle | `struct` copié, champ nommé, interface structurelle |
| Erreur | code de retour | exception | exception | `(T, error)`, comparée à la main | `(T, error)`, propagée avec `or return` |
| Concurrence | fil POSIX | `std::thread` | fil de la machine virtuelle | goroutine, ordonnanceur | fil du système, canal borné |
| Générique | `void *`, macro | template | générique effacé | générique | type contraint par une interface, instancié à la compilation |
| Texte | préprocesseur, en-tête | préprocesseur, template | annotation | fichier unique | fichier `.wc`, deux espaces, pas de macro |
| Produit | le programme | le programme | le programme | le programme | le programme |

L'appel d'une méthode de champ nomme le champ : `b.c.debiter(1)`. Une interface reçoit une copie du struct quand les méthodes correspondent. L'appel sur l'interface passe par une vtable ; l'appel sur le struct reste direct.

Une panne de l'hôte — indice hors table ou division par zéro — arrête le processus. Le message est `why: fichier:ligne:colonne: message`. Ce n'est pas une erreur que le programme rattrape.

`extern func` déclare une fonction C, signature écrite à la main. Il prend et rend `int`, `string` et `[]u8`. Why ne libère pas la mémoire qui vient de C ; `defer` le fera, à la sortie du bloc, avant la libération de l'arène.
