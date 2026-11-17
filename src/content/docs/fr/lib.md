---
title: "Librairies"
weight: 30
---

# Librairies — spec 0

Ce fichier propose les librairies. Il ne change pas le langage.
Chaque paquet dit son why. La règle du langage reste dans `why.md`.
`why.md` gagne en cas de conflit. Rien ici n'est compilé tant que la phrase correspondante n'est pas dans `why.md` et que le code va avec.

Ces paquets parlent au système. Ils ajoutent des valeurs faites des types du langage. Ils n'ajoutent pas un genre.
Ils ne sont pas la machine du document `.oo`. `Part`, `Window` et `Desk` restent dans le prototype SemCards, s'il charge un `.oo`.

Les essais qui compilent aujourd'hui sont dans `why-libs`, à côté de ce dépôt.
`extern` prend et rend `string` et `[]u8`, en plus de `int`. Les essais de `why-libs` ne voient encore que des handles.
Ces essais ne s'appellent pas `Read`. Les paquets de ce fichier attendent leurs fonctions.

Le tour de `why play` a cette page : `lib.Lire(doc)` charge le fichier fixé dans une tranche née dans l'arène `doc`, et `lib.Octets(buf)` somme les octets. Code de sortie 42. Elle passe par le paquet fixe embarqué `lib`, pas par le paquet `fichier` de ce fichier, dont `Read` attend encore.
Le terminal, le client et le serveur sont des binaires. Ils lisent un tube, ou ils parlent à `127.0.0.1`. Ils n'entrent pas dans un fragment coupé à 2 s.

## 1. Découpage

Pourquoi. Le système a une seule façade, `os`. Les quatre autres paquets parlent à `os`, pas au système : un changement de façade ne réécrit pas `fichier`, `terminal`, `client` ni `serveur`. Le handle est un `int`, pour que Why ne voie pas le pointeur du C.

Une librairie Why est un répertoire, donc un paquet, sans `main`. Le `.wo` est une lib.
Le programme qui s'en sert a le `main`. Il lie ces libs. Le format reste un seul fichier, sans runtime Why.

Tant que `import` n'est pas compilé, une épreuve tient dans un seul répertoire : les `.wc`, le `.c`, et le `main`. Les noms ne s'y répètent pas.
Le découpage en paquets date du jour où `import` compile. Ce jour-là, `why build` compile aussi les `.c` des paquets importés et les lie au binaire. Une lib `.wo` seule ne contient pas la façade.

Cinq paquets. Une seule façade.

| Paquet | Rôle |
|---|---|
| `os` | Le handle, les appels, les erreurs. |
| `fichier` | Read et écrire un fichier entier. |
| `terminal` | Assembler une ligne depuis l'entrée. |
| `client` | Envoyer des octets et lire la réponse. |
| `serveur` | Accept, et laisser l'application choisir la réponse. |

`fichier`, `terminal`, `client` et `serveur` n'appellent pas le système. Ils appellent `os`.

## 2. Façade

La façade est `os/os.c`. Elle est écrite à la main. Why ne parse pas ses en-têtes.
Les handles Why sont des `int`. Le pointeur réel, s'il y en a un, reste dans une table de la façade. C'est le même dessin que la fenêtre de `todo`.

```
struct Fd { n int, tls int }
```

`n` est le descripteur, ou l'indice dans la table TLS. `tls` vaut 0 pour un descripteur brut.
Why ne voit pas le descripteur brut d'une session TLS. Le socket reste dans la façade.
`Fd` se copie. La copie désigne le même handle. `Close` deux fois est une erreur `error("ferme")`.

Le zéro est un handle valide : l'entrée standard. Un échec d'`Open` ne se dit pas avec un `Fd` à zéro. Il se dit avec `error`.

Les fonctions C ont un nom préfixé. `open` est déjà le nom du système.

```
extern func os_open(chemin string) int
extern func os_creer(chemin string) int
extern func os_close(fd int) int
extern func os_read(fd int, buf []u8) int
extern func os_write(fd int, buf []u8) int
extern func os_taille(fd int) int
extern func os_poser(fd int, n int) int
extern func os_lieu(fd int) int
extern func os_dial(hote string, port int) int
extern func os_listen(port int) int
extern func os_accept(fd int) int
extern func os_tls_dial(hote string, port int) int
extern func os_tls_accept(fd int) int
extern func os_tls_close(id int)
extern func os_tls_read(id int, buf []u8) int
extern func os_tls_write(id int, buf []u8) int
extern func os_brut(fd int) int
extern func os_cuit(etat int) int
```

Un retour négatif est une erreur, jamais un handle.

| Code | Erreur Why |
|---|---|
| `-1` | `error("absent")` |
| `-2` | `error("refuse")` |
| `-3` | `error("coupe")` |
| `-4` | `error("plein")` |
| `-5` | `error("ferme")` |

Le code tient dans l'`int` rendu. La façade ne le republie pas par une variable globale.
Une panne hôte reste une panne hôte. Un fichier absent n'arrête pas le processus.

`os_read` et `os_write` font un seul appel système. Ils rendent le nombre d'octets. Zéro en lecture est la fin, avec un code 0, pas une erreur.
Un compte rendu plus petit que le tampon est normal. La boucle qui recommence est en Why.
Si `os_write` rend 0 alors qu'il reste des octets, Why en fait `error("coupe")`.

`os_taille` vaut pour un fichier régulier. Sur un tube ou un socket, elle rend `-2`.

`os_poser` place la prochaine lecture à `n` octets depuis le début et rend cette position. `n` négatif rend `-2`. Au-delà de la fin, la position est posée et le rendu est cette position. `os_lieu` rend la position courante et ne la bouge pas. Zéro est le début du fichier, pas une erreur. Sur un tube ou un socket, les deux rendent `-2`. Si la position ne tient pas dans un `int`, le code est `-4`. Un descripteur fermé rend `-5`.

Une `string` passée à la façade est un pointeur et une longueur. Elle n'a pas d'octet nul.
La façade copie le chemin, ajoute le nul, et passe cet octet au système. Au-delà de 4096 octets, le chemin est `error("plein")`. La façade n'alloue pas ce chemin dans le tas.

Le tampon `[]u8` vient d'une arène qui survit à l'appel. La façade y écrit. Elle ne l'alloue pas, elle ne le libère pas.
La mémoire qu'elle alloue pour son propre compte, la session TLS, le `termios`, meurt par `defer`, pas par l'arène.

TLS se lie à part. Le fichier `link` du paquet, une ligne par drapeau, est passé au sidecar (`-I`) et à l'édition de liens (`-L`, `-l`). L'épreuve `testdata/tls` nomme OpenSSL ainsi. Le source Why ne change pas entre le clair et TLS.

`os_brut` met le descripteur en mode brut et garde l'ancien état dans la table. `os_cuit` le rend. Why ne nomme pas `termios`.

## 3. os

`os` enveloppe la façade. Les noms exportés commencent par une majuscule.

```
func Open(chemin string) (Fd, error)
func Create(chemin string) (Fd, error)
func (me *Fd) Close() error
func (me *Fd) Read(buf []u8) (int, error)
func (me *Fd) Write(buf []u8) (int, error)
func (me *Fd) Seek(n int) (int, error)
func (me *Fd) Tell() (int, error)
func Size(f Fd) (int, error)

func Stdin() Fd
func Stdout() Fd
func Stderr() Fd

func Dial(hote string, port int) (Fd, error)
func DialTls(hote string, port int) (Fd, error)
func Listen(port int) (Fd, error)
func Accept(s Fd) (Fd, error)
func AcceptTls(s Fd) (Fd, error)

func Raw(f Fd) (Term, error)
func (me *Term) Restore() error
```

`Stdin`, `Stdout` et `Stderr` sont les descripteurs 0, 1 et 2.
`defer f.Close()` lance l'appel et ignore son `error`. L'erreur qui compte est celle de `Read` ou d'`Write`, rendue avant la sortie du bloc.
`DialTls` et `AcceptTls` posent `tls` à 1. `Read`, `Write` et `Close` lisent ce champ et appellent la fonction claire ou la fonction TLS.

`WriteAll` recommence `Write` jusqu'à la fin du tampon.

```
func WriteAll(f Fd, buf []u8) error
```

`defer f.Close()` est l'usage. `defer` court à la sortie du bloc, avant la libération de l'arène.
`Close` sur l'entrée standard est permis. Aucune fonction de `terminal` ne le fait.

`Seek` et `Tell` sont la position du descripteur. `Seek` compte depuis le début et rend la position atteinte. `Tell` ne bouge rien. `n` négatif est `error("refuse")`. Au-delà de la fin, la position est posée et la lecture suivante rend 0. Un tube ou un socket rend `error("refuse")`. Une position qui ne tient pas dans un `int` est `error("plein")`. Un descripteur déjà fermé rend `error("ferme")`. Zéro est le début du fichier, pas une erreur.

`Read` et `Write` avancent cette position du nombre d'octets rendus. La façade n'a pas de tampon caché. Le programme qui découpe additionne ces nombres, ou il appelle `Tell`.

Un `Fd` copié désigne le même descripteur, donc la même position. Deux fils ne s'en servent pas ensemble. Chacun ouvre le chemin. Le vérificateur ne voit pas le descripteur du système.

La méthode `(Fd) Read` remplit le tampon et avance la position. Charger tout le fichier est le rôle de `fichier.Read`, section 4. Un fichier plus grand que l'arène se lit avec `Seek` et `(Fd) Read`, par morceaux, dans un tampon de l'appelant. Le déplacement depuis la fin n'est pas dans cette coupe.

## 4. fichier

`Read` rend tout le fichier. L'arène est celle de l'appelant. La tranche rendue y vit, et elle meurt avec elle.

```
func Read(a arena, chemin string) ([]u8, error) {
  f := Open(chemin) or return
  defer f.Close()
  n := Size(f) or return
  buf := a.make([]u8, n)
  reste := buf
  for len(reste) > 0 {
    k := f.Read(reste) or return
    if k == 0 { return error("coupe") }
    reste = reste[k:]
  }
  return buf
}
```

La forme sans arène écrite dans `why.md` §4 ne se compile pas : une tranche ne sort pas de l'arène qui l'a vue naître.
Le jour où ce paquet se compile, l'exemple de `why.md` prend le paramètre `a arena`.

`Write` remplace le fichier. Il n'a pas besoin d'arène : les octets sont ceux de l'appelant.

```
func Write(chemin string, buf []u8) error {
  f := Create(chemin) or return
  defer f.Close()
  return WriteAll(f, buf)
}
```

Un tube n'a pas de taille. Il se lit avec la méthode `(Fd) Read`, pas avec la fonction `fichier.Read`.
Grandir un tampon dont on ignore la longueur attend `append`. Ces paquets ne l'inventent pas.

## 5. terminal

`ReadLine` lit l'entrée jusqu'à l'octet `10`, ou jusqu'à remplir `buf`.
Elle rend la fenêtre lue, sans garder l'octet `10`. Un tampon trop court pour la ligne donne `error("plein")`.
La fin de l'entrée au milieu d'une ligne rend ce qui a été lu, sans erreur. La fin au début rend une tranche vide et `nil`.

```
func ReadLine(entree Fd, buf []u8) ([]u8, error)
func WriteLine(sortie Fd, buf []u8) error
```

`WriteLine` verse les octets, puis l'octet `10`.
Le tampon appartient à l'appelant. Pour une ligne qui doit survivre au tampon, l'appelant copie dans son arène.

`Raw` est là pour une touche sans attendre la ligne. La boucle qui l'emploie est au programme, pas dans `why play`.
Le mode brut est rendu par `defer t.Restore()`.

## 6. client

Le client envoie un tampon et lit la réponse dans un autre. Il ne connaît pas HTTP.
Une requête qui contient `13` et `10` est un `[]u8`. Une `string` Why ne porte pas ces octets : `\` est refusé dans un littéral.

```
func Exchange(f Fd, req []u8, rep []u8) (int, error) {
  WriteAll(f, req) or return
  return ReadUntil(f, rep)
}
```

`ReadUntil` remplit `rep` jusqu'à la fin ou jusqu'au plein. Elle rend le nombre d'octets.
Si la réponse dépasse `rep`, le résultat est `error("plein")`. L'appelant choisit la capacité.
`append` raccourcira cette limite plus tard. Le paquet n'attend pas après lui pour exister.

`Dial` et `DialTls` rendent le même `Fd`. `Exchange` ne demande pas lequel des deux a couru.

`Status` est le seul savoir HTTP de cette spec. Il lit trois chiffres après la première espace. Il rend cet `int`, ou `error("coupe")` si les octets n'y sont pas. Pas d'en-têtes, pas de corps découpé, pas de texte.

## 7. serveur

Le programme ne fournit pas une fonction de rappel. Why n'en a pas.
Il fournit une valeur dont la méthode choisit la réponse.

```
interface Responder {
  Respond(a arena, f Fd, req []u8) error
}

func Serve(port int, app Responder) error
func ServeTls(port int, app Responder) error
```

`Serve` écoute, accepte, et pour chaque connexion ouvre un bloc `arena`.
Dans ce bloc, il remplit un tampon de 4096 octets avec `Read`. `error("plein")` si la requête dépasse.
Puis il appelle `app.Respond`. La méthode écrit elle-même la réponse, avec `WriteAll`, avant de rendre.
À la sortie du bloc, l'arène meurt, puis `Close` court.

Une erreur d'`Accept` ou de `Respond` arrête `Serve` et remonte. Le premier paquet ne saute pas une connexion pour continuer la suivante.

La boucle est en Why, dans ce paquet. Les appels système restent dans `os`.
Why peut écrire cette boucle parce que le bloc `arena` est un mot du langage, pas une fonction C.
La façade ne peut pas ouvrir l'arène à sa place : les arènes sont des appels insérés par le compilateur.

L'interface reçoit une copie de la valeur. Cette copie vit le temps de `Serve`.
La valeur ne porte pas de pointeur vers l'arène de l'appelant.

L'épreuve `testdata/serve` démarre un fil par connexion. Ce fil reçoit un struct concret. Une interface ne passe à un `thread` que `freeze`, dans une `arena shared` encore ouverte. `ServeTls` reste la boucle sans borne. L'épreuve TLS appelle `AcceptTls` dans `ServeConn`.
Deux fils ne se partagent pas le tampon. Une valeur qui doit les rejoindre passe par un canal, ou elle est `freeze`.

## 8. Refus

- Pas de ramasse-miettes derrière ces tampons. L'arène nommée est la durée de vie.
- Pas d'allocation cachée dans `Read`. L'arène est un paramètre.
- Pas de `char *` vu depuis Why. Le handle est un `int`, le tampon est un `[]u8`.
- Pas de valeur de fonction pour brancher le serveur.
- Pas de TLS écrit en Why.
- Pas de sélection d'événements dans le langage. L'attente est l'appel `Read` ou `Accept`.
- Pas de fil dans l'application pour servir une connexion.
- Pas de JSON, pas de formatage, pas d'Unicode. Les octets restent des octets.
- Pas de position partagée. Deux fils ouvrent deux fois le même chemin.
- Pas de page de tour pour le terminal, le client ou le serveur.

## 9. Construction

Chaque cran a son épreuve. L'épreuve lance le `.wo` et regarde le code de sortie, ou le diagnostic. Elle ne fige pas le C.

1. Arènes, `defer`, `error`, `or return`. Déjà la prochaine tranche du langage. Pas encore de librairie.
2. `Open`, `Read`, `Close`. Épreuve `testdata/fichier` : le fichier `data` (octets 10, 20, 12), somme 42. `fichier.Read(a arena, chemin)` reste le cran suivant.
3. `Lire(a arena, chemin)` et `Ecrire`. Épreuve `testdata/ecrire` : écrire l'octet 42, le relire, somme 42. L'exemple `lire` de `why.md` §4 prend l'arène. Un seul paquet : les méthodes gardent `Read` et `Write`.
4. `ReadLine`, avec un tube. Le mode brut a une épreuve qui restaure l'état même si le programme s'arrête par `defer`.
5. `Exchange` et `Serve` en clair, sur `127.0.0.1`, dans la même épreuve. Le code de sortie est l'état lu par `Status`.
6. La ligne de lien TLS. `DialTls` et `AcceptTls`. L'épreuve `testdata/tls` est celle de `Serve` : `ServeConn`, deux clients, somme 42. `ServeTls`, la boucle sans fin, n'est pas dans cette épreuve.
7. `import`, les cinq répertoires, et les `.c` des paquets importés liés au binaire.
8. `thread`. `Serve` passe à un fil par connexion. L'épreuve lance deux clients ensemble et rend la somme des deux états.
9. `Seek` et `Tell`. Ce cran suit `Open` et `(Fd) Read`. Il ne suit pas `fichier.Read`. Épreuve : ouvrir un fichier fixé, poser au milieu, lire la fin. La somme des octets lus est le code de sortie.
10. Somme en N fils. Ce cran suit `Seek`. `thread` est déjà compilé. Il n'attend pas `select`, `freeze`, `arena shared`, ni `Serve`. Le fichier, les bornes sur l'octet 10 et les envois d'`int` sont au §7 de `TODO.md`. Le code de sortie est la somme, au plus 255.

`extern` sur `string` et `[]u8` est compilé. La `fichier.Read` de ce fichier n'existe pas encore ; la `lib.Lire` du paquet fixe du tour n'est pas celle-ci. La démo qui ne voit que des `int` ne s'appelle pas `Read`.

## 10. Phrase qui reste

Les phrases d'`extern` sont dans `why.md` §9.

Dans le §4 de `why.md`, l'exemple `lire` prend l'arène de l'appelant. Le corps est celui de la section 4 : `Size`, puis `a.make`, puis `(Fd) Read` qui remplit le tampon. `(Fd) Read` n'alloue pas. La tranche rendue meurt avec `a`. L'épreuve `testdata/ecrire` nomme les fonctions `Lire` et `Ecrire`.
