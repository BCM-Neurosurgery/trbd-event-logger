#!/bin/bash
# build_deb.sh - Script to create Ubuntu .deb package

# Create package structure
mkdir -p trbd-event-logger_1.0/DEBIAN
mkdir -p trbd-event-logger_1.0/usr/local/bin
mkdir -p trbd-event-logger_1.0/usr/share/applications
mkdir -p trbd-event-logger_1.0/usr/share/doc/trbd-event-logger

# Copy application
cp event_logger_qt.py trbd-event-logger_1.0/usr/local/bin/trbd-event-logger
chmod +x trbd-event-logger_1.0/usr/local/bin/trbd-event-logger

# Create control file
cat > trbd-event-logger_1.0/DEBIAN/control << EOF
Package: trbd-event-logger
Version: 1.0
Section: utils
Priority: optional
Architecture: all
Depends: python3, python3-pyqt6
Maintainer: Baylor College of Medicine <your.email@bcm.edu>
Description: TRBD Clinical Trial Event Logger
 A cross-platform desktop application for logging clinical events
 during TRBD Clinical Trial interactions.
EOF

# Create desktop entry
cat > trbd-event-logger_1.0/usr/share/applications/trbd-event-logger.desktop << EOF
[Desktop Entry]
Name=TRBD Event Logger
Comment=Clinical Trial Event Logger
Exec=/usr/local/bin/trbd-event-logger
Icon=utilities-terminal
Terminal=false
Type=Application
Categories=Office;
EOF

# Copy documentation
cp README.md trbd-event-logger_1.0/usr/share/doc/trbd-event-logger/

# Build package
dpkg-deb --build trbd-event-logger_1.0

echo "Package created: trbd-event-logger_1.0.deb"
