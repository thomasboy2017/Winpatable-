#!/usr/bin/env python3

# Winpatable One-Click Installation Script
# Just run: curl -sSL https://raw.githubusercontent.com/thomasboy2017/Winpatable-/main/install.sh | bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
print_header() {
    echo -e "\n${BLUE}╔════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║${NC} $1"
    echo -e "${BLUE}╚════════════════════════════════════════╝${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Check system
check_system() {
    print_header "Checking System Requirements"
    
    # Check OS
    if [[ ! "$OSTYPE" == "linux-gnu"* ]]; then
        print_error "This script only works on Linux"
        exit 1
    fi
    
    if ! grep -E "ubuntu|linuxmint|debian" /etc/os-release > /dev/null 2>&1; then
        print_warning "This is optimized for Ubuntu/Mint, but may work on other Debian-based systems"
    fi
    print_success "Linux system detected"
    
    # Check architecture
    if [[ $(uname -m) != "x86_64" ]]; then
        print_error "This script requires x86_64 architecture"
        exit 1
    fi
    print_success "x86_64 architecture confirmed"
    
    # Check internet
    if ! ping -c 1 8.8.8.8 > /dev/null 2>&1; then
        print_warning "No internet connection detected. Install will fail."
        read -p "Continue anyway? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
    print_success "Internet connection confirmed"
}

# Install dependencies
install_dependencies() {
    print_header "Installing Dependencies"
    
    # Update package manager
    print_info "Updating package manager..."
    sudo apt update > /dev/null 2>&1
    print_success "Package manager updated"
    
    # Check if Python is installed
    if ! command -v python3 &> /dev/null; then
        print_info "Installing Python 3..."
        sudo apt install -y python3 python3-pip > /dev/null 2>&1
        print_success "Python 3 installed"
    else
        print_success "Python 3 already installed"
    fi
    
    # Install basic tools
    TOOLS="git curl wget build-essential"
    print_info "Installing basic tools..."
    sudo apt install -y $TOOLS > /dev/null 2>&1
    print_success "Basic tools installed"
}

# Clone repository
clone_repository() {
    print_header "Downloading Winpatable"
    
    INSTALL_DIR="${1:-.}"
    
    if [ -d "$INSTALL_DIR/Winpatable-" ]; then
        print_info "Updating existing installation..."
        cd "$INSTALL_DIR/Winpatable-"
        git pull origin main > /dev/null 2>&1
        print_success "Updated to latest version"
    else
        print_info "Cloning repository..."
        git clone https://github.com/thomasboy2017/Winpatable-.git "$INSTALL_DIR/Winpatable-" > /dev/null 2>&1
        print_success "Repository cloned"
    fi
    
    echo "$INSTALL_DIR/Winpatable-"
}

# Setup Python environment
setup_python_env() {
    print_header "Setting Up Python Environment"
    
    REPO_DIR="$1"
    
    print_info "Creating virtual environment..."
    python3 -m venv "$REPO_DIR/venv" > /dev/null 2>&1
    print_success "Virtual environment created"
    
    print_info "Activating virtual environment..."
    source "$REPO_DIR/venv/bin/activate"
    print_success "Virtual environment activated"
    
    print_info "Installing Python dependencies..."
    pip install -q --upgrade pip setuptools wheel
    pip install -q -r "$REPO_DIR/requirements.txt"
    print_success "Python dependencies installed"
}

# Create Launcher Script
print_info "creating launcher script..."
Launcher="$INSTALL_DIR.scripts"
sudo mkdir -p "$INSTALL`_DIR/scripts"
CAT << 'EOF' | sudo tee "$Launcher/winpatable" > /dev/null
#!/bin/bash
    python3 /opt/winpatable/scripts/winpatable.py "$@"
EOF
sudo chmod +x "$Launcher/winpatable"
print_success "Launcher script created at $Launcher/winpatable"

#Create symlink to launcher
print_info "Creating symlink to /usr/local/bin..."
sudo ln -sf "$Launcher/winpatable" /usr/local/bin/winpatable
print_success "Symlink created at /usr/local/bin/winpatable" and "command 'winpatable' created"
    # Create user directory
    print_info "Creating user configuration directory..."
    mkdir -p ~/.winpatable/applications
    mkdir -p ~/.winpatable/wine
    mkdir -p ~/.winpatable/gpu
    print_success "Configuration directories created"
}

# Main installation
main() {
    clear
    
    echo -e "${BLUE}"
    cat << "EOF"
╔═══════════════════════════════════════════════════════╗
║                                                       ║
║       WINPATABLE - Windows Compatibility Layer       ║
║            For Linux Mint & Ubuntu                    ║
║                                                       ║
║  Run Windows Applications on Linux with GPU Support  ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
    
    # Check requirements
    check_system
    
    # Ask for installation directory
    print_header "Installation Directory"
    read -p "Install to [/opt/winpatable]: " INSTALL_DIR
    INSTALL_DIR="${INSTALL_DIR:-/opt/winpatable}"
    print_info "Installation directory: $INSTALL_DIR"
    
    # Install dependencies
    install_dependencies
    
    # Clone repository
    REPO_DIR=$(clone_repository "/tmp")
    
    # Setup Python
    setup_python_env "$REPO_DIR"
    
    # Setup installation
    setup_installation "$REPO_DIR" "$INSTALL_DIR"
    
    # Print summary
    print_header "Installation Complete!"
    echo -e "${GREEN}Winpatable is now installed!${NC}\n"
    
    echo -e "${BLUE}Getting Started:${NC}"
    echo ""
    echo "  ${YELLOW}Option 1: Interactive Setup (Recommended for first-time users)${NC}"
    echo "     python3 $INSTALL_DIR/scripts/wizard.py"
    echo ""
    echo "  ${YELLOW}Option 2: Quick Automatic Setup${NC}"
    echo "     winpatable quick-start"
    echo ""
    echo "  ${YELLOW}Option 3: Manual Steps${NC}"
    echo "     1. Check system:  winpatable detect"
    echo "     2. Install apps:  winpatable install-app office --installer path/to/file.exe"
    echo ""
    
    echo -e "${BLUE}Helpful Commands:${NC}"
    echo "  • ${YELLOW}winpatable --help${NC} ........................... View all commands"
    echo "  • ${YELLOW}winpatable detect${NC} ......................... Check your system"
    echo "  • ${YELLOW}winpatable list-apps${NC} ....................... See supported applications"
    echo "  • ${YELLOW}winpatable performance-tuning${NC} .............. Get optimization tips"
    echo ""
    
    echo -e "${BLUE}Documentation:${NC}"
    echo "  • Quick Start Guide: $INSTALL_DIR/QUICK_START.md"
    echo "  • Application Guides: $INSTALL_DIR/docs/APPLICATION_GUIDES.md"
    echo "  • Troubleshooting: $INSTALL_DIR/TROUBLESHOOTING.md"
    echo "  • GPU Setup Guide: $INSTALL_DIR/docs/GPU_GUIDE.md"
    echo ""
    
    echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
    print_success "Winpatable is ready to use!"
    echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
    echo ""
}

# Run main
main "$@"
