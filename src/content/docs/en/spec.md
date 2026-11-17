---
title: "The Spec"
weight: 10
---

# Why — spec 0

A language. The signs are those of C. The declarations are those of Go: the name, then the type.
No garbage collector, no borrow checker, no inheritance.
The only added idea is the `arena` block.

The product is the program. A `.wo` is a binary, or a lib.
SemCards is a prototype. It can load a `.oo` document, interpret it and draw it. That is an occasion. It is not the business of the language.
This spec fixes the language and the `.wo` product. The document is described in §11 and §12. It is not required.

The language is called Why. Each concept states its why: the reason it is there. The rule decides. The reason explains.

The binary is called `why`. Not `wc`: that name is the Unix command.

## 0. Three files

Why. The source compiles. The product is the program. A `.oo` can be loaded by this program. Changing it does not recompile it. If it is loaded, the file remains the truth, the image is its copy.

| Extension | What | Role |
|---|---|---|
| `.wc` | Why source | The code. Functions, structs, methods. |
| `.wo` | product | The binary, or the lib, from one or several `.wc`. |
| `.oo` | document | A possible instance. Loaded, not compiled. |

`.wc` is the only source of Why. `why build` writes a `.wo`. A lib is a `.wo` without a `main` entry. A binary is a `.wo` that has one. The loader does not distinguish them by another extension.

`.oo` is not Why. A program can load it into an arena. The language does not require it.

## 1. Lexicon

Why. A file reads on its own, without a preprocessor: two spaces, a newline, `//`. A `.oo` document may reuse this form. The capital is the package boundary, without a `public` word. A name does not hide another: the reader sees the single meaning.

A `.wc` file is UTF-8. The indentation is two spaces. A tab is refused.
`//` comments to the end of the line. There is no block comment.
No preprocessor, no header, no macro, no semicolon.
A newline ends a statement. After an infix operator, it continues the expression.

A name is a sequence of letters, digits and `_`. It does not start with a digit.
An exported name starts with a capital. The package is the directory.
A name resolves in the block, then in the file, then in the other files of the package, then in the imported packages.
A name does not hide another. `:=` or a parameter that repeats an already-visible name is an error. The name is not recreated.
A parameter may carry the name of a field: the field is written `me.nom`.

Reserved words:

```
func struct interface arena defer if else for return
or nil true false extern freeze shared thread map
chan select case import entree sortie garde
```

The import line is `import "path" name`. The path is the directory of the imported package, relative to the importing directory. The name is the one under which the package is seen. An exported name starts with a capital; a lowercase name from another package is refused: `basse : lowercase, not visible outside the package`. Two imports of the same name are an error. An import cycle is an error. An imported package that has a `main` is refused: `import lib : the package has a main`. In the package, the lowercase stays visible: it is the same namespace.

`:=` declares. `=` assigns. `==` compares.
The type follows the name, in a parameter as in a field. Several names of the same type share the type: `a, b int`. The comma between names is the list; the comma between lists is the separator of the groups. The result follows the parameters.

```
struct Compte { solde int }

func (me *Compte) debiter(m int) error {
  if me.solde < m { return ErrSolde }
  me.solde -= m
  return nil
}
```

## 2. Values

Why. A single number, the machine-word integer. A document loaded by a program counts the same way. `string` is bytes, not Unicode text, so that a slot name and a buffer are the same thing. The header of a slice or a map carries its arena, so that the life of the bytes has a name. A map does not grow: an absent key is a fault, not a hidden allocation.

| Kind | Note |
|---|---|
| `nil` | Absence. Only inhabitant of `error` without error. |
| `bool` | `true`, `false`. |
| `int` | Signed machine-word integer. Only number. |
| `u8` | Byte. For buffers. |
| `string` | Immutable bytes, known length. Not Unicode text. |
| `error` | A value. Compared with `==`. Not an exception. |
| struct | Value, copied on assignment. |
| `*T` | Pointer to a `T` living in a visible arena. |
| `[]T` | Slice: pointer, length, owning arena. |
| `map[K]V` | Map. Same header as the slice. |
| `chan[T]` | Bounded queue. Guard. A name. |
| `entree[T]` | Write end. Copied. Born empty. |
| `sortie[T]` | Read end. Copied. Born empty. |
| interface | Pointer to the value, pointer to the vtable. |
| `Id` | Index in a document table. Not a pointer. |

A struct has at least one field. A struct does not contain itself. A `*T` field does not. `struct Noeud { suite *Noeud }` is allowed.

`/` and `%` truncate toward zero. `-n` is the unary. `0 - n` is allowed.
Operands and arguments evaluate left to right. A call finishes before the next operand or argument.
`==` requires two values of the same kind. `!=`, `<`, `>`, `<=`, `>=` are the signs of C.
`<`, `>`, `<=`, `>=` compare two integers.
A comparison returns a `bool`. `!`, `&&` and `||` take booleans.
`&&` and `||` short-circuit: the right operand does not run when the left has already decided.
`if` takes a boolean. The block runs when it is true. `else` is the other block, on the same line as `}`. `else if` chains.
`for` repeats the block while the boolean is true. The step is a statement of the body. No `break`.
`for x in xs` copies the slice before the first turn. `x` is the element, a name of the body. `for i, x in xs` also binds the index before the element. `i` is an `int` of the body. Assigning it does not change the step.
`for v in c` on a channel is in §8. It borrows the channel, it does not copy it.
The literal `[]T{...}` lives in the `arena name` block and dies with it. Without that block, including in `arena thread`, it is the call stack. A slice born there does not leave the call. Each literal has a storage for the call. A loop reuses it. `thread.make` is the allocation that is born in the thread's arena.
`nom := []T` is the empty slice.
`x[i]` reads. `i` is an `int`. The element of a slice has the type `T`. The element of a string is a `u8`.
`len(x)` returns an `int`, for a slice, a string or a map. Not for a channel.
An index outside `0 .. len-1`, including negative, is the fault `indice hors table`. A table is that indexed storage: the elements of a slice, the bytes of a string, and the table of the document.
`xs[i] = v` writes into the slice. `s[i] = v` is refused.
Copying a slice copies the header. The two names see the same storage.
`x[lo:hi]` is a window on a slice or a string. `lo` and `hi` are `int`. The absent bound before `:` is `0`. The one after is `len(x)`. It must be `0 <= lo <= hi <= len(x)`. Otherwise, it is a host fault. The window shares the storage. Its length is `hi - lo`. A window on a string is a string. A window on a slice born in the call does not leave the call.
`map[K]V` is a map. `K` is an `int` or a `string`. `V` follows the rule of a slice element.
The map has the same header as a slice. Copying it shares the storage. `==` on a `string`, a slice or a map compares this header: the pointer and the length. Two equal texts that do not share the storage are not equal. A copy of the same header is. `error` compares the bytes. A field read from a file is compared byte by byte, walking the buffer. No equality function in the language.
The literal `map[K]V{k: v}` lives in the `arena name` block and dies with it. Without that block, including in `arena thread`, it is the call stack. A map born there does not leave the call. Each literal has a storage for the call. A loop reuses it.
`nom := map[K]V` is the empty map.
`m[k]` reads. `m[k] = v` writes a key already present. An absent key is a host fault. The map does not grow.
A repeated key keeps the last value. The order of the keys is that of first appearance. `len(m)` is the number of keys.
An `int` key is the number. A `string` key is the bytes.
`for v in m` copies the map before the first turn. `v` is the value, a name of the body. `for k, v in m` binds the key before the value. Assigning `k` or `v` does not change the map.
A string literal is the bytes between the quotes. `\` is refused.
`or return` propagates an error. `or` is not a boolean operator.
No float. A drawing at fixed scale counts in `int`.
A foreign float enters by `extern` and does not stay in the language.

`string` is not a mutable slice. `[]u8(s)` copies its bytes into the arena of the current block. Outside a block, the copy lives in the call stack and does not leave the call.
`*T` points to an `int`, a `bool`, a `u8` or a struct. `p := *T` is the null pointer.
`*p` reads. `*p = v` writes. Reading or writing the null pointer is the fault `pointeur nul`.
`p = x`, an argument or a `return` takes the address of `x` when the expected type is `*T`, `x` has the type `T`, and `x` is a variable, a field or an element. There is no `&` operator.
`**T`, or a pointer to a slice, a map, a string, an error or an interface, stays `pointeur : not in this version`.

## 3. Memory

Why. The `arena` block is the added idea. The author names the brace that is the death; he does not write `free`. The stack, the block and `arena thread` are the three deaths one can point to.

Every Why value lives in an arena. There are three kinds.

- The call stack. A local struct, an integer, a pointer.
- The `arena` block. Everything the block allocates dies at the closing brace.
  The compiler inserts a single release.
- `arena thread`, for what must survive the function and that the author did not name.
  It dies with the thread.

```
func main() {
  arena doc {
    buf := read("a.txt") or return
    ls := parse(buf)
    afficher(ls)
  } // one release, for the whole document
}
```

Rules.

1. A reference does not leave its arena. Returning a slice born in the block is a compile error.
2. In a block, a datum has a mutable pointer, or several read pointers. Not both.
   Two addresses of the same variable, taken in the block, do not coexist when one writes. The message is `pointeur mutable`. Several reads coexist. Copying a pointer does not take a second address.
   The copy of a struct that contains a pointer, a slice or a map shares this storage. The copy of a struct that has only `int`, `bool` and `u8` is not an alias.
3. No pointer arithmetic. No conversion of an integer to a pointer.
4. `defer` runs a function at the exit of the block. It serves foreign resources, not Why memory.
   `defer call` records the call. The arguments are evaluated at this point. The result of the deferred call is ignored. Without a call, the message is `defer attend un appel`.
   A `return` evaluates its result, then leaves each open block, from the inside out. The exit of a block closes the channels whose name dies here, waits for the threads launched here, then runs the `defer` from the last to the first. The guards that remain die, and the arena of the block is freed. `arena thread` is not freed at this brace. The body of a `for` closes its channels and runs its `defer` each turn. It does not wait for its threads: they are waited at the block that contains the `for`. A thread launched in a deferred call is waited before the return of that call.

The author does not write `free`. He names the block whose end is the death.
An arena can be passed. The parameter is written `arena`.
`a.make([]T, n)` allocates a slice of length `n` in `a`, initialized to zero. A negative `n` is the fault `taille négative`. If the number of bytes does not fit, or if the host cannot allocate, the fault is `arène épuisée`.
`a.append(xs, v)` returns a new slice in `a`, of length `len(xs) + 1`, that ends with `v`. The append may extend the bytes of `xs`. `xs` keeps its length, and writing in this length writes in the prefix of the returned slice. Otherwise the returned slice is a copy. The storage of the result dies with the arena of `a`. The original bytes die with `a` only if they were already there. If `len(xs)` is already the largest `int`, or if the number of bytes of the new slice does not fit, the fault is `arène épuisée`.
`new` does not exist.
`arena name { }` opens a block. What it allocates dies at the brace. The compiler inserts a single release.
`arena thread { }` opens the thread's arena under the name `thread`. It is not freed at the brace. It dies with the thread. Each thread has its own, including the one that runs `main`. A slice born inside can leave the function. It does not pass to another thread. The message is `le pointeur ne sort pas`.

`struct Nom garde` is a guard. `t := Nom` owns nothing. `t.make([]T, n)` and `t.append(xs, v)` allocate in `t`, with the same faults as on an arena. `t.append` extends like `a.append`. A struct that contains a guard is a guard, with or without the word.
`return` and `=` move. The source becomes empty. The compiler frees the guard at the end of the name that still holds it. The author does not write this release: it is not a destructor. A receiver `*T` borrows. A receiver `T`, a parameter `T` and the argument that fills it move. `*p` moves the targeted guard, and a receiver `T` called on a `*T` too. A `return` still moves when the result is `(T, error)`.
Reading an already-moved guard, or one of its fields, is `garde déplacée`. A slice, a map or a pointer drawn from the guard does not leave alone. Passing it to a call that does not keep it is allowed. Keeping it where it survives is `la tranche ne sort pas`, `la map ne sort pas` or `le pointeur ne sort pas`. Keeping it in another guard, or in a field reached by crossing a nested guard, is the same error: the slice does not live in the arena that leaves. Copying the guard into an interface, a slice or a map is `la garde ne se copie pas`. Moving a field keeps the fate of the container: the container no longer frees it.

A call that returns a guard is its owner until the end of the block, then the compiler frees it. Keeping a slice, a map or a pointer drawn from this result is `la tranche ne sort pas`, `la map ne sort pas` or `le pointeur ne sort pas`. Reading it for an integer, or passing it to a call that does not keep it, is allowed.

Assigning a block arena to a name that survives it is an error. The message is `l'arène ne sort pas`.
Returning a slice born in the block, or keeping it in a name that survives it, is an error. The message is `la tranche ne sort pas`.
Returning a map born in the block, or keeping it in a name that survives it, is an error. The message is `la map ne sort pas`.
Returning an interface born in the block, or keeping it in a name that survives it, is an error. The message is `l'interface ne sort pas`.
Returning a pointer to the stack, or keeping it where it survives, is an error. The message is `le pointeur ne sort pas de l'appel`.
Returning a pointer to block data, or keeping it in a name that survives it, is an error. The message is `le pointeur ne sort pas`.
The address of a field follows the struct that contains it. It does not follow the arena of another field. A pointer kept in a field follows the storage it targets, not the arena of another field. Two fields are two addresses. A stack struct that contains a pointer to the stack does not leave this call, even if another field lives in an arena. Copying it into a variable, a field, an element, an `append` or an interface follows the same rule. A field or an element that dies with this pointer can receive it. A parameter that carries this pointer follows the same rule when the call keeps it in a `*T`, an element, an `append` or a map. A `*T` parameter too. An `interface` parameter too: the copy lives in the caller, and this arrangement gives `l'interface ne sort pas de l'appel`. This copy lives for the duration of the call, a shorter block does not kill it. An interface field of this struct follows the stack box, not the arena of another field. A nested struct that contains this interface follows the same box. Returning the struct, the field or the nested struct gives `l'interface ne sort pas de l'appel`.
The last living `return` decides the life of the result. It replaces the one before it.

```
func parse(a arena, buf []u8) ([]Ligne, error) {
  return a.make([]Ligne, n)
}
```

Two arenas are agreed for the SemCards prototype. They are not words of the language.
They are blocks a program may open.

- `image` contains the cards, the slots, the methods, the file tree and the texts.
  It dies at the reload. A release for the whole document.
- `frame` contains the canvas, the interpreter's locals and the copy of a `for`.
  It englobs the tick and the drawing, and dies at the next tick.

## 4. Functions and methods

Why. A single form, `func`. The method is that form with a receiver `me`. A `.oo` document may reuse this word. `or return` propagates the error, instead of a comparison after each call.

A function is `func name(params) T`.
Several results are written `(T, error)`. `or return` propagates the error.

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

The slice is born in `a`, the caller's arena. Without this parameter, it does not leave the call. `Ecrire` replaces the file and does not take an arena. A function and a method do not share a name: the proof, a single package, calls the functions `Lire` and `Ecrire`, and the methods `(Fd) Read` and `(Fd) Write`.

A `return` always reached ends the function. The statement that follows, in the same block, is not executed. The compiler signals it and compiles the rest. The message is `code non exécuté`.
`if true` keeps only its first branch. `if false` does not keep it. An `if` whose each branch ends, and a `for true` whose body ends, make the statement that follows not executed. Another `for`, a `for x in`, and `or return` leave this statement executed: the loop may not turn, and `nil` lets it continue.
A `select` whose arm does not end leaves the statement that follows executed. If each arm ends, the path where all channels are closed stays open. `or return` after the `select` closes it, and the statement that follows is `code non exécuté`. Without `or return`, the unread error is `erreur ignorée`. If the function returns a value and this path does not, the message is `il manque return`.

A method is written `func (me T) name(params)`.
The receiver is named `me`. It has the type `T` or `*T`, and `T` is a struct.
The name `me` is not that of a function, a struct or a method.
No class, no `this`, no overloading.
Two structs may carry the same method name. A function and a method do not share a name.
The call is written `b.c.debiter(1)`.

```
func (me *Compte) debiter(m int) error {
  if me.solde < m { return ErrSolde }
  me.solde -= m
  return nil
}
```

`nom := Type` declares the zero value of `Type`. A zero `int` is 0. A zero `bool` is `false`. A zero struct has its fields to zero.

`x = y` copies the value. `x` is a variable or a field.
`x += y` is `x = x + y`. The same family: `-=`, `*=`, `/=`, `%=`.
`x.m(...)` calls the method `m` of the type of `x`.
`me` has the type `T` or `*T`, where `T` is the type of `x`.
If `me` is a `*T` and `x` is a value `T`, the call passes the address of `x`.
`x` is then a variable or a field of a variable. There is no `&` operator.
The direct call `m(...)` does not take this address.
Keeping a slice, a map, an interface or a pointer by a method follows the same rules as the assignment of the field.

## 5. Interfaces and composition

Why. The interface is the list of methods. The struct stays in its package, the caller sees only the methods. Composition names the field: `Boite` is not a `Compte`. No inheritance. A card prototype does not have, in the host, the model of a class.

An interface is a list of methods. It does not repeat the receiver.
It is satisfied if the concrete type has these methods, with the same parameters and the same results. No `implements`.
The receiver stays on the method: `func (me *Compte) lire(k string) ([]u8, error)`.

```
interface Stockeur {
  lire(k string) ([]u8, error)
  ecrire(k string, v []u8) error
}
```

If the concrete type is known at the call, the call is direct.
If it is not, the call goes through the vtable.
This call follows the concrete methods when they agree. If it returns a value of the receiver, the result has the life of the interface value. If it keeps a value in the receiver, it follows the same rules as the assignment of the field. If the methods do not agree on this arrangement, the message is `les méthodes ne s'accordent pas`.
A concrete value is passed where an interface is expected when the methods match, parameters and result. The concrete receiver is `T` or `*T`. A variable satisfies a `*T` method: there is no `&` operator. The value passed is a copy. The interface points to this copy and to the vtable. The copy lives for the duration of the call. An interface born there does not leave the call. An interface parameter can. The empty interface is refused. No type assertion. An interface without a value is a host fault.

No inheritance. Composition is a field.

```
struct Boite { c Compte, etiquette string }
```

`Boite` does not have the methods of `Compte`. One writes `b.c.debiter(1)`.
Promoting the field's methods is refused. The author names the field.

## 6. Generics

Why. `Pile[T]` is a text and several concrete functions. C sees only these functions. The constraint is an interface, so that there is no second constraint language.

A struct or a function may take types. They are instantiated at compile time.
The only constraint is an interface. No specialization, no variadic of types, no code at compile time. `comptime` does not exist.

The parameter is written `T`, or `T Interface`. Several parameters are separated by a comma.
The instantiation is written at the site: `Pile[int]`, `identique[int](v)`. It is not guessed.
A method reuses the parameters of the struct, in order: `func (me *Pile[T]) pousser`. It does not add any.
A parameter does not carry the name of a type. The message is `int est un type`.
The constraint names an interface. Otherwise the message is `int n'est pas une interface`.
A method that fixes the parameter, `func (me *Pile[int]) pousser`, is `pas de spécialisation`.
Forgetting the argument is `Pile attend 1 type`. The number is that of the parameters.
A function without a type parameter, written `f[int]`, is `f attend 0 type`.
A struct without a parameter, written `Compte[int]`, is `Compte attend 0 type`.
A concrete name already taken is `déjà déclaré`.
A pointer to the parameter, `*T`, is `pointeur : not in this version`. `*Pile[T]` stays a pointer to the struct.

In the body, a parameter without a constraint is copied, passed, kept and returned.
An operation, a comparison or a field on it is `pas une méthode`.
With a constraint, the methods of the interface are called on the value. An absent method is `dire n'est pas une méthode de Parleur`.
The concrete type must have these methods. Otherwise the message is `Bonjour n'a pas dire`.
An argument that is still a parameter carries this constraint, or an interface that has its methods. Otherwise the message is `U n'a pas dire`.

```
struct Pile[T] { data []T, n int }

func (me *Pile[T]) pousser(a arena, v T) {
  me.data = a.append(me.data, v)
  me.n = len(me.data)
}
```

## 7. Errors

Why. `error` is a value, it comes back with the result. A host fault stops the process: an index out of bounds is not an error the document catches.

`error` is a type. `nil` means no error. `nil` is its zero value. `e := error` is `nil`.
An error is created with `error("solde")`. The text is `solde`. `error("")` is `nil`.
Every zero-length error is `nil`. `== nil` is true. `or return` continues.
It is compared with `==`. `error("solde") == error("solde")` is true. `error("solde") == nil` is false. `!=` is the negation.
An `error` field is compared like an `error`.
`(T, error)` is the only multi-result form. The second type is `error`. Another form stays `plusieurs résultats : not in this version`.
`appel() or return` follows a call. If the call returns `(T, error)`, the expression is `T`. If the call returns `error`, it is nothing. `nil` lets it continue. Otherwise the current function returns this error. A `(T, error)` function then returns the zero value of `T` and the error. An `error` function returns the error. A function that does not return `error` is refused. The message is `or return : la fonction ne rend pas error`.
In a `(T, error)` function, `return v` returns `v` and `nil`. `return nil` and `return error("solde")` return the zero value of `T` and this error. `return appel()` reuses the pair when the call returns `(T, error)`.
A `(T, error)` call used as `T` is refused. The message is `or return attendu`. An ignored `error`, outside `defer` and outside `thread`, is `erreur ignorée`.
`or return` returns the error of the current function.
No `try`, no `catch`, no catchable panic.

A host fault stops the process. Index out of bounds, division by zero, arena exhausted. A half-dead thread would leave an arena.
It names the file, the line and the column: `why: file:line:column: message`.
It is not caught. It is not an error of the document: the document has its own faults, defined by the interpreter.

## 8. Concurrency

Why. The thread is that of the system. Why has no scheduler: the ceiling stays that of C. The brace that launches waits: the author writes no handle. The channel copies or moves, so that a pointer does not enter another thread's arena. The order of the `select` is the priority, the first ready arm. `image` is not shared: a single thread interprets the world.

A thread is launched with `thread call`. The arguments are evaluated at this point, left to right. The result is ignored, including an error. It is not `erreur ignorée`. Without a call, the message is `thread attend un appel`.
The thread has its stack and its `arena thread`, which dies when its call returns. No goroutine. No growable stack. No scheduling runtime.
The brace that contains the `thread` waits for it. An `if`, an `else`, an `arena`, a `select` arm and the body of a function are such braces. The body of a `for` is not. `return` and `or return` take the exit of §3. There is no handle.

The close is that of §3. It precedes the wait. The send that has not yet entered returns `error("fermé")` and the value does not enter. A receive takes a slot still full. When none remain, it returns the zero value of `T` and `error("fermé")`. The storage of the channel lives until the death of the guard, after the wait. A thread of the same block that still sends therefore sees `error("fermé")`. For its sends to enter first, it is launched in an inner block, waited before the name of the channel dies.
A name declared in the body of a `for` dies at the end of the turn. A thread launched in this body and that borrows this name is `le pointeur ne sort pas`: the wait is outside.

A `*T` argument of `thread` is `le pointeur ne sort pas`, except `*chan[T]`, and except a `freeze` that lives in an `arena shared` still open during the call. Passing a block arena, or `thread`, is `l'arène ne sort pas`. Passing an `arena shared` is `arène partagée`. `int`, `bool` and `u8` are copied. The bytes of a `string` or an `error` are copied for the call. A guard is moved.

`chan[T]` takes a type. Otherwise the message is `chan attend 1 type`. `c := chan[T]` owns nothing. There is no null channel. The send or the receive on this name is `garde déplacée`. `c := chan[T](n)` opens `n` slots. The queue does not grow. `n` zero is a rendezvous: the value is copied, then both continue. `n` negative is the fault `taille négative`. If the host cannot allocate, the fault is `arène épuisée`. At instantiation, the value follows the rule of its concrete type.

The channel is a guard, and it stays a name: a variable, a parameter or a result. A field, the element of a slice, the key of a map and the value of a map are not a `chan[T]`. The message is `le canal reste un nom`. `*chan[T]` may be a field: it is the address of the name, not the channel. `chan[chan[T]]` stays a name whose element is a channel.

Copying is `la garde ne se copie pas`. `=` and `return` move it. The source becomes empty. The compiler closes it at the end of the name that holds it. The author does not write `close`. A `chan[T]` parameter moves. A `*chan[T]` parameter borrows and does not close. Several threads may borrow the same channel. It is not `pointeur mutable`. The borrow lasts until the wait of the `thread` that received it. Moving the channel before, or letting it die before, is `le pointeur ne sort pas`.
`send` and `receive` have the receiver `*chan[T]`. There is no other method on the channel.

`entree[T]` is a write end. `sortie[T]` is a read end. Each takes a type, the same element as the channel. Otherwise the message is `entree attend 1 type` or `sortie attend 1 type`. `entree[T](n)` and `sortie[T](n)` are `not in this version`. There is no `*entree[T]` nor `*sortie[T]`. The message is `pointeur : not in this version`. `nom := entree[T]` and `nom := sortie[T]` are the empty end. The word `sortie` of §3 stays the end of a block. The type is written `sortie[T]`.

The empty end is copied, passed and returned. It does not own the queue. It is not a null channel, and it is not `garde déplacée`. `n.c = src` links the end when `n.c` is an `entree[T]` or a `sortie[T]` and `src` is a `chan[T]` of the same element. The link copies the pointer of the channel. It does not move `src`. `src` keeps the send and the receive, and it still closes the channel at its death. A `chan[T](n)` without a name does not hold this link. The owner is a name. The message is `le pointeur ne sort pas`.

Before the link, `send` and `receive` return `error("pas relié")` and the value does not enter. After the link, the operation goes into the queue of this channel. `entree[T]` has only `send`. `sortie[T]` has only `receive`. The other name is not a method. When the name that holds the channel dies, a thread launched in the block of this name sees `error("fermé")`: the close precedes the wait. An end whose storage survives this name is `le pointeur ne sort pas`. The compiler also refuses when it does not know if the end is still empty.

A named slice or map holds its ends as long as this name. `xs[i].c = src` and `m[k] = src` link like `n.c = src`. Several elements may name the same channel. Copying the header to a longer life, returning it, or passing it to a function that keeps it, is `le pointeur ne sort pas`. An index whose base is not a followed name stays refused.

An empty end may leave. Returning a received end as a parameter is allowed: the caller holds the name. Linking an end to a borrowed `*chan[T]`, then returning it to the caller, is allowed. A method that opens a channel and keeps it in a field of the receiver is `le pointeur ne sort pas`, because the name dies at the end of the method. Passing a linked end to a `thread` launched in the block of the name follows the rule of `*chan[T]`. Moving the name to a shorter life than the end is `le pointeur ne sort pas`.

In a sent struct, an `entree[T]` or a `sortie[T]` is copied. It does not close the channel. The struct is not a guard for this end.

`c.send(v)` returns `error`. A full queue blocks. It is not an error. `nil` means `v` entered. `c.receive()` returns `(T, error)`. An empty queue blocks. `nil` means the value was received. After the close, the send returns `error("fermé")`. Each receive returns a slot still full, then, when none remain, the zero value of `T` and `error("fermé")`.
The send copies an `int`, a `bool`, a `u8`. It copies the bytes of a `string` or an `error`. It moves a guard. A slice, a map, a pointer or an interface passes if it is `freeze` and it lives in an `arena shared` still open at the receive. Otherwise it is `le pointeur ne sort pas`. A struct is handled field by field. A value that still has a mutable alias is `alias`.
The receive of a `string` or an `error` copies like `[]u8`: into the arena of the current block, or on the call stack if there is no block. The stack copy does not leave the call.
Several threads blocked on the same channel are served in order of arrival.

`p := freeze(x)` moves `x`. Without a value, the message is `freeze attend une valeur`. At the head of a statement, outside the `:=` that defines it, it is `freeze attend un :=`. `freeze` marks the storage. It does not change the arena and does not return a private arena shareable. A write that reaches this storage is `freeze`, including in the thread that opened it. The send and the receive write the channel: a `freeze` channel refuses them. If a mutable alias remains, the message is `alias`.

`arena shared name { }` dies at the brace, after the wait of the threads launched inside. `name.make` and `name.append` stay on the thread that opened the block. Another thread receives a copy, or reads a `freeze`.

The only thread that calls `name.make` or `name.append` is the one that opened the block. A thread launched in the block cannot call `make` nor `append` in it: passing it `name` is `arène partagée`, as `thread f(s)` refuses. A call of the same thread passes `name` as an ordinary arena, and `a.make` is legal there.

"Still open during the call" and "still open at the receive" mean for the verifier that the arena is on the stack of the block when the thread is launched: the brace waits for the thread before `why_arena_free`, so the storage is alive during the thread. A `freeze` born in the block and read by a thread of this block passes. A value that leaves the block to be read outside follows the rule of §3: `la tranche ne sort pas` for a slice, `le pointeur ne sort pas` for a pointer.

The name `name` is not visible by a thread launched in the block: it is local to the brace and dies with it. The thread sees only the `freeze` value that was passed to it, which names the same storage. Passing the name `name` itself, instead of a `freeze`, is `arène partagée`.

`for v in c` receives until the close. `v` has the type `T`. The slots still full come out, then the loop stops. `error("fermé")` is not a value of the body. Assigning `v` sends nothing. `for i, v in c` is `le canal n'a pas d'indice`.

`select` returns an `error`. Each arm has a block. An arm is `case v := c.receive()` or `case c.send(v)`. Otherwise the message is `le bras attend un canal`. The channels of the arms are evaluated left to right before the wait. The value sent is evaluated only if this arm runs. The first ready arm, in text order, runs. An arm does not satisfy another arm of the same `select`. `v` is a `T`: the arm runs only for a received value. A closed and empty channel does not make the arm ready. A closed channel that still has a slot makes the receive arm ready. A channel written first that stays ready keeps the following in wait. If no arm can advance anymore, `select` returns `error("fermé")`. If a send may still arrive, it blocks. `or return` may follow the `select`, as it follows a call. The arm that ran has consumed the error of the send or the receive. No `default`. Without an arm, the message is `select attend un bras`. A `case` outside a `select` is `case hors select`.
The choice of the `select` is the order of the text. The order between two threads is that of the system.

A send that no one receives, or a receive that no one feeds, blocks the process at the wait of the block. No detector.

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

`n := Nod` leaves `c` empty. `n.c.send(1)` is `error("pas relié")`. `n.c = src` links, and `src` stays the name that closes. A read end is written `sortie[int]`. `s = src` links it the same way.

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

A program may keep an arena and a single thread. The language does not require it. The `.oo` document refuses concurrency. A fault in a thread stops the process.

The `serveur` package accepts and starts a thread per connection. `ServeConn(ecoute, app, n)` serves exactly n connections and returns when the n threads are done. The `client` package sends bytes and reads the answer in a buffer. The proof launches two clients toward a server on `127.0.0.1`; the sum of the two states is 42.

`Open(chemin)` opens a file from the disk. `(Fd) Read` writes into the caller's buffer and returns the number of bytes. Zero is the end, not an error. A count shorter than the buffer is normal: the proof relaunches `Read`. `Close` closes the descriptor and returns an `error`. The proof opens the `data` file of its directory, reads to the end, and the exit code is the sum of the bytes.

`Lire(a, chemin)` returns the whole file into the caller's arena. `Ecrire(chemin, buf)` replaces the file. The proof writes the byte 42, reads it back, and the exit code is this sum.

`Seek(n)` places the next read at `n` bytes from the start and returns the position reached. `Tell` returns the current position and does not move it. A negative `n` is `error("refuse")`. The façade has no hidden buffer. The proof opens a fixed file, seeks to the middle, reads the end; the sum of the bytes read is the exit code.

The sum in N threads: the parent computes bounds that share the file, closes its descriptor, and launches a thread per interval. Each thread opens, seeks, reads its piece and sends the sum of the digits. The parent receives N times and adds. The channel is a queue of N slots. No lock. The exit code is the sum of the sums.

TLS: `DialTls(hote, port)` and `AcceptTls(ecoute)` do the handshake and return an encrypted `Fd`. The read and the write go through the same `Fd`, without changing the call. The self-signed certificate is embedded in the binary; the client does not verify the name. The proof is the same as Serve: two clients, the sum of the two states is 42.

## 9. Foreign

Why. `extern` is a hand-written signature. Why does not parse C headers. `defer` frees what C allocated, because the arena only frees what it created.

`extern func` declares a C function, hand-written signature.
Why does not free memory allocated by C. `defer` does.
No parsed header.
An `extern` takes and returns `int`, `string` and `[]u8`. Any other type is refused. The message is `extern attend int, string ou []u8`. On a pair, it points to the `(`.
A `string` passed to C is the pointer to the bytes, then their count. Why does not add the null byte. The C function copies and adds the null if the system requires it.
A `[]u8` passed to C is the pointer to the bytes, then their count. These bytes survive the call, on the stack or in an arena. C writes into them. It does not allocate them.
A `string` or a `[]u8` returned by C is the pointer to the bytes, then their count. Why makes a value of it. It does not add the null byte and does not attach these bytes to an arena. The C function does not return a pointer taken on an argument.

## 10. Product

Why. The `.wo` is a native binary, without a Why runtime. `why run` on a directory compiles and runs. `why run monde.oo` may pass a document to the `.wo` already there. Editing that file does not recompile the program.

`why build [directory]` reads the `.wc` of a directory and writes a `.wo`.
`why check [directory]` checks these `.wc`. It does not write a `.wo`.
The absent directory is the current directory.
The diagnostics go to the error output. `code non exécuté` does not refuse the package.
Without `main`, the `.wo` is a lib. With `main`, it is a binary.
A binary can link `.wo` libs. The format is a single file, without a Why runtime.
The arenas are calls inserted by the compiler, not a dynamic library.

`why run [directory]` writes the same `.wo` as `why build`, then runs it.
The absent directory is the current directory. The arguments that follow are those of the process.
The process starts from the directory of the package.
The exit code is its own. Without `main`, the command refuses.
`why run monde.oo` loads the current `.wo` and passes it the document.
It does not compile. It runs the `.wo` already written in the current directory, under the name of this directory. The path of the document is the argument of the process. The process starts from this directory. The exit code is its own.
Without this `.wo`, the message is `il manque le .wo`. Without the file, the message is `document absent`.
The interpreter opens this path. Without an argument, it opens the file `data`.
The `.oo` is not linked in the `.wo`. Replacing it does not recompile the program. This command is a possibility. The language does not make it mandatory.

`why play` serves a local page. Each page is a fragment with a `main`; the result is the exit code, or the diagnostic.
The fragment is alone: there is no directory to import. The only visible package is the fixed package `lib`, without `main`, imported by the path `lib`. `lib.Reponse()` calls the function exported by its qualifier, and exits 42. `lib.Lire(doc)` loads a fixed file into a slice born in the arena `doc`, and `lib.Octets(buf)` sums the bytes. Exit code 42. The path is not a parameter: the package reads the `data` file of the proof's folder, and nothing else. It is not the `fichier` package of `lib-spec.md`.
What stays refused: a lowercase name of the other package, `basse : lowercase, not visible outside the package`; a field, a method, a struct name from the other package. Only the first-level exported function crosses the boundary.

## 11. The `.oo` document

Why. A `.oo` document is a possibility. SemCards, the prototype, may use it. The card has a name, a prototype, slots, methods. It is not Why: the author of a card does not choose an arena. `arena` is not a word of `.oo`.

A `.oo` file is a sequence of objects. The indentation is the block.
`//` comments to the end of the line. Tabs are refused.
The image loaded at boot is the copy. The file remains the truth.
The program does not create an object, does not free one, and does not inspect itself.

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

An object has a name, an optional prototype, slots and methods.
`object MillIn : Stack` reads `qty` on `Stack` until `MillIn` writes it.
The write always falls on the receiver. `me.qty = 0` in a method of `MillIn` creates the slot there. The parent does not change.

A nested slot is a child object, born at the load, absent from the head table.
Its kind is the name of the prototype. The slot `home` points to the parent.

```
object Bake
  stock: Stack
    qty: 1600000
    value: 141888
```

A method is `on name (params):`. There is no function, no `return`.
The value of the method is the last value computed.
An assignment is the value assigned.
An `if` without `else` whose condition is false is `nothing`.

The names resolve in this order: the local, the slot of `me` going up the parents, the head object.
`qty := 1` writes a local and shadows the slot. To write the slot, one writes `me.qty = 1`.

The values are `nothing`, `true`, `false`, the integer, the text, the list, the object, the canvas.
The integer is the only number. `/` and `%` truncate. A negative is written `0 - n`.
`if` accepts only a boolean. `==` compares two values of the same kind.
`!=`, `<`, `>`, `<=`, `>=`, `&&`, `||`, `!` are the same signs as in the host.

The list is the only aggregate. `[a, b]`. `add` moves the already-present element to the end.
`remove`, `length`, `at`. `for x in liste:` copies the list before walking.
`length` returns the number of elements. `at(n)` returns the element at `n`, zero is the first. Out of list is a host fault.
`add(x)` and `remove(x)` return nothing. `remove` removes the first occurrence; the absent element is a host fault.
`for x in liste:` is the last value of the body, or nothing if the list is empty.
A list is equal only to itself. Two texts are equal if they are the same bytes.
An integer has `asText`.

The canvas is not built by the program. The host passes it to `draw`.
The methods (`rect`, `text`, `frame`, `hit`, `chrome`, `card`) record orders the host replays. They return `nothing`.
`rect(x, y, w, h)`, `text(x, y, texte)`, `frame(x, y, w, h)`, `hit(x, y, w, h)`, `chrome(n)`, `card(x, y)`.
The orders are replayed in the order of the call.

An error is a host fault: absent slot, wrong number of arguments, division by zero, call deeper than 48. The program does not catch it.

`image.oo` reuses the grammar of the statements, one line per living slot.
It is not a second language. It is the written copy, if the host saves.

What the document refuses, it refuses to remain the document: no pointer, no allocation, no concurrency, no class, no generic.
The standard library is the machine: `Part`, `Window`, `Desk`, the stacks of the month of bread.

## 12. SemCards

Why. SemCards is a prototype. It can show a document. Why is not defined by it. The graph, if it is loaded, is a table of `Id` in an arena, so that several names target the same card. The possible release is the reload, once for the whole table.

SemCards is a possible environment. Why is the language. A Why program may serve it as a host.
A card is an object of the document: a name, a prototype, slots, methods.
The instance is the loaded card. The prototype is the object from which it inherits the unwritten slots.
It is not a class. Writing a slot does not modify the prototype.

The graph is not made of Why pointers. It is a table in `image`.
A `.oo` reference is an `Id`. `Desk.windows`, `home`, a list of `Shelf` and a `Hit` may target the same card. Two methods may mutate `MillIn` in the same frame.
It is the program. The rule "a single mutable pointer" stops at the table.
Inside, the alias is the semantics: the read goes up, the write falls on the receiver.
The `Id` is not freed. It dies with `image`, and the host drops the whole table at once.

A list born in a method and kept in a slot is born in `image`.
The `.oo` author does not choose the arena. The primitive that stores copies into `image`.
The local dies with the call. The Why compiler continues to refuse that a slice of `frame` leaves its block. It does not see the `.oo` program.

The boot:

1. Open the arena `image`.
2. Read the `.oo`. Build the table, the threads, the `home`, the methods.
3. Open the arena `frame`.
4. Call the tick, then the drawing. Empty `frame` at the next tick.
5. At the reload, free `image` and resume at 1. The file has not changed, unless it was saved.

The visual editing, the single message and the text field are cards and canvas orders.
They are not constructions of Why. Modifying them is modifying the `.oo` or the host's primitives (`hit`, `chrome`, `card`), not the language.

## 13. What Why refuses

Why. These refusals keep the single idea. A garbage collector, a borrow checker, an inheritance or a destructor written by the author would hide the death that the block names.

- The garbage collector, including on a region of the program.
- The borrow checker and the named lifetimes on the pointers.
- The inheritance, the overloading, the abstract classes.
- The pointer arithmetic, the hidden allocation, the destructor written by the author. The release of a guard is inserted by the compiler, as that of a block.
- The lock, in the language or in a Why library. Two threads do not share a mutable datum. An `extern` that hides a lock leaves an alias the verifier does not see.
- The macros, the annotations, the code at compile time.
- The exceptions.
- A second grammar for the document. `arena` is not a word of `.oo`.

## 14. What this spec does not buy

Why. The interpreter written in Why is the same program, more concise. The C ceiling on a few-line method is not the goal.

An interpreter in Why is a more concise interpreter. `me.qty + q` stays a lookup, a climb of the parents, a node.
The C ceiling on this code arrives when a `.oo` method is compiled.
The methods are a few lines. That signal is not there.
One does not rewrite the language to speed up a prototype whose subject is a document.
