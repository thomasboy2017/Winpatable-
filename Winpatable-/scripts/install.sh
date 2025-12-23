#!/bin/bash
# Winpatable - Main Installation Script
# Installs Winpatable and all dependencies

set -e

echo "======================================================"
echo "Winpatable Installation Script"
echo "======================================================"

# Check if running on Linux
if [[ ! "$OSTYPE" == "linux-gnu"* ]]; then
    echo "✗ This script only works on Linux"
    exit 1
fi

# Detect OS via /etc/os-release and allow Debian-based systems
if [ -f /etc/os-release ]; then
    # shellcheck disable=SC1091
    . /etc/os-release
    OS_ID="${ID:-}"; OS_NAME="${NAME:-}"
    if ! echo "${OS_ID,,} ${OS_NAME,,}" | grep -E "ubuntu|linuxmint|mint|debian" > /dev/null; then
        echo "✗ This script requires Ubuntu, Linux Mint, or a Debian-based distro"
        exit 1
    fi
else
    echo "✗ Unable to detect OS (missing /etc/os-release)"
    exit 1
fi

# Check for sudo access
if ! sudo -n true 2>/dev/null; then
    echo "This installation requires sudo access"
    sudo -v
fi

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
INSTALL_DIR="/opt/winpatable"
BIN_DIR="/usr/local/bin"

# Detect package manager (prefer `apt` when available)
PKG_MGR="apt"
if ! command -v "$PKG_MGR" >/dev/null 2>&1; then
    if command -v apt-get >/dev/null 2>&1; then
        PKG_MGR="apt-get"
    else
        echo "✗ No supported Debian package manager found (apt/apt-get)"
        exit 1
    fi
fi

echo ""
echo "[1/5] Updating system packages..."
sudo "$PKG_MGR" update
sudo "$PKG_MGR" upgrade -y

echo ""
echo "[2/5] Installing system dependencies..."
sudo "$PKG_MGR" install -y \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    git \
    curl \
    wget \
    apt-transport-https

echo ""
echo "[3/5] Installing Python dependencies..."
pip3 install --user \
    setuptools \
    wheel \
    requests

echo ""
echo "[4/5] Installing Winpatable..."
sudo mkdir -p "$INSTALL_DIR"
sudo cp -r "$SCRIPT_DIR"/* "$INSTALL_DIR/"
sudo chmod +x "$INSTALL_DIR/src/winpatable.py"

# Create symlink to make winpatable command available
sudo ln -sf "$INSTALL_DIR/src/winpatable.py" "$BIN_DIR/winpatable"
sudo chmod +x "$BIN_DIR/winpatable"

echo ""
echo "[5/5] Creating configuration directory..."
mkdir -p ~/.winpatable
mkdir -p ~/.winpatable/applications
mkdir -p ~/.winpatable/wine
mkdir -p ~/.winpatable/gpu

echo ""
echo "======================================================"
echo "Installation Complete!"
echo "======================================================"
echo ""
echo "To get started:"
echo "  1. Run: winpatable detect"
echo "  2. Then: winpatable quick-start"
echo ""
echo "For help: winpatable --help"
echo ""
