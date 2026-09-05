# Maintainer: Pengu-54
pkgname=runix
pkgver=1.0
pkgrel=1
pkgdesc="Universal file runner for Linux"
arch=('any')
url="https://github.com/Pengu-54/Runix"
license=('GPL3')
depends=('python' 'python-pyqt6')
source=("https://github.com/Pengu-54/Runix/archive/refs/tags/v${pkgver}.tar.gz")
sha256sums=('SKIP')

package() {
    cd "$srcdir/Runix-${pkgver}"

    # Install Python files
    install -Dm755 Runix.py "$pkgdir/usr/share/runix/Runix.py"
    install -Dm644 Runixui.py "$pkgdir/usr/share/runix/Runixui.py"
    install -Dm644 runixsetting.py "$pkgdir/usr/share/runix/runixsetting.py"
    install -Dm644 runixsettingui.py "$pkgdir/usr/share/runix/runixsettingui.py"

    # Install icon
    install -Dm644 Runix.svg "$pkgdir/usr/share/icons/hicolor/scalable/apps/Runix.svg"

    # Install .desktop file
    install -Dm644 runix.desktop "$pkgdir/usr/share/applications/runix.desktop"

    # Create launcher script
    install -dm755 "$pkgdir/usr/bin"
    echo '#!/bin/bash
python3 /usr/share/runix/Runix.py "$@"' > "$pkgdir/usr/bin/runix"
    chmod 755 "$pkgdir/usr/bin/runix"
}
