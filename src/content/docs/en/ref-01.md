---
title: "Lexicon"
weight: 1
---

A file reads on its own. Two spaces, a newline, `//`. The capital is the package boundary. A name does not hide another: the reader sees the single meaning.

> A `.wc` file is UTF-8. The indentation is two spaces. A tab is refused. `//` comments to the end of the line. No preprocessor, no header, no macro, no semicolon. A newline ends a statement. After an infix operator, it continues the expression.

```
func somme(a, b int) int {
  return a + b
}

func main() int {
  return somme(10, 20)
}
```

`:=` declares, `=` assigns, `==` compares. The type follows the name. Several names of the same type share the type: `a, b int`.

> An exported name starts with a capital. The package is the directory. A name resolves in the block, then in the file, then in the other files of the package, then in the imported packages. A name does not hide another. `:=` or a parameter that repeats an already-visible name is an error.

```
import "../lib" lib

func main() int {
  return lib.Reponse()
}
```

**Diagnostic.** `basse : lowercase, not visible outside the package` — a lowercase name from another package is refused. Two imports of the same name are an error. An import cycle is an error. An imported package that has a `main` is refused: `import lib : the package has a main`.

**Reserved words.** `func struct interface arena defer if else for return or nil true false extern freeze shared thread map chan select case import entree sortie garde`

**Not in this version.** The tab, the semicolon, the block comment, the preprocessor.
