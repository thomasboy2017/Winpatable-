#!/bin/bash
# Universal Winpatable Installer
# Usage: curl -sSL https://raw.githubusercontent.com/thomasboy2017/Winpatable-/version.1.1/install.sh | bash

set -e

# Colors
GREEN='\033[0;32m'; RED='\033[0;31m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'

msg() { echo -e "${BLUE}ℹ${NC} $1"; }
ok()  { echo -e "${GREEN}✓${NC} $1"; }
warn(){ echo -e "${YELLOW}⚠${NC} $1"; }
err() { echo -e "${RED}✗${NC} $1"; }

# Detect package manager
detect_pkg() {
    if command -v apt &>/dev/null; then PKG=apt
    elif command -v dnf &>/dev/null; then PKG=dnf
    elif command -v pacman &>/dev/null; then PKG=pacman
    else err "Unsupported distro"; exit 1; fi
    ok "Detected package manager: $PKG"
}

# Install dependencies
install_deps() {
    msg "Installing dependencies..."
    case $PKG in
        apt)
            sudo apt update -y
            sudo apt install -y git curl wget build-essential python3 python3-pip
            ;;
        dnf)
            sudo dnf install -y git curl wget gcc gcc-c++ make python3 python3-pip
            ;;
        pacman)
            sudo pacman -Sy --noconfirm git curl wget base-devel python python-pip
            ;;
    esac
    ok "Dependencies installed"
}

# GPU driver setup
setup_gpu() {
    GPU=$(lspci | grep -E "VGA|3D" | grep -i "nvidia\|amd\|intel" || true)
    [[ -z "$GPU" ]] && { warn "No GPU detected"; return; }
    msg "Detected GPU: $GPU"

    case $PKG in
        apt)
            if echo "$GPU" | grep -qi nvidia; then sudo apt install -y nvidia-driver-535
            elif echo "$GPU" | grep -qi amd; then sudo apt install -y mesa-vulkan-drivers mesa-utils
            elif echo "$GPU" | grep -qi intel; then sudo apt install -y intel-media-va-driver mesa-vulkan-drivers; fi
            ;;
        dnf)
            if echo "$GPU" | grep -qi nvidia; then sudo dnf install -y akmod-nvidia xorg-x11-drv-nvidia-cuda
            elif echo "$GPU" | grep -qi amd; then sudo dnf install -y mesa-dri-drivers mesa-vulkan-drivers
            elif echo "$GPU" | grep -qi intel; then sudo dnf install -y intel-media-driver mesa-vulkan-drivers; fi
            ;;
        pacman)
            if echo "$GPU" | grep -qi nvidia; then sudo pacman -S --noconfirm nvidia nvidia-utils
            elif echo "$GPU" | grep -qi amd; then sudo pacman -S --noconfirm mesa vulkan-radeon
            elif echo "$GPU" | grep -qi intel; then sudo pacman -S --noconfirm mesa vulkan-intel; fi
            ;;
    esac
    ok "GPU drivers installed"
}

# Clone and install
install_winpatable() {
    msg "Cloning Winpatable..."
    git clone https://github.com/thomasboy2017/Winpatable-.git /tmp/Winpatable- || true
    cd /tmp/Winpatable-
    python3 -m venv venv && source venv/bin/activate
    pip install -q --upgrade pip setuptools wheel
    pip install -q -r requirements.txt
    sudo mkdir -p /opt/winpatable
    sudo cp -r ./* /opt/winpatable/
    sudo ln -sf /opt/winpatable/src/winpatable.py /usr/local/bin/winpatable
    sudo chmod +x /usr/local/bin/winpatable
    mkdir -p ~/.winpatable/{applications,wine,gpu}
    ok "Winpatable installed"
}

# Post-install test
gpu_test() {
    msg "Testing GPU setup..."
    if command -v glxinfo &>/dev/null; then glxinfo | grep "OpenGL renderer"
    elif command -v vulkaninfo &>/dev/null; then vulkaninfo | grep "GPU id"
    else warn "No GPU test tool found"; fi
}

### Main
clear
echo -e "${BLUE}=== Winpatable Universal Installer ===${NC}"
detect_pkg
install_deps
setup_gpu
install_winpatable
gpu_test
echo -e "${GREEN}✓ Installation complete! Run 'winpatable --help' to get started.${NC}"
