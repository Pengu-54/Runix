# Maintainer: Pengu-54
pkgname=runix
pkgver=1.6
pkgrel=1
pkgdesc="Universal file runner for Linux"
arch=('any')
url="https://github.com/Pengu-54/Runix"
license=('GPL3')
depends=('python' 'python-pyqt6' 'file')
optdepends=('gcc: C/C++ compiling'
            'clang: alternative C/C++ compiler'
            'nodejs: JavaScript/TypeScript'
            'qt6-wayland: native Wayland support (Display Backend setting)'
            'binutils: objdump decompiling'
            'jadx: JAR decompiling'
            'retdec: ELF decompiling'
            'libnotify: decompile notifications'
            'kitty: terminal emulator'
            'konsole: terminal emulator'
            'alacritty: terminal emulator')
source=("https://github.com/Pengu-54/Runix/archive/refs/tags/v${pkgver}.tar.gz")
sha256sums=('SKIP')

package() {
    cd "$srcdir/Runix-${pkgver}"

    # Install Python files
    install -Dm755 Runix.py "$pkgdir/usr/share/runix/Runix.py"
    install -Dm644 Runixui.py "$pkgdir/usr/share/runix/Runixui.py"
    install -Dm644 runixsetting.py "$pkgdir/usr/share/runix/runixsetting.py"
    install -Dm644 runixsettingui.py "$pkgdir/usr/share/runix/runixsettingui.py"
    install -Dm644 runix_flag_window.py "$pkgdir/usr/share/runix/runix_flag_window.py"
    install -Dm644 ui_runix_flag_ui.py "$pkgdir/usr/share/runix/ui_runix_flag_ui.py"
    install -Dm644 runix_al.py "$pkgdir/usr/share/runix/runix_al.py"
    install -Dm644 ui_runix_language_ui.py "$pkgdir/usr/share/runix/ui_runix_language_ui.py"
    
    # Install icon
    install -Dm644 Runix.svg "$pkgdir/usr/share/icons/hicolor/scalable/apps/Runix.svg"

    # Install .desktop file
    install -Dm644 runix.desktop "$pkgdir/usr/share/applications/runix.desktop"

    # Create launcher script
    install -dm755 "$pkgdir/usr/bin"
    echo '#!/bin/bash
exec python3 /usr/share/runix/Runix.py "$@"' > "$pkgdir/usr/bin/runix"
    chmod 755 "$pkgdir/usr/bin/runix"
}
