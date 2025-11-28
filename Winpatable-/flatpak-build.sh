#!/bin/bash
# Winpatable Flatpak Build Script
# This script builds a Flatpak package for Winpatable

set -e

APP_ID="org.winpatable.Winpatable"
MANIFEST="org.winpatable.Winpatable.yml"
BUILD_DIR="flatpak-build"
REPO_DIR="flatpak-repo"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_header() {
    echo -e "\n${GREEN}=== $1 ===${NC}\n"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# Check if flatpak and flatpak-builder are installed
check_tools() {
    print_header "Checking System Tools"
    
    if ! command -v flatpak &> /dev/null; then
        print_error "flatpak is not installed"
        echo "Install with: sudo apt install flatpak flatpak-builder"
        exit 1
    fi
    print_success "flatpak found"
    
    if ! command -v flatpak-builder &> /dev/null; then
        print_error "flatpak-builder is not installed"
        echo "Install with: sudo apt install flatpak-builder"
        exit 1
    fi
    print_success "flatpak-builder found"
    
    # Add Flathub repo if not present
    if ! flatpak remote-list | grep -q flathub; then
        print_info "Adding Flathub remote..."
        flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
        print_success "Flathub remote added"
    else
        print_success "Flathub remote already configured"
    fi
}

# Install runtime and SDK if needed
install_runtime() {
    print_header "Installing Flatpak Runtime"
    
    RUNTIME="org.freedesktop.Platform"
    RUNTIME_VERSION="23.08"
    SDK="org.freedesktop.Sdk"
    
    # Install runtime
    if ! flatpak list --app | grep -q "$RUNTIME"; then
        print_info "Installing $RUNTIME/$RUNTIME_VERSION..."
        flatpak install -y flathub "$RUNTIME/x86_64/$RUNTIME_VERSION" || true
        print_success "Runtime installed"
    else
        print_success "Runtime already installed"
    fi
    
    # Install SDK
    if ! flatpak list --app | grep -q "$SDK"; then
        print_info "Installing $SDK/$RUNTIME_VERSION..."
        flatpak install -y flathub "$SDK/x86_64/$RUNTIME_VERSION" || true
        print_success "SDK installed"
    else
        print_success "SDK already installed"
    fi
}

# Build the Flatpak
build_flatpak() {
    print_header "Building Flatpak Package"
    
    # Clean previous build
    if [ -d "$BUILD_DIR" ]; then
        print_info "Cleaning previous build..."
        rm -rf "$BUILD_DIR"
    fi
    
    # Create build directory
    mkdir -p "$BUILD_DIR"
    
    print_info "Running flatpak-builder..."
    flatpak-builder --force-clean \
        --install-deps-from=flathub \
        --ccache \
        "$BUILD_DIR" \
        "$MANIFEST" || {
        print_error "Build failed"
        exit 1
    }
    
    print_success "Flatpak built successfully"
}

# Export as single-file bundle
export_flatpak() {
    print_header "Exporting Flatpak Bundle"
    
    mkdir -p "$REPO_DIR"
    
    # Export as repository
    print_info "Exporting as repository..."
    flatpak build-export "$REPO_DIR" "$BUILD_DIR" || {
        print_error "Export failed"
        exit 1
    }
    print_success "Repository created"
    
    # Create single-file bundle
    print_info "Creating single-file bundle..."
    flatpak build-bundle "$REPO_DIR" "Winpatable.flatpak" "$APP_ID" || {
        print_error "Bundle creation failed"
        exit 1
    }
    print_success "Flatpak bundle created: Winpatable.flatpak"
}

# Summary and installation instructions
print_summary() {
    print_header "Build Complete!"
    
    echo -e "${GREEN}Flatpak package created: $(pwd)/Winpatable.flatpak${NC}"
    echo -e "\n${YELLOW}Installation Instructions:${NC}\n"
    
    echo "1. Install the Flatpak:"
    echo -e "   ${GREEN}flatpak install Winpatable.flatpak${NC}"
    echo ""
    echo "2. Run Winpatable:"
    echo -e "   ${GREEN}flatpak run org.winpatable.Winpatable${NC}"
    echo ""
    echo "3. (Optional) Add to application menu:"
    echo -e "   ${GREEN}flatpak install --assume-yes Winpatable.flatpak${NC}"
    echo ""
    
    echo -e "${YELLOW}Distribution:${NC}\n"
    echo "Upload to Flathub for wider distribution:"
    echo "1. Fork: https://github.com/flathub/flathub"
    echo "2. Add manifest to: new-apps/org.winpatable.Winpatable.yml"
    echo "3. Submit Pull Request"
    echo ""
}

# Main execution
main() {
    echo -e "${GREEN}"
    echo "╔══════════════════════════════════════╗"
    echo "║      Winpatable Flatpak Builder      ║"
    echo "╚══════════════════════════════════════╝"
    echo -e "${NC}"
    
    check_tools
    install_runtime
    build_flatpak
    export_flatpak
    print_summary
}

# Run main
main "$@"
