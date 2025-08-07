#!/bin/bash
# create_tarball.sh - Create simple tarball distribution

VERSION="1.0"
PACKAGE_NAME="trbd-event-logger-${VERSION}"

# Create package directory
mkdir -p ${PACKAGE_NAME}

# Copy files
cp event_logger_qt.py ${PACKAGE_NAME}/
cp README.md ${PACKAGE_NAME}/
cp requirements.txt ${PACKAGE_NAME}/ 2>/dev/null || echo "PyQt6" > ${PACKAGE_NAME}/requirements.txt

# Create install script
cat > ${PACKAGE_NAME}/install.sh << 'EOF'
#!/bin/bash
echo "Installing TRBD Event Logger..."

# Install Python dependencies
pip3 install -r requirements.txt

# Copy to system location
sudo cp event_logger_qt.py /usr/local/bin/trbd-event-logger
sudo chmod +x /usr/local/bin/trbd-event-logger

# Create desktop entry
mkdir -p ~/.local/share/applications
cat > ~/.local/share/applications/trbd-event-logger.desktop << 'DESKTOP'
[Desktop Entry]
Name=TRBD Event Logger
Comment=Clinical Trial Event Logger
Exec=/usr/local/bin/trbd-event-logger
Icon=utilities-terminal
Terminal=false
Type=Application
Categories=Office;
DESKTOP

echo "Installation complete!"
echo "Run: trbd-event-logger"
EOF

chmod +x ${PACKAGE_NAME}/install.sh

# Create tarball
tar -czf ${PACKAGE_NAME}.tar.gz ${PACKAGE_NAME}/

echo "Created: ${PACKAGE_NAME}.tar.gz"
echo "Users can extract and run: ./install.sh"
