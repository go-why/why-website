---
title: "Why"
weight: 0
---

Why is a programming language. Its surface is close to Go: the signs are those of C, the declarations are those of Go (the name, then the type). The object is a copied struct, without inheritance. The product is a native binary, without a runtime.

The one added idea — the only one — is the `arena` block. The author names the closing brace that frees the memory; he does not write `free`. There is no garbage collector, no borrow checker, no inheritance, no destructor written by the author.

| Extension | Role |
|---|---|
| `.wc` | Why source code. |
| `.wo` | The binary or the library that `why build` produces. |
| `.oo` | A document. Loaded by a program, not compiled. |

The binary is called `why`. The spec that is the reference is [why.md](why.md).

## The why

The language is called Why because each concept states its reason. The rule decides; the reason explains. It is written in [why.md](why.md), at the start of each section, and restated here.

### Three files

The source code (`.wc`) compiles into a binary (`.wo`). A binary can, at runtime, load a document (`.oo`). Editing the document does not require recompiling the binary. The file remains the source of truth; the image in memory is its copy.

### Lexicon

A `.wc` file is read without a preprocessor: two-space indentation, a newline ends a statement, `//` comments to the end of the line. A name that starts with a capital is exported — that is the package boundary, without a `public` keyword. A name does not shadow another visible name: the reader always sees a single meaning.

### Values

Why has a single numeric type: the machine-word integer. `string` is a sequence of bytes of known length, not Unicode text. The header of a slice or a map carries the name of the arena that allocated it, so that the life of the bytes is visible in the text. A map does not grow: accessing an absent key is a fault, not a hidden allocation.

### Memory — the `arena` block

The `arena` block is the single idea added by Why. The author names the closing brace that frees the memory; he does not write `free`. Three levels of release exist:

- **The call stack** — freed at the return of the function.
- **The `arena` block** — freed at the close of the block, by a release the compiler inserts.
- **`arena thread`** — freed at the death of the thread.

```
func main() {
  arena doc {
    buf := read("a.txt") or return
    ls := parse(buf)
    afficher(ls)
  } // one release, for the whole document
}
```

### Guard

A guard is a struct that owns its storage (a slice, a map, a channel). The compiler inserts the release at the end of the scope of the name that holds the guard. The author does not write that release: it is not a destructor. `return` and `=` move the guard; the source becomes empty.

### Functions and methods

There is a single form, `func`. A method is that form with a receiver `me`. `or return` propagates the error, instead of a comparison after each call.

```
func (me *Compte) debiter(m int) error {
  if me.solde < m { return ErrSolde }
  me.solde -= m
  return nil
}
```

### Interfaces and composition

An interface is a list of methods. The struct stays in its package; the caller sees only the methods. Composition names the field: `Box` is not an `Account`. No inheritance, no method promotion.

### Generics

A generic type such as `Stack[T]` is instantiated into concrete functions at compile time. The generated C sees only those functions. The only constraint one can impose on `T` is an interface: there is no second constraint language.

### Errors

`error` is a value, like the others. A function returns `(T, error)`; the caller compares with `==`. `or return` propagates the error of the current function. A host fault (index out of bounds, division by zero, arena exhausted) stops the process: it is not an error the program can catch.

### Concurrency

Why uses the system threads, no goroutines, no scheduler. The performance ceiling stays that of C. A channel copies or moves values, so that a pointer does not enter another thread's arena.

- `thread call` launches a thread and waits for it at the brace.
- `chan[T](n)` opens a bounded queue of `n` slots.
- `for v in c` receives until the channel is closed.
- `select` waits on channel arms; the first ready, in text order, runs.
- `freeze` marks a storage as immutable; a write that reaches it is an error.
- `arena shared` lets two threads read the same arena by `freeze` or by channel.

### Calling C

`extern` declares a C function with a hand-written signature. Why does not parse C headers. `defer` frees memory allocated by C, because the arena only frees what it created itself.

### Product

The `.wo` file is a native binary, without a Why runtime. `why run [directory]` compiles and runs the program. `why run monde.oo` runs the `.wo` already written in the current directory and passes it the document. Editing the `.oo` does not recompile.

### The `.oo` document — a possibility, not yet implemented

A `.oo` document is a possibility offered to Why programs. The card has a name, a prototype, slots, methods. It is not Why: the author of a card would not choose an arena. The object graph would be a table of identifiers in an arena, so that several names target the same card. The release of the graph would be at reload, once for the whole table.

### Rejections

A garbage collector, a borrow checker, an inheritance, or a destructor written by the author would hide the death that the `arena` block names. That is why Why rejects them.

### Interpreter

An interpreter written in Why would be the same program, more concise. The C ceiling on a few-line method is not the goal. One does not rewrite the language to speed up a prototype whose subject is a document.

## Tour

The tour is an interactive execution in the browser. It is opened at [play.why.noematic.eu](https://play.why.noematic.eu).

The challenges are the practice: each level gives a goal and a constraint, and you write the code. They are opened at [defi.why.noematic.eu](https://defi.why.noematic.eu).

Each page has a title, a lesson in French, a lesson in English, and a code fragment with a `main`. The page shows the output code, or the diagnostic if the construction is refused.

The project is not open source for now. A question, or an interest in the code: [contact@noematic.eu](mailto:contact@noematic.eu).

## Reference

Three texts have three roles.

**`why.md`** decides. A missing behavior is added there in the same change as the code. The compiler does not describe a behavior this spec does not fix.

**The tour** makes a construction run, one page at a time, on the already-compiled subset.

**The reference** is written to be read. It follows the order of `why.md`. Each page starts with the why of the concept, then restates the sentence of the spec, a fragment of the tour or of `testdata/`, and the diagnostic when the construction is refused. A construction written but not yet compiled is marked `not in this version`. Files, the network, JSON and formatting are a library; they do not enter the reference of the language. See [ref/](ref/README.md).

### State of this version

Compiled: functions, structs, methods, interfaces, slices, maps, `arena` block, `arena thread`, `defer`, `error`, `or return`, stored pointer, guard, type parameters on a struct and on a function (the only constraint being an interface), `thread call`, `chan[T](n)`, `for v in c`, `select`, `freeze`, `arena shared`, `import`.

Not yet compiled: the `.oo` document.

## Four languages

The close surface is that of Go. The ceiling aimed at is that of C. The object is a copied struct. The construction these four languages do not have together is the block that frees.

| | C | C++ | Java | Go | Why |
|---|---|---|---|---|---|
| Memory | `malloc`, `free` | destructor, RAII | garbage collector | garbage collector | call stack, `arena` block, `arena thread`, guard |
| Function | one form, macros beside | overloading | method in the class, overloading | `func`, method outside the type | one form, `func`. Method `func (me *T) name` |
| Assembly | `struct` | class, inheritance | class, inheritance, named interface | `struct`, embedding, structural interface | copied `struct`, named field, structural interface |
| Error | return code | exception | exception | `(T, error)`, compared by hand | `(T, error)`, propagated with `or return` |
| Concurrency | POSIX thread | `std::thread` | VM thread | goroutine, scheduler | system thread, bounded channel |
| Generic | `void *`, macro | template | erased generic | generic | type constrained by an interface, instantiated at compile time |
| Text | preprocessor, header | preprocessor, template | annotation | single file | `.wc` file, two spaces, no macro |
| Product | the program | the program | the program | the program | the program |

A method call on a field names the field: `b.c.debit(1)`. An interface receives a copy of the struct when the methods match. The call through the interface goes through a vtable; the call on the struct stays direct.

A host fault — index out of bounds or division by zero — stops the process. The message is `why: file:line:column: message`. It is not an error the program catches.

`extern func` declares a C function, hand-written signature. It takes and returns `int`, `string` and `[]u8`. Why does not free memory that comes from C; `defer` will, at the exit of the block, before the release of the arena.
