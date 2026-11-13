# Maintainer: Pengu-54
pkgname=runix
pkgver=1.7
pkgrel=1
pkgdesc="Universal file runner for Linux — drop a file, Runix runs or compiles it"
arch=('any')
url="https://github.com/Pengu-54/Runix"
license=('GPL-3.0-only')
depends=('python' 'python-pyqt6' 'file')
optdepends=(
    'gcc: C/C++ compiling'
    'clang: alternative C/C++ compiler'
    'pkgconf: auto library detection via pkg-config'
    'qt6-base: Qt apps (auto-detect)'
    'glfw: GLFW apps (auto-detect)'
    'vulkan-icd-loader: Vulkan apps (auto-detect)'
    'gtk4: GTK4 apps (auto-detect)'
    'gtk3: GTK3 fallback (auto-detect)'
    'sdl2: SDL2 apps (auto-detect)'
    'sfml: SFML apps (auto-detect)'
    'ncurses: ncurses apps (auto-detect)'
    'curl: libcurl apps (auto-detect)'
    'nodejs: JavaScript/TypeScript'
    'qt6-wayland: native Wayland support (Display Backend setting)'
    'binutils: objdump decompiling'
    'jadx: JAR decompiling'
    'retdec: ELF decompiling'
    'libnotify: decompile notifications'
    'kitty: terminal emulator'
    'konsole: terminal emulator'
    'alacritty: terminal emulator'
    'gnome-terminal: terminal emulator'
    'gnome-console: terminal emulator (kgx)'
    'xfce4-terminal: terminal emulator'
)
source=("https://github.com/Pengu-54/Runix/archive/refs/tags/v${pkgver}.tar.gz")
sha256sums=('SKIP')

package() {
    cd "$srcdir/Runix-${pkgver}"

    # Core Python modules
    install -Dm755 Runix.py                "$pkgdir/usr/share/runix/Runix.py"
    install -Dm644 Runixui.py              "$pkgdir/usr/share/runix/Runixui.py"
    install -Dm644 runixsetting.py         "$pkgdir/usr/share/runix/runixsetting.py"
    install -Dm644 runixsettingui.py       "$pkgdir/usr/share/runix/runixsettingui.py"
    install -Dm644 runix_flag_window.py    "$pkgdir/usr/share/runix/runix_flag_window.py"
    install -Dm644 ui_runix_flag_ui.py     "$pkgdir/usr/share/runix/ui_runix_flag_ui.py"
    install -Dm644 runix_al.py             "$pkgdir/usr/share/runix/runix_al.py"
    install -Dm644 ui_runix_language_ui.py "$pkgdir/usr/share/runix/ui_runix_language_ui.py"

    # Auto library detection + UI
    install -Dm644 librarydetect.py        "$pkgdir/usr/share/runix/librarydetect.py"
    install -Dm644 runix_library.py        "$pkgdir/usr/share/runix/runix_library.py"
    install -Dm644 ui_runix_library.py     "$pkgdir/usr/share/runix/ui_runix_library.py"

    # Icon
    install -Dm644 Runix.svg \
        "$pkgdir/usr/share/icons/hicolor/scalable/apps/Runix.svg"

    # Desktop entry
    install -Dm644 runix.desktop \
        "$pkgdir/usr/share/applications/runix.desktop"

    # Launcher (cd so relative imports work)
    install -dm755 "$pkgdir/usr/bin"
    cat > "$pkgdir/usr/bin/runix" << 'EOF'
#!/bin/bash
cd /usr/share/runix && exec python3 Runix.py "$@"
EOF
    chmod 755 "$pkgdir/usr/bin/runix"
}
