# Runix

A universal file runner for Linux. Drop a file, Runix figures out the language and runs it — no terminal needed.

> Born out of frustration with Linux file managers not having a proper "Run" option for scripts.

## Features

- Supports 18+ programming languages
- Drag & drop or file picker
- Compile-only or compile & run
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
- Language runtimes/compilers as needed (gcc, g++, python3, node, etc.)

## Command Line Usage

```bash
runix file.py              # Run a file
runix --compile file.c     # Compile only
runix --decompile binary   # Decompile an ELF binary
```

## License

[GNU General Public License v3.0](LICENSE)
