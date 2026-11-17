---
title: "Libraries"
weight: 30
---

# Libraries — spec 0

This file proposes the libraries. It does not change the language.
Each package states its why. The rule of the language stays in `why.md`.
`why.md` wins in case of conflict. Nothing here is compiled until the corresponding sentence is in `why.md` and the code goes with it.

These packages speak to the system. They add values made of the types of the language. They do not add a kind.
They are not the machine of the `.oo` document. `Part`, `Window` and `Desk` stay in the SemCards prototype, if it loads a `.oo`.

The proofs that compile today are in `why-libs`, next to this repository.
`extern` takes and returns `string` and `[]u8`, in addition to `int`. The proofs of `why-libs` still only see handles.
These proofs are not named `Read`. The packages of this file wait for their functions.

The tour of `why play` has this page: `lib.Lire(doc)` loads the fixed file into a slice born in the arena `doc`, and `lib.Octets(buf)` sums the bytes. Exit code 42. It goes through the fixed embedded package `lib`, not through the `fichier` package of this file, whose `Read` still waits.
The terminal, the client and the server are binaries. They read a pipe, or they speak to `127.0.0.1`. They do not fit in a fragment cut at 2 s.

## 1. Splitting

Why. The system has a single façade, `os`. The four other packages speak to `os`, not to the system: a change of façade does not rewrite `fichier`, `terminal`, `client` nor `serveur`. The handle is an `int`, so that Why does not see the pointer of the C.

A Why library is a directory, hence a package, without `main`. The `.wo` is a lib.
The program that uses it has the `main`. It links these libs. The format stays a single file, without a Why runtime.

Until `import` is compiled, a proof fits in a single directory: the `.wc`, the `.c`, and the `main`. The names do not repeat there.
The splitting into packages dates from the day `import` compiles. That day, `why build` also compiles the `.c` of the imported packages and links them to the binary. A `.wo` lib alone does not contain the façade.

Five packages. A single façade.

| Package | Role |
|---|---|
| `os` | The handle, the calls, the errors. |
| `fichier` | Read and write a whole file. |
| `terminal` | Assemble a line from the input. |
| `client` | Send bytes and read the answer. |
| `serveur` | Accept, and let the application choose the answer. |

`fichier`, `terminal`, `client` and `serveur` do not call the system. They call `os`.

## 2. Façade

The façade is `os/os.c`. It is written by hand. Why does not parse its headers.
The Why handles are `int`. The real pointer, if there is one, stays in a table of the façade. It is the same drawing as the window of `todo`.

```
struct Fd { n int, tls int }
```

`n` is the descriptor, or the index in the TLS table. `tls` is 0 for a raw descriptor.
Why does not see the raw descriptor of a TLS session. The socket stays in the façade.
`Fd` is copied. The copy designates the same handle. `Close` twice is an error `error("ferme")`.

Zero is a valid handle: the standard input. A failure of `Open` is not said with a zero `Fd`. It is said with `error`.

The C functions have a prefixed name. `open` is already the name of the system.

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

A negative return is an error, never a handle.

| Code | Why error |
|---|---|
| `-1` | `error("absent")` |
| `-2` | `error("refuse")` |
| `-3` | `error("coupe")` |
| `-4` | `error("plein")` |
| `-5` | `error("ferme")` |

The code fits in the `int` returned. The façade does not re-publish it by a global variable.
A host fault stays a host fault. An absent file does not stop the process.

`os_read` and `os_write` do a single system call. They return the number of bytes. Zero in read is the end, with a code 0, not an error.
A report smaller than the buffer is normal. The loop that resumes is in Why.
If `os_write` returns 0 while there are still bytes, Why makes it `error("coupe")`.

`os_taille` holds for a regular file. On a pipe or a socket, it returns `-2`.

`os_poser` places the next read at `n` bytes from the start and returns this position. A negative `n` returns `-2`. Beyond the end, the position is set and the return is this position. `os_lieu` returns the current position and does not move it. Zero is the start of the file, not an error. On a pipe or a socket, both return `-2`. If the position does not fit in an `int`, the code is `-4`. A closed descriptor returns `-5`.

A `string` passed to the façade is a pointer and a length. It has no null byte.
The façade copies the path, adds the null, and passes this byte to the system. Beyond 4096 bytes, the path is `error("plein")`. The façade does not allocate this path on the heap.

The buffer `[]u8` comes from an arena that survives the call. The façade writes into it. It does not allocate it, it does not free it.
The memory it allocates for its own account, the TLS session, the `termios`, dies by `defer`, not by the arena.

TLS is linked apart. The `link` file of the package, one line per flag, is passed to the sidecar (`-I`) and to the link edit (`-L`, `-l`). The proof `testdata/tls` names OpenSSL thus. The Why source does not change between the clear and TLS.

`os_brut` sets the descriptor to raw mode and keeps the old state in the table. `os_cuit` returns it. Why does not name `termios`.

## 3. os

`os` wraps the façade. The exported names start with a capital.

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

`Stdin`, `Stdout` and `Stderr` are the descriptors 0, 1 and 2.
`defer f.Close()` launches the call and ignores its `error`. The error that counts is that of `Read` or of `Write`, returned before the exit of the block.
`DialTls` and `AcceptTls` set `tls` to 1. `Read`, `Write` and `Close` read this field and call the clear function or the TLS function.

`WriteAll` resumes `Write` until the end of the buffer.

```
func WriteAll(f Fd, buf []u8) error
```

`defer f.Close()` is the usage. `defer` runs at the exit of the block, before the release of the arena.
`Close` on the standard input is allowed. No function of `terminal` does it.

`Seek` and `Tell` are the position of the descriptor. `Seek` counts from the start and returns the position reached. `Tell` does not move. A negative `n` is `error("refuse")`. Beyond the end, the position is set and the next read returns 0. A pipe or a socket returns `error("refuse")`. A position that does not fit in an `int` is `error("plein")`. An already-closed descriptor returns `error("ferme")`. Zero is the start of the file, not an error.

`Read` and `Write` advance this position by the number of bytes returned. The façade has no hidden buffer. The program that slices adds these numbers, or it calls `Tell`.

A copied `Fd` designates the same descriptor, hence the same position. Two threads do not use it together. Each opens the path. The verifier does not see the descriptor of the system.

The method `(Fd) Read` fills the buffer and advances the position. Loading the whole file is the role of `fichier.Read`, section 4. A file larger than the arena is read with `Seek` and `(Fd) Read`, in pieces, in a buffer of the caller. The movement from the end is not in this cut.

## 4. fichier

`Read` returns the whole file. The arena is that of the caller. The slice returned lives there, and it dies with it.

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

The form without arena written in `why.md` §4 does not compile: a slice does not leave the arena that saw it born.
The day this package compiles, the example of `why.md` takes the parameter `a arena`.

`Write` replaces the file. It does not need an arena: the bytes are those of the caller.

```
func Write(chemin string, buf []u8) error {
  f := Create(chemin) or return
  defer f.Close()
  return WriteAll(f, buf)
}
```

A pipe has no size. It is read with the method `(Fd) Read`, not with the function `fichier.Read`.
Growing a buffer whose length is unknown waits for `append`. These packages do not invent it.

## 5. terminal

`ReadLine` reads the input until the byte `10`, or until filling `buf`.
It returns the window read, without keeping the byte `10`. A buffer too short for the line gives `error("plein")`.
The end of the input in the middle of a line returns what was read, without error. The end at the start returns an empty slice and `nil`.

```
func ReadLine(entree Fd, buf []u8) ([]u8, error)
func WriteLine(sortie Fd, buf []u8) error
```

`WriteLine` pours the bytes, then the byte `10`.
The buffer belongs to the caller. For a line that must survive the buffer, the caller copies into its arena.

`Raw` is there for a key without waiting for the line. The loop that uses it is in the program, not in `why play`.
The raw mode is returned by `defer t.Restore()`.

## 6. client

The client sends a buffer and reads the answer in another. It does not know HTTP.
A request that contains `13` and `10` is a `[]u8`. A Why `string` does not carry these bytes: `\` is refused in a literal.

```
func Exchange(f Fd, req []u8, rep []u8) (int, error) {
  WriteAll(f, req) or return
  return ReadUntil(f, rep)
}
```

`ReadUntil` fills `rep` until the end or until full. It returns the number of bytes.
If the answer exceeds `rep`, the result is `error("plein")`. The caller chooses the capacity.
`append` will shorten this limit later. The package does not wait after it to exist.

`Dial` and `DialTls` return the same `Fd`. `Exchange` does not ask which of the two ran.

`Status` is the only HTTP knowledge of this spec. It reads three digits after the first space. It returns this `int`, or `error("coupe")` if the bytes are not there. No headers, no split body, no text.

## 7. serveur

The program does not provide a callback function. Why does not have one.
It provides a value whose method chooses the answer.

```
interface Responder {
  Respond(a arena, f Fd, req []u8) error
}

func Serve(port int, app Responder) error
func ServeTls(port int, app Responder) error
```

`Serve` listens, accepts, and for each connection opens an `arena` block.
In this block, it fills a buffer of 4096 bytes with `Read`. `error("plein")` if the request exceeds.
Then it calls `app.Respond`. The method writes the answer itself, with `WriteAll`, before returning.
At the exit of the block, the arena dies, then `Close` runs.

An error of `Accept` or of `Respond` stops `Serve` and rises. The first package does not skip a connection to continue the next.

The loop is in Why, in this package. The system calls stay in `os`.
Why can write this loop because the `arena` block is a word of the language, not a C function.
The façade cannot open the arena in its place: the arenas are calls inserted by the compiler.

The interface receives a copy of the value. This copy lives for the duration of `Serve`.
The value does not carry a pointer to the caller's arena.

The proof `testdata/serve` starts a thread per connection. This thread receives a concrete struct. An interface passes to a `thread` only a `freeze`, in an `arena shared` still open. `ServeTls` stays the unbounded loop. The TLS proof calls `AcceptTls` in `ServeConn`.
Two threads do not share the buffer. A value that must join them goes through a channel, or it is `freeze`.

## 8. Rejections

- No garbage collector behind these buffers. The named arena is the lifetime.
- No hidden allocation in `Read`. The arena is a parameter.
- No `char *` seen from Why. The handle is an `int`, the buffer is a `[]u8`.
- No function value to wire the server.
- No TLS written in Why.
- No event selection in the language. The wait is the call `Read` or `Accept`.
- No thread in the application to serve a connection.
- No JSON, no formatting, no Unicode. The bytes stay bytes.
- No shared position. Two threads open the same path twice.
- No tour page for the terminal, the client or the server.

## 9. Construction

Each step has its proof. The proof launches the `.wo` and looks at the exit code, or the diagnostic. It does not freeze the C.

1. Arenas, `defer`, `error`, `or return`. Already the next slice of the language. No library yet.
2. `Open`, `Read`, `Close`. Proof `testdata/fichier`: the file `data` (bytes 10, 20, 12), sum 42. `fichier.Read(a arena, chemin)` stays the next step.
3. `Lire(a arena, chemin)` and `Ecrire`. Proof `testdata/ecrire`: write the byte 42, read it back, sum 42. The example `lire` of `why.md` §4 takes the arena. A single package: the methods keep `Read` and `Write`.
4. `ReadLine`, with a pipe. The raw mode has a proof that restores the state even if the program stops by `defer`.
5. `Exchange` and `Serve` in the clear, on `127.0.0.1`, in the same proof. The exit code is the state read by `Status`.
6. The TLS link line. `DialTls` and `AcceptTls`. The proof `testdata/tls` is that of `Serve`: `ServeConn`, two clients, sum 42. `ServeTls`, the endless loop, is not in this proof.
7. `import`, the five directories, and the `.c` of the imported packages linked to the binary.
8. `thread`. `Serve` passes to a thread per connection. The proof launches two clients together and returns the sum of the two states.
9. `Seek` and `Tell`. This step follows `Open` and `(Fd) Read`. It does not follow `fichier.Read`. Proof: open a fixed file, seek to the middle, read the end. The sum of the bytes read is the exit code.
10. Sum in N threads. This step follows `Seek`. `thread` is already compiled. It does not wait for `select`, `freeze`, `arena shared`, nor `Serve`. The file, the bounds on the byte 10 and the sends of `int` are in §7 of `TODO.md`. The exit code is the sum, at most 255.

`extern` on `string` and `[]u8` is compiled. The `fichier.Read` of this file does not exist yet; the `lib.Lire` of the fixed package of the tour is not this one. The demo that only sees `int` is not named `Read`.

## 10. The sentence that stays

The sentences of `extern` are in `why.md` §9.

In §4 of `why.md`, the example `lire` takes the caller's arena. The body is that of section 4: `Size`, then `a.make`, then `(Fd) Read` that fills the buffer. `(Fd) Read` does not allocate. The slice returned dies with `a`. The proof `testdata/ecrire` names the functions `Lire` and `Ecrire`.
