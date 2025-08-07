#!/bin/bash
# build_appimage.sh - Create AppImage for universal Linux distribution

# Install required tools
# wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
# chmod +x appimagetool-x86_64.AppImage

# Create AppDir structure
mkdir -p TRBD-Event-Logger.AppDir/usr/bin
mkdir -p TRBD-Event-Logger.AppDir/usr/share/applications
mkdir -p TRBD-Event-Logger.AppDir/usr/share/icons/hicolor/256x256/apps

# Copy application
cp event_logger_qt.py TRBD-Event-Logger.AppDir/usr/bin/trbd-event-logger
chmod +x TRBD-Event-Logger.AppDir/usr/bin/trbd-event-logger

# Create desktop file
cat > TRBD-Event-Logger.AppDir/usr/share/applications/trbd-event-logger.desktop << EOF
[Desktop Entry]
Name=TRBD Event Logger
Comment=Clinical Trial Event Logger
Exec=trbd-event-logger
Icon=trbd-event-logger
Terminal=false
Type=Application
Categories=Office;
EOF

# Copy desktop file to AppDir root
cp TRBD-Event-Logger.AppDir/usr/share/applications/trbd-event-logger.desktop TRBD-Event-Logger.AppDir/

# Create AppRun script
cat > TRBD-Event-Logger.AppDir/AppRun << 'EOF'
#!/bin/bash
HERE="$(dirname "$(readlink -f "${0}")")"
exec "${HERE}/usr/bin/trbd-event-logger" "$@"
EOF
chmod +x TRBD-Event-Logger.AppDir/AppRun

# Build AppImage
# ./appimagetool-x86_64.AppImage TRBD-Event-Logger.AppDir

echo "AppImage structure created in TRBD-Event-Logger.AppDir/"
echo "Run appimagetool to create final AppImage"
