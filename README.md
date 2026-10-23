# Runix

A universal file runner for Linux. Drop a file, Runix figures out the language and runs it — no terminal needed.

> Born out of frustration with Linux file managers not having a proper "Run" option for scripts.

## Features

- Supports 18 programming languages, plus JAR files and ELF binaries
- Drag & drop or file picker
- Compile-only or compile & run
- Program arguments (right-click **Run**)
- Custom compiler flags for C/C++ (`-std`, `-I`, `-include`, `-lm`)
- Decompile ELF binaries and JAR files (objdump, retdec, jadx)
- Recently run files list with search
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
| `Ctrl+H` | Recently run files |
| `Ctrl+.` | Open settings |
| `F5` | Run |
| `F6` | Compile only |
| `Esc` | Close file |

## Right-Click Menus

| Right-click on | What it does |
|----------------|--------------|
| **Run** button | Set program arguments |
| **Compile** button | Set C/C++ compiler flags (`.c` and `.cpp` only) |
| File button | Open the recently run files list |

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

## Dependencies

Required:

- Python 3
- PyQt6 (`python-pyqt6`)
- `file` (used to detect ELF binaries)
- A terminal emulator (Kitty, Konsole, Alacritty, GNOME Terminal, Xfce Terminal or GNOME Console)

Optional (install what you need):

- Language runtimes and compilers: `gcc`, `clang`, `nodejs`, `php`, `lua`, `ruby`, `perl`, a JDK, `go`, `rust`, `dart`, `swift`, `kotlin`, `nasm`, `dotnet`
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
