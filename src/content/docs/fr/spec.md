---
title: "Spécification"
weight: 10
---

# Why — spec 0

Langage. Les signes sont ceux du C. Les déclarations sont celles de Go : le nom, puis le type.
Pas de ramasse-miettes, pas de borrow checker, pas d'héritage.
La seule idée en plus est le bloc `arena`.

Le produit est le programme. Un `.wo` est un binaire, ou une lib.
SemCards est un prototype. Il peut charger un document `.oo`, l'interpréter et le dessiner. C'est une occasion. Ce n'est pas le métier du langage.
Cette spec fixe le langage et le produit `.wo`. Le document est décrit aux §11 et §12. Il n'est pas exigé.

Le langage s'appelle Why. Chaque concept dit son why : la raison pour laquelle il est là. La règle tranche. La raison explique.

Le binaire s'appelle `why`. Pas `wc` : ce nom est la commande Unix.

## 0. Trois fichiers

Pourquoi. Le source se compile. Le produit est le programme. Un `.oo` peut être chargé par ce programme. Le changer ne le recompile pas. S'il est chargé, le fichier reste la vérité, l'image en est la copie.

| Extension | Quoi | Rôle |
|---|---|---|
| `.wc` | source Why | Le code. Fonctions, structs, méthodes. |
| `.wo` | produit | Le binaire, ou la lib, issu d'un ou plusieurs `.wc`. |
| `.oo` | document | Une instance possible. Chargée, pas compilée. |

`.wc` est la seule source de Why. `why build` écrit un `.wo`. Une lib est un `.wo` sans entrée `main`. Un binaire est un `.wo` qui en a une. Le chargeur ne les distingue pas par une autre extension.

`.oo` n'est pas du Why. Un programme peut le charger dans une arène. Le langage ne l'exige pas.

## 1. Lexique

Pourquoi. Un fichier se lit seul, sans préprocesseur : deux espaces, un saut de ligne, `//`. Un document `.oo` peut reprendre cette forme. La majuscule est la frontière du paquet, sans mot `public`. Un nom ne cache pas un autre : le lecteur voit le seul sens.

Un fichier `.wc` est UTF-8. L'indentation est de deux espaces. Une tabulation est refusée.
`//` commente jusqu'au bout de la ligne. Il n'y a pas de commentaire de bloc.
Pas de préprocesseur, pas d'en-tête, pas de macro, pas de point-virgule.
Un saut de ligne termine un énoncé. Après un opérateur infixe, il continue l'expression.

Un nom est une suite de lettres, de chiffres et de `_`. Il ne commence pas par un chiffre.
Un nom exporté commence par une majuscule. Le paquet est le répertoire.
Un nom se résout dans le bloc, puis dans le fichier, puis dans les autres fichiers du paquet, puis dans les paquets importés.
Un nom ne cache pas un autre. `:=` ou un paramètre qui répète un nom déjà visible est une erreur. Le nom n'est pas recréé.
Un paramètre peut porter le nom d'un champ : le champ s'écrit `me.nom`.

Mots réservés :

```
func struct interface arena defer if else for return
or nil true false extern freeze shared thread map
chan select case import entree sortie garde
```

La ligne d'import est `import "chemin" nom`. Le chemin est le répertoire du paquet importé, relatif au répertoire qui importe. Le nom est celui sous lequel le paquet est vu. Un nom exporté commence par une majuscule ; un nom minuscule d'un autre paquet est refusé : `basse : minuscule, pas visible hors du paquet`. Deux imports du même nom sont une erreur. Un cycle d'imports est une erreur. Un paquet importé qui a un `main` est refusé : `import lib : le paquet a un main`. Dans le paquet, la minuscule reste visible : c'est le même espace de noms.

`:=` déclare. `=` affecte. `==` compare.
Le type suit le nom, dans un paramètre comme dans un champ. Plusieurs noms du même type partagent le type : `a, b int`. La virgule entre noms est la liste ; la virgule entre listes est le séparateur des groupes. Le résultat suit les paramètres.

```
struct Compte { solde int }

func (me *Compte) debiter(m int) error {
  if me.solde < m { return ErrSolde }
  me.solde -= m
  return nil
}
```

## 2. Valeurs

Pourquoi. Un seul nombre, l'entier du mot machine. Un document chargé par un programme compte de la même façon. `string` est des octets, pas un texte Unicode, pour qu'un nom de slot et un tampon soient la même chose. L'en-tête d'une tranche ou d'une map porte son arène, pour que la vie des octets ait un nom. Une map ne grandit pas : une clé absente est une panne, pas une allocation cachée.

| Genre | Note |
|---|---|
| `nil` | Absence. Seul habitant de `error` sans erreur. |
| `bool` | `true`, `false`. |
| `int` | Entier signé du mot machine. Seul nombre. |
| `u8` | Octet. Pour les tampons. |
| `string` | Octets immuables, longueur connue. Pas un texte Unicode. |
| `error` | Une valeur. Comparée avec `==`. Pas une exception. |
| struct | Valeur, copiée à l'affectation. |
| `*T` | Pointeur vers un `T` vivant dans une arène visible. |
| `[]T` | Tranche : pointeur, longueur, arène propriétaire. |
| `map[K]V` | Map. Même en-tête que la tranche. |
| `chan[T]` | File bornée. Garde. Un nom. |
| `entree[T]` | Prise d'écriture. Copiée. Née vide. |
| `sortie[T]` | Prise de lecture. Copiée. Née vide. |
| interface | Pointeur vers la valeur, pointeur vers la vtable. |
| `Id` | Indice dans une table du document. Pas un pointeur. |

Un struct a au moins un champ. Un struct ne se contient pas. Un champ `*T` ne le contient pas. `struct Noeud { suite *Noeud }` est admis.

`/` et `%` tronquent vers zéro. `-n` est l'unaire. `0 - n` est admis.
Les opérandes et les arguments s'évaluent de gauche à droite. Un appel se termine avant l'opérande ou l'argument suivant.
`==` exige deux valeurs de même genre. `!=`, `<`, `>`, `<=`, `>=` sont les signes du C.
`<`, `>`, `<=`, `>=` comparent deux entiers.
Une comparaison rend un `bool`. `!`, `&&` et `||` prennent des booléens.
`&&` et `||` court-circuitent : l'opérande droit ne court pas quand le gauche a déjà décidé.
`if` prend un booléen. Le bloc court quand il est vrai. `else` est l'autre bloc, sur la même ligne que `}`. `else if` enchaîne.
`for` répète le bloc tant que le booléen est vrai. Le pas est une instruction du corps. Pas de `break`.
`for x in xs` copie la tranche avant le premier tour. `x` est l'élément, un nom du corps. `for i, x in xs` lie aussi l'indice avant l'élément. `i` est un `int` du corps. L'affecter ne change pas le pas.
`for v in c` sur un canal est au §8. Il emprunte le canal, il ne le copie pas.
Le littéral `[]T{...}` vit dans le bloc `arena nom` et meurt avec lui. Sans ce bloc, y compris dans `arena thread`, c'est la pile de l'appel. Une tranche née là ne sort pas de l'appel. Chaque littéral a un stockage pour l'appel. Une boucle le réutilise. `thread.make` est l'allocation qui naît dans l'arène du fil.
`nom := []T` est la tranche vide.
`x[i]` lit. `i` est un `int`. L'élément d'une tranche a le type `T`. L'élément d'une chaîne est un `u8`.
`len(x)` rend un `int`, pour une tranche, une chaîne ou une map. Pas pour un canal.
L'indice hors de `0 .. len-1`, y compris négatif, est la panne `indice hors table`. Une table est ce stockage indicé : les éléments d'une tranche, les octets d'une chaîne, et la table du document.
`xs[i] = v` écrit dans la tranche. `s[i] = v` est refusé.
Copier une tranche copie l'en-tête. Les deux noms voient le même stockage.
`x[lo:hi]` est une fenêtre sur une tranche ou une chaîne. `lo` et `hi` sont des `int`. La borne absente avant `:` vaut `0`. Celle d'après vaut `len(x)`. Il faut `0 <= lo <= hi <= len(x)`. Sinon, c'est une panne hôte. La fenêtre partage le stockage. Sa longueur est `hi - lo`. Une fenêtre sur une chaîne est une chaîne. Une fenêtre sur une tranche née dans l'appel ne sort pas de l'appel.
`map[K]V` est une map. `K` est un `int` ou une `string`. `V` suit la règle d'un élément de tranche.
La map a le même en-tête qu'une tranche. La copier partage le stockage. `==` sur une `string`, une tranche ou une map compare cet en-tête : le pointeur et la longueur. Deux textes égaux qui ne partagent pas le stockage ne sont pas égaux. Une copie du même en-tête l'est. `error` compare les octets. Un champ lu dans un fichier se compare octet par octet, en marchant le tampon. Pas de fonction d'égalité dans la langue.
Le littéral `map[K]V{k: v}` vit dans le bloc `arena nom` et meurt avec lui. Sans ce bloc, y compris dans `arena thread`, c'est la pile de l'appel. Une map née là ne sort pas de l'appel. Chaque littéral a un stockage pour l'appel. Une boucle le réutilise.
`nom := map[K]V` est la map vide.
`m[k]` lit. `m[k] = v` écrit une clé déjà présente. Une clé absente est une panne hôte. La map ne grandit pas.
Une clé répétée garde la dernière valeur. L'ordre des clés est celui de la première apparition. `len(m)` est le nombre de clés.
Une clé `int` est le nombre. Une clé `string` est les octets.
`for v in m` copie la map avant le premier tour. `v` est la valeur, un nom du corps. `for k, v in m` lie la clé avant la valeur. Affecter `k` ou `v` ne change pas la map.
Une chaîne littérale est les octets entre les guillemets. `\` est refusé.
`or return` propage une erreur. `or` n'est pas un opérateur booléen.
Pas de flottant. Un dessin à échelle fixe compte en `int`.
Un flottant étranger entre par `extern` et ne reste pas dans le langage.

`string` n'est pas une tranche mutable. `[]u8(s)` copie ses octets dans l'arène du bloc courant. Hors d'un bloc, la copie vit dans la pile de l'appel et ne sort pas de l'appel.
`*T` pointe vers un `int`, un `bool`, un `u8` ou un struct. `p := *T` est le pointeur nul.
`*p` lit. `*p = v` écrit. Lire ou écrire le pointeur nul est la panne `pointeur nul`.
`p = x`, un argument ou un `return` prend l'adresse de `x` quand le type attendu est `*T`, que `x` a le type `T`, et que `x` est une variable, un champ ou un élément. Il n'y a pas d'opérateur `&`.
`**T`, ou un pointeur vers une tranche, une map, une chaîne, une erreur ou une interface, reste `pointeur : pas dans cette version`.

## 3. Mémoire

Pourquoi. Le bloc `arena` est l'idée ajoutée. L'auteur nomme l'accolade qui est la mort, il n'écrit pas `free`. La pile, le bloc et `arena thread` sont les trois morts qu'on peut montrer du doigt.

Toute valeur Why vit dans une arène. Il y en a trois sortes.

- La pile de l'appel. Un struct local, un entier, un pointeur.
- Le bloc `arena`. Tout ce que le bloc alloue meurt à l'accolade fermante.
  Le compilateur insère une seule libération.
- `arena thread`, pour ce qui doit survivre à la fonction et que l'auteur n'a pas nommé.
  Elle meurt avec le thread.

```
func main() {
  arena doc {
    buf := read("a.txt") or return
    ls := parse(buf)
    afficher(ls)
  } // une libération, pour tout le document
}
```

Règles.

1. Une référence ne sort pas de son arène. Retourner une tranche née dans le bloc est une erreur de compilation.
2. Dans un bloc, une donnée a un pointeur mutable, ou plusieurs pointeurs en lecture. Pas les deux.
   Deux adresses de la même variable, prises dans le bloc, ne coexistent pas quand l'une écrit. Le message est `pointeur mutable`. Plusieurs lectures coexistent. Copier un pointeur ne prend pas une seconde adresse.
   La copie d'un struct qui contient un pointeur, une tranche ou une map partage ce stockage. La copie d'un struct qui n'a que des `int`, des `bool` et des `u8` n'est pas un alias.
3. Pas d'arithmétique de pointeur. Pas de conversion d'entier en pointeur.
4. `defer` exécute une fonction à la sortie du bloc. Il sert aux ressources étrangères, pas à la mémoire Why.
   `defer appel` enregistre l'appel. Les arguments sont évalués à cet endroit. Le résultat de l'appel différé est ignoré. Sans appel, le message est `defer attend un appel`.
   Un `return` évalue son résultat, puis sort de chaque bloc ouvert, de l'intérieur vers l'extérieur. La sortie d'un bloc ferme les canaux dont le nom meurt ici, attend les fils lancés ici, puis exécute les `defer` du dernier au premier. Les gardes qui restent meurent, et l'arène du bloc se libère. `arena thread` ne se libère pas à cette accolade. Le corps d'un `for` ferme ses canaux et exécute ses `defer` à chaque tour. Il n'attend pas ses fils : ils le sont au bloc qui contient le `for`. Un fil lancé dans un appel différé est attendu avant le retour de cet appel.

L'auteur n'écrit pas `free`. Il nomme le bloc dont la fin est la mort.
Une arène peut être passée. Le paramètre s'écrit `arena`.
`a.make([]T, n)` alloue une tranche de longueur `n` dans `a`, initialisée à zéro. `n` négatif est la panne `taille négative`. Si le nombre d'octets ne tient pas, ou si l'hôte ne peut pas allouer, la panne est `arène épuisée`.
`a.append(xs, v)` rend une tranche neuve dans `a`, de longueur `len(xs) + 1`, qui se termine par `v`. L'ajout peut prolonger les octets de `xs`. `xs` garde sa longueur, et écrire dans cette longueur écrit dans le préfixe de la tranche rendue. Sinon la tranche rendue est une copie. Le stockage du résultat meurt avec l'arène de `a`. Les octets d'origine ne meurent avec `a` que s'ils y étaient déjà. Si `len(xs)` est déjà le plus grand `int`, ou si le nombre d'octets de la tranche neuve ne tient pas, la panne est `arène épuisée`.
`new` n'existe pas.
`arena nom { }` ouvre un bloc. Ce qu'il alloue meurt à l'accolade. Le compilateur insère une seule libération.
`arena thread { }` ouvre l'arène du fil sous le nom `thread`. Elle ne se libère pas à l'accolade. Elle meurt avec le fil. Chaque fil a la sienne, y compris celui qui exécute `main`. Une tranche née dedans peut sortir de la fonction. Elle ne passe pas à un autre fil. Le message est `le pointeur ne sort pas`.

`struct Nom garde` est une garde. `t := Nom` ne possède rien. `t.make([]T, n)` et `t.append(xs, v)` allouent dans `t`, avec les mêmes pannes que sur une arène. `t.append` prolonge comme `a.append`. Un struct qui contient une garde est une garde, avec ou sans le mot.
`return` et `=` déplacent. La source devient vide. Le compilateur libère la garde à la fin du nom qui la tient encore. L'auteur n'écrit pas cette libération : ce n'est pas un destructeur. Un receveur `*T` emprunte. Un receveur `T`, un paramètre `T` et l'argument qui le remplit déplacent. `*p` déplace la garde visée, et un receveur `T` appelé sur un `*T` aussi. Un `return` déplace encore quand le résultat est `(T, error)`.
Lire une garde déjà déplacée, ou un de ses champs, est `garde déplacée`. Une tranche, une map ou un pointeur tiré de la garde ne sort pas seul. Le passer à un appel qui ne le range pas est permis. Le ranger là où il lui survit est `la tranche ne sort pas`, `la map ne sort pas` ou `le pointeur ne sort pas`. Le ranger dans une autre garde, ou dans un champ atteint en traversant une garde emboîtée, est la même erreur : la tranche ne vit pas dans l'arène qui part. Copier la garde dans une interface, une tranche ou une map est `la garde ne se copie pas`. Déplacer un champ garde le sort du contenant : le contenant ne le libère plus.
Un appel qui rend une garde en est le propriétaire jusqu'à la fin du bloc, puis le compilateur la libère. Ranger une tranche, une map ou un pointeur tiré de ce résultat est `la tranche ne sort pas`, `la map ne sort pas` ou `le pointeur ne sort pas`. Le lire pour un entier, ou le passer à un appel qui ne le range pas, est permis.
Un appel reprend le résumé de l'appelé : le rangement fait dans le corps de l'appelé compte pour l'appelant, au site d'appel. Un corps qui ne fait que transmettre range comme le corps qui range. Une fenêtre d'un paramètre porte le slot de ce paramètre. La récursion répète le résumé tant qu'il grandit. Deux arguments nés dans la même arène restent acceptés. Un résumé n'est ajouté à l'appelant que si les deux bouts sont son receveur ou l'un de ses paramètres. L'appel est jugé sur les arguments réels. Un champ du receveur rangé dans un argument a pour source le receveur : cette source n'est pas l'absence de provenance, ni l'arène du fil. Une écriture dans un élément d'une tranche passée en paramètre range dans cette tranche. Un local qui ne porte pas le slot d'un paramètre ou du receveur n'entre pas dans le résumé. Un local qui recopie un paramètre, comme `t := source`, garde ce slot. Le point fixe s'arrête quand une passe n'ajoute aucun couple : cette stabilisation est le critère, pas le nombre de passes déjà faites. Soixante-quatre passes sans elle refusent la compilation. Le message est `le résumé des appels ne converge pas en 64 itérations`. Le binaire n'est pas écrit. Un nombre fini de couples borne les ajouts si l'analyse ne fait qu'ajouter ; il ne borne pas le nombre de passes à soixante-quatre. L'ordre du parcours et la profondeur de la chaîne changent ce nombre. Un appel d'interface est revu une fois le corps achevé, pour que la comparaison porte sur les résumés finaux. Un désaccord provisoire qui se résout n'est pas gardé. Un désaccord apparu après un accord provisoire est gardé. Un désaccord qui reste refuse l'appel, sans boucler sur ce seul désaccord.

Affecter une arène de bloc à un nom qui lui survit est une erreur. Le message est `l'arène ne sort pas`.
Retourner une tranche née dans le bloc, ou la ranger dans un nom qui lui survit, est une erreur. Le message est `la tranche ne sort pas`.
Retourner une map née dans le bloc, ou la ranger dans un nom qui lui survit, est une erreur. Le message est `la map ne sort pas`.
Retourner une interface née dans le bloc, ou la ranger dans un nom qui lui survit, est une erreur. Le message est `l'interface ne sort pas`.
Retourner un pointeur vers la pile, ou le ranger là où il lui survit, est une erreur. Le message est `le pointeur ne sort pas de l'appel`.
Retourner un pointeur vers une donnée du bloc, ou le ranger dans un nom qui lui survit, est une erreur. Le message est `le pointeur ne sort pas`.
L'adresse d'un champ suit le struct qui le contient. Elle ne suit pas l'arène d'un autre champ. Un pointeur rangé dans un champ suit le stockage qu'il vise, pas l'arène d'un autre champ. Deux champs sont deux adresses. Un struct de la pile qui contient un pointeur vers la pile ne sort pas de cet appel, même si un autre champ vit dans une arène. Le copier dans une variable, un champ, un élément, un `append` ou une interface suit la même règle. Un champ ou un élément qui meurt avec ce pointeur peut le recevoir. Un paramètre qui porte ce pointeur suit la même règle quand l'appel le range dans un `*T`, un élément, un `append` ou une map. Un paramètre `*T` aussi. Un paramètre `interface` aussi : la copie vit dans l'appelant, et ce rangement donne `l'interface ne sort pas de l'appel`. Cette copie vit le temps de l'appel, un bloc plus court ne la tue pas. Un champ interface de ce struct suit la boîte de la pile, pas l'arène d'un autre champ. Un struct imbriqué qui contient cette interface suit la même boîte. Retourner le struct, le champ ou le struct imbriqué donne `l'interface ne sort pas de l'appel`.
Le dernier `return` vivant décide de la vie du résultat. Il remplace celui qui précède.

```
func parse(a arena, buf []u8) ([]Ligne, error) {
  return a.make([]Ligne, n)
}
```

Deux arènes sont convenues pour le prototype SemCards. Elles ne sont pas des mots du langage.
Ce sont des blocs qu'un programme peut ouvrir.

- `image` contient les cartes, les slots, les méthodes, l'arbre du fichier et les textes.
  Elle meurt au rechargement. Une libération pour tout le document.
- `frame` contient le canevas, les locaux de l'interpréteur et la copie d'un `for`.
  Elle englobe le tick et le dessin, et meurt au tick suivant.

## 4. Fonctions et méthodes

Pourquoi. Une seule forme, `func`. La méthode est cette forme avec un receveur `me`. Un document `.oo` peut reprendre ce mot. `or return` propage l'erreur, au lieu d'une comparaison après chaque appel.

Une fonction est `func nom(params) T`.
Plusieurs résultats s'écrivent `(T, error)`. `or return` propage l'erreur.

```
func lire(a arena, chemin string) ([]u8, error) {
  f := open(chemin) or return
  defer f.close()
  n := size(f) or return
  buf := a.make([]u8, n)
  reste := buf
  for len(reste) > 0 {
    k := f.read(reste) or return
    if k == 0 { return error("coupe") }
    reste = reste[k:]
  }
  return buf
}
```

La tranche naît dans `a`, l'arène de l'appelant. Sans ce paramètre, elle ne sort pas de l'appel. `Ecrire` remplace le fichier et ne prend pas d'arène. Une fonction et une méthode ne partagent pas un nom : l'épreuve, un seul paquet, appelle les fonctions `Lire` et `Ecrire`, et les méthodes `(Fd) Read` et `(Fd) Write`.

Un `return` toujours atteint termine la fonction. L'énoncé qui suit, dans le même bloc, n'est pas exécuté. Le compilateur le signale et compile le reste. Le message est `code non exécuté`.
`if true` ne garde que sa première branche. `if false` ne la garde pas. Un `if` dont chaque branche termine, et `for true` dont le corps termine, rendent l'énoncé qui suit non exécuté. Un autre `for`, un `for x in`, et `or return` laissent cet énoncé exécuté : la boucle peut ne pas tourner, et `nil` laisse continuer.
Un `select` dont un bras ne termine pas laisse l'énoncé qui suit exécuté. Si chaque bras termine, le chemin où tous les canaux sont fermés reste ouvert. `or return` après le `select` le ferme, et l'énoncé qui suit est `code non exécuté`. Sans `or return`, l'erreur non lue est `erreur ignorée`. Si la fonction rend une valeur et que ce chemin n'en rend pas, le message est `il manque return`.

Une méthode s'écrit `func (me T) nom(params)`.
Le receveur s'appelle `me`. Il a le type `T` ou `*T`, et `T` est un struct.
Le nom `me` n'est pas celui d'une fonction, d'un struct ou d'une méthode.
Pas de classe, pas de `this`, pas de surcharge.
Deux structs peuvent porter le même nom de méthode. Une fonction et une méthode ne partagent pas un nom.
L'appel s'écrit `b.c.debiter(1)`.

```
func (me *Compte) debiter(m int) error {
  if me.solde < m { return ErrSolde }
  me.solde -= m
  return nil
}
```

`nom := Type` déclare la valeur zéro de `Type`. Un `int` zéro vaut 0. Un `bool` zéro vaut `false`. Un struct zéro a ses champs à zéro.

`x = y` copie la valeur. `x` est une variable ou un champ.
`x += y` est `x = x + y`. La même famille : `-=`, `*=`, `/=`, `%=`.
`x.m(...)` appelle la méthode `m` du type de `x`.
`me` a le type `T` ou `*T`, où `T` est le type de `x`.
Si `me` est un `*T` et que `x` est une valeur `T`, l'appel passe l'adresse de `x`.
`x` est alors une variable ou un champ d'une variable. Il n'y a pas d'opérateur `&`.
L'appel direct `m(...)` ne prend pas cette adresse.
Ranger une tranche, une map, une interface ou un pointeur par une méthode suit les mêmes règles que l'affectation du champ.

## 5. Interfaces et composition

Pourquoi. L'interface est la liste des méthodes. Le struct reste dans son paquet, l'appelant ne voit que les méthodes. La composition nomme le champ : `Boite` n'est pas un `Compte`. Pas d'héritage. Un prototype de carte n'a pas, dans l'hôte, le modèle d'une classe.

Une interface est une liste de méthodes. Elle ne répète pas le receveur.
Elle est satisfaite si le type concret a ces méthodes, avec les mêmes paramètres et les mêmes résultats. Pas de `implements`.
Le receveur reste sur la méthode : `func (me *Compte) lire(k string) ([]u8, error)`.

```
interface Stockeur {
  lire(k string) ([]u8, error)
  ecrire(k string, v []u8) error
}
```

Si le type concret est connu à l'appel, l'appel est direct.
S'il ne l'est pas, l'appel passe par la vtable.
Cet appel suit les méthodes concrètes quand elles s'accordent. S'il rend une valeur du receveur, le résultat a la vie de la valeur d'interface. S'il range une valeur dans le receveur, il suit les mêmes règles que l'affectation du champ. Si les méthodes ne s'accordent pas sur ce rangement, le message est `les méthodes ne s'accordent pas`.
Une valeur concrète est passée là où une interface est attendue quand les méthodes correspondent, paramètres et résultat. Le receveur concret est `T` ou `*T`. Une variable satisfait une méthode `*T` : il n'y a pas d'opérateur `&`. La valeur passée est une copie. L'interface pointe vers cette copie et vers la vtable. La copie vit le temps de l'appel. Une interface née là ne sort pas de l'appel. Un paramètre d'interface le peut. L'interface vide est refusée. Pas d'assertion de type. Une interface sans valeur est une panne hôte.

Pas d'héritage. La composition est un champ.

```
struct Boite { c Compte, etiquette string }
```

`Boite` n'a pas les méthodes de `Compte`. On écrit `b.c.debiter(1)`.
Promouvoir les méthodes du champ est refusé. L'auteur nomme le champ.

## 6. Génériques

Pourquoi. `Pile[T]` est un texte et plusieurs fonctions concrètes. Le C ne voit que ces fonctions. La contrainte est une interface, pour qu'il n'y ait pas un second langage de contraintes.

Un struct ou une fonction peut prendre des types. Ils sont instanciés à la compilation.
La seule contrainte est une interface. Pas de spécialisation, pas de variadique de types, pas de code à la compilation. `comptime` n'existe pas.

Le paramètre s'écrit `T`, ou `T Interface`. Plusieurs paramètres se séparent par une virgule.
L'instanciation s'écrit au site : `Pile[int]`, `identique[int](v)`. Elle n'est pas devinée.
Une méthode reprend les paramètres du struct, dans l'ordre : `func (me *Pile[T]) pousser`. Elle n'en ajoute pas.
Un paramètre ne porte pas le nom d'un type. Le message est `int est un type`.
La contrainte nomme une interface. Sinon le message est `int n'est pas une interface`.
Une méthode qui fixe le paramètre, `func (me *Pile[int]) pousser`, est `pas de spécialisation`.
Oublier l'argument est `Pile attend 1 type`. Le nombre est celui des paramètres.
Une fonction sans paramètre de type, écrite `f[int]`, est `f attend 0 type`.
Un struct sans paramètre, écrit `Compte[int]`, est `Compte attend 0 type`.
Un nom concret déjà pris est `déjà déclaré`.
Un pointeur vers le paramètre, `*T`, est `pointeur : pas dans cette version`. `*Pile[T]` reste un pointeur vers le struct.

Dans le corps, un paramètre sans contrainte se copie, se passe, se range et se retourne.
Une opération, une comparaison ou un champ sur lui est `pas une méthode`.
Avec une contrainte, les méthodes de l'interface s'appellent sur la valeur. Une méthode absente est `dire n'est pas une méthode de Parleur`.
Le type concret doit avoir ces méthodes. Sinon le message est `Bonjour n'a pas dire`.
Un argument qui est encore un paramètre porte cette contrainte, ou une interface qui en a les méthodes. Sinon le message est `U n'a pas dire`.

```
struct Pile[T] { data []T, n int }

func (me *Pile[T]) pousser(a arena, v T) {
  me.data = a.append(me.data, v)
  me.n = len(me.data)
}
```

## 7. Erreurs

Pourquoi. `error` est une valeur, elle rentre avec le résultat. Une panne de l'hôte arrête le processus : un indice hors table n'est pas une erreur que le document rattrape.

`error` est un type. `nil` veut dire pas d'erreur. `nil` est sa valeur zéro. `e := error` est `nil`.
Une erreur se crée avec `error("solde")`. Le texte est `solde`. `error("")` est `nil`.
Toute erreur de longueur nulle est `nil`. `== nil` est vrai. `or return` continue.
Elle se compare avec `==`. `error("solde") == error("solde")` est vrai. `error("solde") == nil` est faux. `!=` est la négation.
Un champ `error` se compare comme une `error`.
`(T, error)` est la seule forme à plusieurs résultats. Le second type est `error`. Une autre forme reste `plusieurs résultats : pas dans cette version`.
`appel() or return` suit un appel. Si l'appel rend `(T, error)`, l'expression vaut `T`. Si l'appel rend `error`, elle ne vaut rien. `nil` laisse continuer. Sinon la fonction en cours retourne cette erreur. Une fonction `(T, error)` rend alors la valeur zéro de `T` et l'erreur. Une fonction `error` rend l'erreur. Une fonction qui ne rend pas `error` est refusée. Le message est `or return : la fonction ne rend pas error`.
Dans une fonction `(T, error)`, `return v` rend `v` et `nil`. `return nil` et `return error("solde")` rendent la valeur zéro de `T` et cette erreur. `return appel()` reprend la paire quand l'appel rend `(T, error)`.
Un appel `(T, error)` utilisé comme `T` est refusé. Le message est `or return attendu`. Une `error` ignorée, hors `defer` et hors `thread`, est `erreur ignorée`.
`or return` retourne l'erreur de la fonction en cours.
Pas de `try`, pas de `catch`, pas de panique rattrapable.

Une panne de l'hôte arrête le processus. Indice hors table, division par zéro, arène épuisée. Un fil à moitié mort laisserait une arène.
Elle nomme le fichier, la ligne et la colonne : `why: fichier:ligne:colonne: message`.
Elle ne se rattrape pas. Ce n'est pas une erreur du document : le document a ses propres pannes, définies par l'interpréteur.

## 8. Concurrence

Pourquoi. Le fil est celui du système. Why n'a pas d'ordonnanceur : le plafond reste celui du C. L'accolade qui lance attend : l'auteur n'écrit pas de poignée. Le canal copie ou déplace, pour qu'un pointeur n'entre pas dans l'arène d'un autre fil. L'ordre du `select` est la priorité, le premier bras prêt. `image` n'est pas partagée : un seul fil interprète le monde.

Un fil se lance avec `thread appel`. Les arguments sont évalués à cet endroit, de gauche à droite. Le résultat est ignoré, y compris une erreur. Ce n'est pas `erreur ignorée`. Sans appel, le message est `thread attend un appel`.
Le fil a sa pile et son `arena thread`, qui meurt quand son appel retourne. Pas de goroutine. Pas de pile extensible. Pas de runtime d'ordonnancement.
L'accolade qui contient le `thread` l'attend. Un `if`, un `else`, un `arena`, un bras de `select` et le corps d'une fonction sont de ces accolades. Le corps d'un `for` ne l'est pas. `return` et `or return` prennent la sortie du §3. Il n'y a pas de poignée.

La fermeture est celle du §3. Elle précède l'attente. L'envoi qui n'est pas encore entré rend `error("fermé")` et la valeur n'entre pas. Une réception prend une place encore pleine. Quand il n'en reste plus, elle rend la valeur zéro de `T` et `error("fermé")`. Le stockage du canal vit jusqu'à la mort de la garde, après l'attente. Un fil du même bloc qui envoie encore voit donc `error("fermé")`. Pour que ses envois entrent avant, il est lancé dans un bloc intérieur, attendu avant que le nom du canal meure.
Un nom déclaré dans le corps d'un `for` meurt à la fin du tour. Un fil lancé dans ce corps et qui emprunte ce nom est `le pointeur ne sort pas` : l'attente est dehors.

Un argument `*T` de `thread` est `le pointeur ne sort pas`, sauf `*chan[T]`, et sauf un `freeze` qui vit dans une `arena shared` encore ouverte pendant l'appel. Passer une arène de bloc, ou `thread`, est `l'arène ne sort pas`. Passer une `arena shared` est `arène partagée`. `int`, `bool` et `u8` se copient. Les octets d'une `string` ou d'une `error` se copient pour l'appel. Une garde se déplace.

`chan[T]` prend un type. Sinon le message est `chan attend 1 type`. `c := chan[T]` ne possède rien. Il n'y a pas de canal nul. L'envoi ou la réception sur ce nom est `garde déplacée`. `c := chan[T](n)` ouvre `n` places. La file ne grandit pas. `n` nul est un rendez-vous : la valeur est copiée, puis les deux continuent. `n` négatif est la panne `taille négative`. Si l'hôte ne peut pas allouer, la panne est `arène épuisée`. À l'instanciation, la valeur suit la règle de son type concret.

Le canal est une garde, et il reste un nom : une variable, un paramètre ou un résultat. Un champ, l'élément d'une tranche, la clé d'une map et la valeur d'une map ne sont pas un `chan[T]`. Le message est `le canal reste un nom`. `*chan[T]` peut être un champ : c'est l'adresse du nom, pas le canal. `chan[chan[T]]` reste un nom dont l'élément est un canal.

Le copier est `la garde ne se copie pas`. `=` et `return` le déplacent. La source devient vide. Le compilateur le ferme à la fin du nom qui le tient. L'auteur n'écrit pas `fermer`. Un paramètre `chan[T]` déplace. Un paramètre `*chan[T]` emprunte et ne ferme pas. Plusieurs fils peuvent emprunter le même canal. Ce n'est pas `pointeur mutable`. L'emprunt dure jusqu'à l'attente du `thread` qui l'a reçu. Déplacer le canal avant, ou le laisser mourir avant, est `le pointeur ne sort pas`.
`send` et `receive` ont le receveur `*chan[T]`. Il n'y a pas d'autre méthode sur le canal.

`entree[T]` est une prise d'écriture. `sortie[T]` est une prise de lecture. Chacune prend un type, le même élément que le canal. Sinon le message est `entree attend 1 type` ou `sortie attend 1 type`. `entree[T](n)` et `sortie[T](n)` sont `pas dans cette version`. Il n'y a pas de `*entree[T]` ni de `*sortie[T]`. Le message est `pointeur : pas dans cette version`. `nom := entree[T]` et `nom := sortie[T]` sont la prise vide. Le mot `sortie` du §3 reste la fin d'un bloc. Le type s'écrit `sortie[T]`.

La prise vide se copie, se passe et se rend. Elle ne possède pas la file. Ce n'est pas un canal nul, et ce n'est pas `garde déplacée`. `n.c = src` relie la prise quand `n.c` est une `entree[T]` ou une `sortie[T]` et que `src` est un `chan[T]` du même élément. La liaison copie le pointeur du canal. Elle ne déplace pas `src`. `src` garde l'envoi et la réception, et il ferme encore le canal à sa mort. Un `chan[T](n)` sans nom ne tient pas cette liaison. Le propriétaire est un nom. Le message est `le pointeur ne sort pas`.

Avant la liaison, `send` et `receive` rendent `error("pas relié")` et la valeur n'entre pas. Après la liaison, l'opération va dans la file de ce canal. `entree[T]` n'a que `send`. `sortie[T]` n'a que `receive`. L'autre nom n'est pas une méthode. Quand le nom qui tient le canal meurt, un fil lancé dans le bloc de ce nom voit `error("fermé")` : la fermeture précède l'attente. Une prise dont le stockage survit à ce nom est `le pointeur ne sort pas`. Le compilateur refuse aussi quand il ne sait pas si la prise est encore vide.

Une tranche ou une map nommée tient ses prises aussi longtemps que ce nom. `xs[i].c = src` et `m[k] = src` relient comme `n.c = src`. Plusieurs éléments peuvent nommer le même canal. Copier l'en-tête vers une vie plus longue, le rendre, ou le passer à une fonction qui le garde, est `le pointeur ne sort pas`. Un indice dont la base n'est pas un nom suivi reste refusé.

Une prise vide peut sortir. Rendre une prise reçue en paramètre est admis : l'appelant tient le nom. Relier une prise à un `*chan[T]` emprunté, puis la rendre à l'appelant, est admis. Une méthode qui ouvre un canal et le range dans un champ du receveur est `le pointeur ne sort pas`, parce que le nom meurt à la fin de la méthode. Passer une prise liée à un `thread` lancé dans le bloc du nom suit la règle de `*chan[T]`. Déplacer le nom vers une vie plus courte que la prise est `le pointeur ne sort pas`.

Dans un struct envoyé, une `entree[T]` ou une `sortie[T]` se copie. Elle ne ferme pas le canal. Le struct n'est pas une garde pour cette prise.

`c.send(v)` rend `error`. La file pleine bloque. Ce n'est pas une erreur. `nil` veut dire que `v` est entré. `c.receive()` rend `(T, error)`. La file vide bloque. `nil` veut dire que la valeur est reçue. Après la fermeture, l'envoi rend `error("fermé")`. Chaque réception rend une place encore pleine, puis, quand il n'en reste plus, la valeur zéro de `T` et `error("fermé")`.
L'envoi copie un `int`, un `bool`, un `u8`. Il copie les octets d'une `string` ou d'une `error`. Il déplace une garde. Une tranche, une map, un pointeur ou une interface passe s'il est `freeze` et qu'il vit dans une `arena shared` encore ouverte à la réception. Sinon c'est `le pointeur ne sort pas`. Un struct se traite champ par champ. Une valeur qui a encore un alias mutable est `alias`.
La réception d'une `string` ou d'une `error` copie comme `[]u8` : dans l'arène du bloc courant, ou sur la pile de l'appel s'il n'y a pas de bloc. La copie de la pile ne sort pas de l'appel.
Plusieurs fils bloqués sur le même canal sont servis dans l'ordre d'arrivée.

`p := freeze(x)` déplace `x`. Sans valeur, le message est `freeze attend une valeur`. En tête d'énoncé, hors du `:=` qui la définit, elle est `freeze attend un :=`. `freeze` marque le stockage. Il ne change pas d'arène et ne rend pas une arène privée partageable. Une écriture qui atteint ce stockage est `freeze`, y compris dans le fil qui l'a ouvert. L'envoi et la réception écrivent le canal : un canal `freeze` les refuse. S'il reste un alias mutable, le message est `alias`.

`arena shared nom { }` meurt à l'accolade, après l'attente des fils lancés dedans. `nom.make` et `nom.append` restent sur le fil qui a ouvert le bloc. Un autre fil reçoit une copie, ou lit un `freeze`.

Le seul fil qui appelle `nom.make` ou `nom.append` est celui qui a ouvert le bloc. Un fil lancé dans le bloc ne peut pas y appeler `make` ni `append` : lui passer `nom` est `arène partagée`, comme le refuse `thread f(s)`. Un appel du même fil passe `nom` comme une arène ordinaire, et `a.make` y est légal.

« Encore ouverte pendant l'appel » et « encore ouverte à la réception » veulent dire pour le vérificateur que l'arène est sur la pile du bloc quand le fil est lancé : l'accolade attend le fil avant `why_arena_free`, donc le stockage est vivant pendant le fil. Un `freeze` né dans le bloc et lu par un fil de ce bloc passe. Une valeur qui sort du bloc pour être lue dehors suit la règle du §3 : `la tranche ne sort pas` pour une tranche, `le pointeur ne sort pas` pour un pointeur.

Le nom `nom` n'est pas visible par un fil lancé dans le bloc : il est local à l'accolade et meurt avec elle. Le fil ne voit que la valeur `freeze` qu'on lui a passée, qui nomme le même stockage. Passer le nom `nom` lui-même, au lieu d'un `freeze`, est `arène partagée`.

`for v in c` reçoit jusqu'à la fermeture. `v` a le type `T`. Les places encore pleines sortent, puis la boucle s'arrête. `error("fermé")` n'est pas une valeur du corps. Affecter `v` n'envoie rien. `for i, v in c` est `le canal n'a pas d'indice`.

`select` rend une `error`. Chaque bras a un bloc. Un bras est `case v := c.receive()` ou `case c.send(v)`. Sinon le message est `le bras attend un canal`. Les canaux des bras sont évalués de gauche à droite avant l'attente. La valeur envoyée n'est évaluée que si ce bras court. Le premier bras prêt, dans l'ordre du texte, court. Un bras ne satisfait pas un autre bras du même `select`. `v` est un `T` : le bras ne court que pour une valeur reçue. Un canal fermé et vide ne rend pas le bras prêt. Un canal fermé qui a encore une place rend le bras de réception prêt. Un canal écrit en premier qui reste prêt garde les suivants en attente. Si aucun bras ne peut plus avancer, `select` rend `error("fermé")`. S'il peut encore arriver un envoi, il bloque. `or return` peut suivre le `select`, comme il suit un appel. Le bras qui court a consommé l'erreur de l'envoi ou de la réception. Pas de `default`. Sans bras, le message est `select attend un bras`. `case` hors d'un `select` est `case hors select`.
Le choix du `select` est l'ordre du texte. L'ordre entre deux fils est celui du système.

Un envoi que personne ne reçoit, ou une réception que personne ne nourrit, bloque le processus à l'attente du bloc. Pas de détecteur.

```
struct Nod { c entree[int] }

func lier() error {
  src := chan[int](1)
  n := Nod
  e := n.c.send(1)
  if e == nil { return error("vide") }
  n.c = src
  n.c.send(2) or return
  v := src.receive() or return
  if v != 2 { return error("non") }
  return nil
}
```

`n := Nod` laisse `c` vide. `n.c.send(1)` est `error("pas relié")`. `n.c = src` relie, et `src` reste le nom qui ferme. Une prise de lecture s'écrit `sortie[int]`. `s = src` la relie de la même façon.

```
func ajouter(c *chan[int], n int) error {
  c.send(n) or return
  return nil
}

func somme() error {
  c := chan[int](0)
  thread ajouter(c, 20)
  thread ajouter(c, 22)
  a := c.receive() or return
  b := c.receive() or return
  if a + b != 42 { return error("non") }
  return nil
}
```

```
func suivre(c *chan[int]) int {
  s := 0
  for v in c {
    s = s + v
  }
  return s
}
```

```
func lire(urgent *chan[int], reste *chan[int]) (int, error) {
  select {
  case v := urgent.receive() {
    return v
  }
  case v := reste.receive() {
    return v
  }
  } or return
}
```

Un programme peut garder une arène et un seul fil. Le langage ne l'exige pas. Le document `.oo` refuse la concurrence. Une panne dans un fil arrête le processus.

Le paquet `serveur` accepte et démarre un fil par connexion. `ServeConn(ecoute, app, n)` sert exactement n connexions et rend quand les n fils sont finis. Le paquet `client` envoie des octets et lit la réponse dans un tampon. L'épreuve lance deux clients vers un serveur sur `127.0.0.1` ; la somme des deux états est 42.

`Open(chemin)` ouvre un fichier du disque. `(Fd) Read` écrit dans le tampon de l'appelant et rend le nombre d'octets. Zéro est la fin, pas une erreur. Un compte plus court que le tampon est normal : l'épreuve relance `Read`. `Close` ferme le descripteur et rend une `error`. L'épreuve ouvre le fichier `data` de son répertoire, lit jusqu'à la fin, et le code de sortie est la somme des octets.

`Lire(a, chemin)` rend tout le fichier dans l'arène de l'appelant. `Ecrire(chemin, buf)` remplace le fichier. L'épreuve écrit l'octet 42, le relit, et le code de sortie est cette somme.

`Seek(n)` place la prochaine lecture à `n` octets depuis le début et rend la position atteinte. `Tell` rend la position courante et ne la bouge pas. `n` négatif est `error("refuse")`. La façade n'a pas de tampon caché. L'épreuve ouvre un fichier fixé, pose au milieu, lit la fin ; la somme des octets lus est le code de sortie.

La somme en N fils : le parent calcule des bornes qui partagent le fichier, ferme son descripteur, et lance un fil par intervalle. Chaque fil ouvre, pose, lit son morceau et envoie la somme des chiffres. Le parent reçoit N fois et additionne. Le canal est une file de N places. Pas de verrou. Le code de sortie est la somme des sommes.

TLS : `DialTls(hote, port)` et `AcceptTls(ecoute)` font le handshake et rendent un `Fd` chiffré. La lecture et l'écriture passent par le même `Fd`, sans changer d'appel. Le certificat auto-signé est embarqué dans le binaire ; le client ne vérifie pas le nom. L'épreuve est la même que Serve : deux clients, la somme des deux états est 42.

## 9. Étranger

Pourquoi. `extern` est une signature écrite à la main. Why ne parse pas les en-têtes du C. `defer` rend ce que C a alloué, parce que l'arène ne libère que ce qu'elle a créé.

`extern func` déclare une fonction C, signature écrite à la main.
Why ne libère pas la mémoire allouée par C. `defer` le fait.
Pas d'en-tête parsé.
Un `extern` prend et rend `int`, `string` et `[]u8`. Un autre type est refusé. Le message est `extern attend int, string ou []u8`. Sur une paire, il pointe la `(`.
Une `string` passée à C est le pointeur des octets, puis leur nombre. Why n'ajoute pas l'octet nul. La fonction C copie et ajoute le nul si le système l'exige.
Un `[]u8` passé à C est le pointeur des octets, puis leur nombre. Ces octets survivent à l'appel, sur la pile ou dans une arène. C écrit dedans. Il ne les alloue pas.
Une `string` ou un `[]u8` rendu par C est le pointeur des octets, puis leur nombre. Why en fait une valeur. Il n'ajoute pas l'octet nul et ne rattache pas ces octets à une arène. La fonction C ne rend pas un pointeur pris sur un argument.

## 10. Produit

Pourquoi. Le `.wo` est un binaire natif, sans runtime Why. `why run` sur un répertoire compile et lance. `why run monde.oo` peut passer un document au `.wo` déjà là. Éditer ce fichier ne recompile pas le programme.

`why build [répertoire]` lit les `.wc` d'un répertoire et écrit un `.wo`.
`why check [répertoire]` vérifie ces `.wc`. Il n'écrit pas de `.wo`.
Le répertoire absent est le répertoire courant.
Les diagnostics vont sur la sortie d'erreur. `code non exécuté` ne refuse pas le paquet.
La langue du message est choisie au démarrage du processus `why`. L'ordre est `LC_ALL`, puis `LC_MESSAGES`, puis `LANG`. Une variable vide laisse la suivante. La langue est le morceau avant `_` et avant `.`. `fr` choisit le français. `C`, `POSIX`, une autre langue, ou l'absence de ces variables, choisit l'anglais. L'anglais est le défaut.
Les phrases citées dans cette spécification sont la forme française. Le texte traduit est le message après `fichier:ligne:colonne`, les messages de la commande (`il manque main`, `il manque le .wo`, `document absent`, l'usage), et les pannes de l'hôte. Les mots du langage restent : `garde`, `entree`, `sortie`, `arena`, `freeze`. La position ne change pas.
Une panne hôte est un littéral écrit dans le C au moment de `why build`. Le `.wo` ne relit pas la locale. Un binaire compilé en anglais dit la panne anglaise sur une machine française.
`why play` suit la langue de la page pour la vérification et l'émission de ce fragment. Le `.wo` lancé ensuite garde cette langue.
Sans `main`, le `.wo` est une lib. Avec `main`, c'est un binaire.
Un binaire peut lier des libs `.wo`. Le format est un seul fichier, sans runtime Why.
Les arènes sont des appels insérés par le compilateur, pas une bibliothèque dynamique.

`why run [répertoire]` écrit le même `.wo` que `why build`, puis le lance.
Le répertoire absent est le répertoire courant. Les arguments qui suivent sont ceux du processus.
Le processus part du répertoire du paquet.
Le code de sortie est le sien. Sans `main`, la commande refuse.
`why run monde.oo` charge le `.wo` courant et lui passe le document.
Il ne compile pas. Il lance le `.wo` déjà écrit dans le répertoire courant, sous le nom de ce répertoire. Le chemin du document est l'argument du processus. Le processus part de ce répertoire. Le code de sortie est le sien.
Sans ce `.wo`, le message est `il manque le .wo`. Sans le fichier, le message est `document absent`.
L'interpréteur ouvre ce chemin. Sans argument, il ouvre le fichier `data`.
Le `.oo` n'est pas lié dans le `.wo`. Le remplacer ne recompile pas le programme. Cette commande est une possibilité. Le langage ne la rend pas obligatoire.

`why play` sert une page locale. Chaque page est un fragment avec un `main` ; le résultat est le code de sortie, ou le diagnostic.
Le fragment est seul : il n'y a pas de répertoire à importer. Le seul paquet visible est le paquet fixe `lib`, sans `main`, importé par le chemin `lib`. `lib.Reponse()` appelle la fonction exportée par son qualificateur, et sort 42. `lib.Lire(doc)` charge un fichier fixé dans une tranche née dans l'arène `doc`, et `lib.Octets(buf)` somme les octets. Code de sortie 42. Le chemin n'est pas un paramètre : le paquet lit le fichier `data` du dossier de l'épreuve, et rien d'autre. Il n'est pas le paquet `fichier` de `lib-spec.md`.
Ce qui reste refusé : un nom minuscule de l'autre paquet, `basse : minuscule, pas visible hors du paquet` ; un champ, une méthode, un nom de struct venu de l'autre paquet. Seule la fonction exportée du premier niveau franchit la frontière.

## 11. Le document `.oo`

Pourquoi. Un document `.oo` est une possibilité. SemCards, le prototype, peut s'en servir. La carte a un nom, un prototype, des slots, des méthodes. Ce n'est pas du Why : l'auteur d'une carte ne choisit pas une arène. `arena` n'est pas un mot de `.oo`.

Un fichier `.oo` est une suite d'objets. L'indentation est le bloc.
`//` commente jusqu'au bout de la ligne. Les tabulations sont refusées.
L'image chargée au boot est la copie. Le fichier reste la vérité.
Le programme ne crée pas d'objet, n'en libère pas, et ne s'inspecte pas.

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

Un objet a un nom, un prototype optionnel, des slots et des méthodes.
`object MillIn : Stack` lit `qty` sur `Stack` tant que `MillIn` ne l'a pas écrit.
L'écriture tombe toujours sur le receveur. `me.qty = 0` dans une méthode de `MillIn` crée le slot là. Le parent ne change pas.

Un slot imbriqué est un objet fils, né au chargement, absent de la table de tête.
Son genre est le nom du prototype. Le slot `home` pointe vers le père.

```
object Bake
  stock: Stack
    qty: 1600000
    value: 141888
```

Une méthode est `on nom (params):`. Il n'y a pas de fonction, pas de `return`.
La valeur de la méthode est la dernière valeur calculée.
Une assignation vaut la valeur assignée.
Un `if` sans `else` dont la condition est fausse vaut `nothing`.

Les noms se résolvent dans cet ordre : le local, le slot de `me` en remontant les parents, l'objet de tête.
`qty := 1` écrit un local et masque le slot. Pour écrire le slot, on écrit `me.qty = 1`.

Les valeurs sont `nothing`, `true`, `false`, l'entier, le texte, la liste, l'objet, le canevas.
L'entier est le seul nombre. `/` et `%` tronquent. Un négatif s'écrit `0 - n`.
`if` n'accepte qu'un booléen. `==` compare deux valeurs de même genre.
`!=`, `<`, `>`, `<=`, `>=`, `&&`, `||`, `!` sont les mêmes signes que dans l'hôte.

La liste est le seul agrégat. `[a, b]`. `add` déplace l'élément déjà présent vers la fin.
`remove`, `length`, `at`. `for x in liste:` copie la liste avant de marcher.
`length` rend le nombre d'éléments. `at(n)` rend l'élément à `n`, zéro est le premier. Hors liste est une panne de l'hôte.
`add(x)` et `remove(x)` rendent nothing. `remove` retire la première occurrence ; l'élément absent est une panne de l'hôte.
`for x in liste:` vaut la dernière valeur du corps, ou nothing si la liste est vide.
Une liste n'est égale qu'à elle-même. Deux textes sont égaux s'ils sont les mêmes octets.
Un entier a `asText`.

Le canevas n'est pas construit par le programme. L'hôte le passe à `draw`.
Les méthodes (`rect`, `text`, `frame`, `hit`, `chrome`, `card`) enregistrent des ordres que l'hôte rejoue. Elles rendent `nothing`.
`rect(x, y, w, h)`, `text(x, y, texte)`, `frame(x, y, w, h)`, `hit(x, y, w, h)`, `chrome(n)`, `card(x, y)`.
Les ordres se rejouent dans l'ordre de l'appel.

Une erreur est une panne de l'hôte : slot absent, mauvais nombre d'arguments, division par zéro, appel plus profond que 48. Le programme ne la rattrape pas.

`image.oo` réutilise la grammaire des énoncés, une ligne par slot vivant.
Ce n'est pas un second langage. C'est la copie écrite, si l'hôte sauve.

Ce que le document refuse, il le refuse pour rester le document : pas de pointeur, pas d'allocation, pas de concurrence, pas de classe, pas de générique.
La bibliothèque standard est la machine : `Part`, `Window`, `Desk`, les piles du mois du pain.

## 12. SemCards

Pourquoi. SemCards est un prototype. Il peut montrer un document. Why ne se définit pas par lui. Le graphe, s'il est chargé, est une table d'`Id` dans une arène, pour que plusieurs noms visent la même carte. La libération possible est le rechargement, une fois pour toute la table.

SemCards est un environnement possible. Why est le langage. Un programme Why peut lui servir d'hôte.
Une carte est un objet du document : un nom, un prototype, des slots, des méthodes.
L'instance est la carte chargée. Le prototype est l'objet dont elle hérite les slots non écrits.
Ce n'est pas une classe. Écrire un slot ne modifie pas le prototype.

Le graphe n'est pas fait de pointeurs Why. Il est une table dans `image`.
Une référence `.oo` est un `Id`. `Desk.windows`, `home`, une liste de `Shelf` et un `Hit` peuvent viser la même carte. Deux méthodes peuvent muter `MillIn` dans la même frame.
C'est le programme. La règle « un seul pointeur mutable » s'arrête à la table.
Dedans, l'alias est la sémantique : la lecture remonte, l'écriture tombe sur le receveur.
L'`Id` ne se libère pas. Il meurt avec `image`, et l'hôte lâche toute la table d'un coup.

Une liste née dans une méthode et rangée dans un slot naît dans `image`.
L'auteur `.oo` ne choisit pas l'arène. La primitive qui stocke copie dans `image`.
Le local meurt avec l'appel. Le compilateur Why continue de refuser qu'une tranche de `frame` sorte de son bloc. Il ne voit pas le programme `.oo`.

Le boot :

1. Ouvrir l'arène `image`.
2. Lire le `.oo`. Construire la table, les fils, les `home`, les méthodes.
3. Ouvrir l'arène `frame`.
4. Appeler le tick, puis le dessin. Vider `frame` au tick suivant.
5. Au rechargement, libérer `image` et reprendre au 1. Le fichier n'a pas changé, sauf s'il a été sauvé.

L'édition visuelle, le message unique et le champ de texte sont des cartes et des ordres de canevas.
Ils ne sont pas des constructions de Why. Les modifier, c'est modifier le `.oo` ou les primitives de l'hôte (`hit`, `chrome`, `card`), pas le langage.

## 13. Ce que Why refuse

Pourquoi. Ces refus gardent l'idée unique. Un ramasse-miettes, un borrow checker, un héritage ou un destructeur écrit par l'auteur cacheraient la mort que le bloc nomme.

- Le ramasse-miettes, y compris sur une région du programme.
- Le borrow checker et les durées de vie nommées sur les pointeurs.
- L'héritage, la surcharge, les classes abstraites.
- L'arithmétique de pointeur, l'allocation cachée, le destructeur écrit par l'auteur. La libération d'une garde est insérée par le compilateur, comme celle d'un bloc.
- Le verrou, dans le langage ou dans une bibliothèque Why. Deux fils ne partagent pas une donnée mutable. Un `extern` qui cache un verrou laisse un alias que le vérificateur ne voit pas.
- Les macros, les annotations, le code à la compilation.
- Les exceptions.
- Une seconde grammaire pour le document. `arena` n'est pas un mot de `.oo`.

## 14. Ce que cette spec n'achète pas

Pourquoi. L'interpréteur écrit en Why est le même programme, plus sec. Le plafond du C sur une méthode de quelques lignes n'est pas le but.

Un interpréteur en Why est un interpréteur plus sec. `me.qty + q` reste une recherche, une remontée de parents, un nœud.
Le plafond du C sur ce code arrive quand une méthode `.oo` est compilée.
Les méthodes font quelques lignes. Ce signal n'est pas là.
On ne réécrit pas le langage pour accélérer un prototype dont le sujet est un document.
