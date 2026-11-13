# Runix

A universal file runner for Linux. Drop a file, Runix figures out the language and runs it — no terminal needed.

> Born out of frustration with Linux file managers not having a proper "Run" option for scripts.

## Features

- Supports 18 programming languages, plus JAR files and ELF binaries
- Drag & drop or file picker
- Compile-only or compile & run
- Program arguments (right-click **Run**)
- Custom compiler flags for C/C++ (`-std`, `-I`, `-include`, `-lm`)
- **Automatic C/C++ library detection** (Qt, GTK, GLFW, Vulkan, SDL2, SFML, ncurses, curl, math, …)
- Decompile ELF binaries and JAR files (objdump, retdec, jadx)
- Recently run **files** and **commands** (copy the exact compile/run line)
- Add your own languages (custom interpreters and compilers)
- Configurable default terminal, compilers and decompiler
- Display backend setting (X11 / Wayland)
- Built-in help and one-click settings reset
- Keyboard shortcuts
- File manager integration via `.desktop` file ("Open with Runix")

## Supported Languages

| Language | Extension | Type |
|----------|-----------|------|
| Python | `.py` | Interpreted |
| JavaScript | `.js` | Interpreted |
| TypeScript | `.ts` | Interpreted |
| PHP | `.php` | Interpreted |
| Lua | `.lua` | Interpreted |
| Ruby | `.rb` | Interpreted |
| Perl | `.pl` | Interpreted |
| Bash | `.sh` | Interpreted |
| C | `.c` | Compiled |
| C++ | `.cpp` | Compiled |
| Go | `.go` | Compiled |
| Rust | `.rs` | Compiled |
| Dart | `.dart` | Compiled |
| Swift | `.swift` | Compiled |
| Kotlin | `.kt` | Compiled |
| Java | `.java` | Compiled |
| Assembly (NASM) | `.asm` | Compiled |
| C# | `.cs` | Compiled |
| JAR | `.jar` | Bytecode |
| ELF Binary | — | Binary |

> C# files are run with `dotnet run file.cs`, which needs a .NET SDK that supports running a single file.

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+O` | Open file |
| `Ctrl+H` | Recently run files and commands |
| `Ctrl+.` | Open settings |
| `F5` | Run |
| `F6` | Compile only |
| `Esc` | Close file |

## Right-Click Menus

| Right-click on | What it does |
|----------------|--------------|
| **Run** button | Set program arguments |
| **Compile** button | Set C/C++ compiler flags (`.c` and `.cpp` only) |
| File button | Open the recently run files and commands list |

## Program Arguments

Right-click the **Run** button to pass arguments to the program you are about to run. Type them the way you would in a shell:

```
5 --verbose "hello world"
```

The program receives three arguments: `5`, `--verbose` and `hello world`.

Notes:

- Works for interpreted languages, compiled languages (the compiled program receives them), JAR files and ELF binaries.
- Arguments are **single-use**. They are cleared after you run the file, and also when you select another file or close the current one (`Esc`).
- Arguments apply to the graphical window only, not to the command line mode.

## Compiler Flags (C / C++)

Right-click the **Compile** button to open the flags window. It is available for `.c` and `.cpp` files.

| Field | Passed to the compiler as | Example input |
|-------|---------------------------|---------------|
| `-std` | `-std=<value>` | `c++20` |
| `-I` | `-I<path>` | `/home/user/project/include` |
| `-include` | `-include <file>` | `config.h` |
| `-lm` (checkbox) | `-lm` | Links the math library |

Press **Save** to apply the flags, then use **F5** (compile & run) or **F6** (compile only) as usual.

Notes:

- Flags are **single-use**. They are cleared after the file is compiled successfully, and also when you select another file or close the current one (`Esc`).
- If the compilation fails, the flags are kept so you can fix the code and try again.
- Runix uses your default C/C++ compiler (gcc/g++ or clang/clang++) from the settings.
- Paths containing spaces are supported.
- Manual flags work together with **automatic library detection** (see below).

## Automatic library detection (C / C++)

Before compiling a `.c` or `.cpp` file, Runix scans `#include` lines and adds linker / pkg-config flags when it recognizes a known library.

Built-in detections (defaults; stored in `~/.config/runix/librarys.json` on first use):

| Include (example) | Flags / pkg-config |
|-------------------|--------------------|
| `#include <QApplication>` | `pkg-config Qt6Widgets` (fallback Qt5Widgets) |
| `#include <GLFW/glfw3.h>` | `-lglfw -lGL -ldl` |
| `#include <vulkan/vulkan.h>` | `-lvulkan` |
| `#include <gtk/gtk.h>` | `pkg-config gtk4` (fallback gtk+-3.0) |
| `#include <math.h>` | `-lm` |
| `#include <curl/curl.h>` | `pkg-config libcurl` |
| `#include <SFML/Graphics.hpp>` | `pkg-config sfml-all` (fallback sfml-graphics) |
| `#include <SDL2/SDL.h>` | `pkg-config sdl2` |
| `#include <ncurses.h>` | `pkg-config ncurses` |

You can add more headers and flags from the **library** UI (or by editing `librarys.json`).  
`pkg-config` is recommended for packages that ship a `.pc` file (`pkgconf` on Arch).

The exact command Runix ran (including auto flags) appears under **Most Recently Run Command**.

## Recently Run Files and Commands

Press `Ctrl+H` (or right-click the file button) to open the history window. The drop-down at the top switches between two lists:

- **Most Recently Run Files** — click a file to select it again.
- **Most Recently Run Command** — shows the exact command Runix ran, with any compiler flags and program arguments. Click a command to copy it to the clipboard, then paste it into a terminal.

Both lists have a search box and a **Clear** button.

## Custom Languages

Runix runs the languages in the table above out of the box. For any other language, add it yourself in the **Add Language** window. Each language you add is saved as a small JSON file in `~/.config/runix/custom_lang/` (for example `.f90.json`).

The window asks for:

| Field | What to enter |
|-------|---------------|
| Exec | The command, using the placeholders below |
| File extension | For example `jl` or `.jl` (the dot is added for you) |
| Compiler or Interpreter name | The program Runix checks for, for example `julia` |
| Interpreter / Compile | Whether the file is run directly or compiled first |
| Compiled File Type Extension | `ELF` for a native program, or an extension such as `.jar` (compile only) |
| Execute command | How to run the compiled file (compile only, not used for `ELF`) |

### Placeholders

Write commands with these placeholders instead of real file names. Each placeholder must be a separate word, for example `-o rcc=compiledfile` (not `-orcc=compiledfile`):

| Placeholder | Replaced with |
|-------------|---------------|
| `rcc=file` | The full path of the file you are running |
| `rcc=compiledfile` | The compiled file name (without the folder). For `ELF` this is the file name without extension, otherwise the extension from "Compiled File Type Extension" is added |

### Examples

An interpreted language (Julia):

| Field | Value |
|-------|-------|
| Exec | `julia rcc=file` |
| File extension | `.jl` |
| Name | `julia` |
| Type | Interpreter |

A compiled language that produces a native program (Fortran):

| Field | Value |
|-------|-------|
| Exec | `gfortran rcc=file -o rcc=compiledfile` |
| File extension | `.f90` |
| Name | `gfortran` |
| Type | Compile |
| Compiled File Type Extension | `ELF` |

Notes:

- Extensions of built-in languages (`.py`, `.c`, ...) cannot be overridden.
- Custom file extensions appear in the file picker, and the **Compile** button shows up for languages of type Compile.
- Custom languages work from the command line too.
- To remove a language, delete its file from `~/.config/runix/custom_lang/`.

## Settings

Open the settings with `Ctrl+.` or the `...` button.

| Tab | What you can change |
|-----|---------------------|
| Default terminal | Which terminal Runix opens (Auto, Kitty, Konsole, Alacritty, GNOME Terminal, GNOME Console, Xfce Terminal) |
| Default compiler | C++ compiler (g++ / clang++) and C compiler (gcc / clang) |
| Default decompiler/disassembler | objdump or retdec for ELF binaries |
| Runix | Display backend, help and reset |

### Runix tab

- **Display Backend** — choose **X11** (default) or **Wayland**. Restart Runix for the change to take effect. Wayland needs the `qt6-wayland` package.
- **Help** — shortcuts and right-click menus at a glance.
- **Reset Settings** — restores the default settings after a confirmation.

## Installation

### AUR

An AUR package is planned. AUR submissions are currently restricted, so for now use the manual install below.

### Manual (via PKGBUILD)

```bash
git clone https://github.com/Pengu-54/Runix
cd Runix
makepkg -si
```

Replace `sha256sums=('SKIP')` with the real checksum before publishing (`makepkg -g`).

## Dependencies

Required:

- Python 3
- PyQt6 (`python-pyqt6`)
- `file` (used to detect ELF binaries)
- A terminal emulator (Kitty, Konsole, Alacritty, GNOME Terminal, Xfce Terminal or GNOME Console)

Optional (install what you need):

- Language runtimes and compilers: `gcc`, `clang`, `nodejs`, `php`, `lua`, `ruby`, `perl`, a JDK, `go`, `rust`, `dart`, `swift`, `kotlin`, `nasm`, `dotnet`
- Auto-detect / libraries: `pkgconf`, Qt6, GLFW, Vulkan loader, GTK4/GTK3, SDL2, SFML, ncurses, curl
- `binutils` for objdump, `jadx` for JAR decompiling, `retdec` for ELF decompiling
- `libnotify` for decompile notifications
- `qt6-wayland` to run natively on Wayland

## Command Line Usage

```bash
runix file.py              # Run a file
runix file1.py file2.c     # Run several files
runix --compile file.c     # Compile only
runix --decompile binary   # Decompile an ELF binary or JAR

runix --setterminal Kitty  # Set the default terminal
runix --setccompiler gcc   # Set the default C compiler (gcc or clang)
runix --setcppcompiler g++ # Set the default C++ compiler (g++ or clang++)
```

Running `runix` without arguments opens the window.

## Security

Runix runs the file you give it without asking for confirmation. Only run files you trust, and be careful when making Runix the default app for a file type.

## License

[GNU General Public License v3.0](LICENSE)
