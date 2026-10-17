# Runix

A universal file runner for Linux. Drop a file, Runix figures out the language and runs it — no terminal needed.

> Born out of frustration with Linux file managers not having a proper "Run" option for scripts.

## Features

- Supports 18+ programming languages
- Drag & drop or file picker
- Compile-only or compile & run
- Custom compiler flags for C/C++ (`-std`, `-I`, `-include`, `-lm`)
- Decompile ELF binaries and JAR files (objdump, retdec, jadx)
- Recently run files list with search
- Configurable default terminal and compiler
- Keyboard shortcuts
- File manager integration via `.desktop` file

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

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+O` | Open file |
| `Ctrl+H` | Recently run files |
| `Ctrl+.` | Open settings |
| `F5` | Run |
| `F6` | Compile only |
| `Esc` | Close file |

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

## Installation

### AUR (Recommended)

Using yay:
```bash
yay -S runix
```

### Manual (via PKGBUILD)

```bash
git clone https://github.com/Pengu-54/Runix
cd Runix
makepkg -si
```

## Dependencies

- Python 3
- PyQt6 (`python-pyqt6`)
- A terminal emulator (Kitty, Konsole, Alacritty, GNOME Terminal, Xfce Terminal, GNOME Console)
- `file` (used to detect ELF binaries for the decompile button)
- Language runtimes/compilers as needed (gcc, g++, python3, node, etc.)

## Command Line Usage

```bash
runix file.py              # Run a file
runix --compile file.c     # Compile only
runix --decompile binary   # Decompile an ELF binary
```

## License

[GNU General Public License v3.0](LICENSE)
