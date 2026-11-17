---
title: "Performance"
weight: 40
---

Why compile en C. Le plafond de performance est celui du C. Cette page montre où Why se situe face au C, et dit clairement où il gagne et où il perd. Les chiffres de référence sont ceux du dépôt de benchmark séparé, et correspondent à l'article.

**Machine.** Darwin arm64. Apple clang 21 (`-O2`), go1.27.3, rustc 1.99.1, Odin dev-2026-10, Java 17. Why est le `.wo` de `why build`, avec les mêmes drapeaux C.

**Méthode.** best-of-5 : le minimum des 5 échantillons (robuste aux pics de la machine), après un échauffement ; `ns/op = min / N`. La machine n'étant pas isolée, un même code varie d'environ 15 à 20 % d'un run à l'autre (fréquence CPU, thermique, malloc/GC). Le drapeau `-stable` lance C et Why 3× dans l'appel et prend la médiane des 3 ratios `Why/C` : c'est le mode recommandé pour un chiffre stable.

## Premier état des mesures

C'est le même état que dans l'article. Quatre questions :

| Question | Observation |
|---|---|
| Le vérificateur refuse-t-il les stockages interdits ? | **76 programmes de non-régression** passent, rejets attendus compris. |
| Le C émis est-il au niveau du C ? | **Médiane Why/C ≈ 1,01** sur 46 noyaux de calcul entier ; écart notable sur la mise à jour de table associative (**≈ 6×**). |
| Que coûte un cycle d'allocation par région ? | **1,33×** face à `malloc`/`free` pour un lot de 4 Ko mis en pool ; **1,4 à 1,9×** pour 64 Ko libérés ; pic mémoire proche du C. |
| Des programmes réels compilent-ils ? | Un serveur de fichiers et un client/serveur TLS compilent et renvoient le code attendu. |

Il n'existe pas encore de **preuve de (E)** : la sûreté est couverte par la suite de tests, pas par un théorème. C'est une limite assumée, pas un oubli.

## L'allocateur, premier chantier

L'environnement d'exécution tient dans un en-tête de **934 lignes** : allocation par avancement de curseur, blocs de **4096 octets** recyclés dans un pool local au thread, pool de `min(cpus, 8)` threads de travail et canaux bornés. À la sortie d'un bloc, le code émis ferme les canaux, attend les tâches, exécute les `defer`, libère les gardes, puis appelle `why_arena_free`.

Le cycle d'allocation par région coûte encore entre **1,33×** (4 Ko mis en pool) et **1,4–1,9×** (64 Ko libérés) face à `malloc`/`free`. C'est le premier chantier d'optimisation désigné par les mesures.

## Course préliminaire inter-langages

Cette section provient d'une course antérieure (commit `d782924`) ; elle sert de contexte inter-langages sur une même machine. Les chiffres de référence ci-dessus viennent de la course actuelle, dont la médiane Why/C est ≈ 1,01.

**Résumé de cette course.** Sur les exemples accordés, la médiane Why/C est 1.07. Trois choses sont vraies à la fois :

1. **Au plafond du C** sur les noyaux linéaires, struct et entier — Why est à quelques pourcents du C, et plus rapide que le C sur plusieurs.
2. **Plus rapide que le C sur les cœurs cross-thread** — un pool de fils supprime `pthread_create`/`pthread_join` ; Why est là bien devant Go, Rust, Odin et Java.
3. **Plus lent que le C quand l'allocation et la croissance de map dominent** — la faiblesse honnête, la mise à jour de table associative.

| Noyau | C | Go | Rust | Odin | Java | Why | Why/C |
|---|---:|---:|---:|---:|---:|---:|---:|
| fonctions | 3.25 | 3.68 | 4.63 | 3.35 | 3.35 | 3.51 | 1.08 |
| si | 3.21 | 3.34 | 4.48 | 3.27 | 2.82 | 3.01 | 0.94 |
| boucle | 5.53 | 25.12 | 6.92 | 5.65 | 7.67 | 5.82 | 1.05 |
| indice | 5.38 | 8.43 | 8.40 | 4.84 | 4.20 | 3.23 | **0.60** |
| fenêtre | 4.82 | 8.57 | 6.98 | 5.48 | 3.85 | 5.37 | 1.11 |
| map lecture | 4.52 | 6.44 | 8.16 | 6.05 | 3.50 | 5.81 | 1.29 |
| map écriture | 5.56 | 15.65 | 15.23 | 6.14 | 11.81 | 23.34 | 4.20 |
| struct copie | 3.80 | 4.83 | 4.90 | 3.63 | 3.68 | 3.84 | 1.01 |
| méthode ptr | 3.77 | 4.56 | 5.28 | 4.00 | 3.18 | 3.63 | 0.96 |
| journal | 3.25 | 9.94 | 4.20 | 4.66 | 29.41 | 2.00 | **0.62** |
| canal rendez-vous | 14526 | 463.75 | 18133 | 26055 | 34289 | 5586 | **0.38** |
| canal file | 14796 | 433.25 | 17256 | 16692 | 36411 | 5826 | **0.39** |
| spawn fil | 15362 | 414.83 | 17345 | 20747 | 31315 | 5838 | **0.38** |
| appel générique | 3.85 | 3.93 | 4.09 | 2.92 | 3.21 | 3.50 | 0.91 |
| propagation erreur | 4.99 | 4.97 | 5.94 | 5.12 | 3.49 | 4.56 | 0.91 |
| hanoi | 671466 | 786858 | 524943 | 1034772 | 390215 | 683200 | 1.02 |

Valeurs en `ns/op`. Gras = où Why bat nettement le C.

## Le benchmark complet

La suite complète est **46 noyaux** sur sept langages plus Y, dans un dépôt séparé. La course de référence est estampillée du commit Why ; la méthodologie (drapeaux par langage, le mappage Y, les pages non mesurées) est documentée dans le README de ce dépôt.
