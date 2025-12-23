# Winpatable Flatpak Build Guide

This guide explains how to build and distribute Winpatable as a Flatpak package for Linux.

## What is Flatpak?

Flatpak is a universal packaging format for Linux applications that:
- Works on all Linux distributions
- Provides sandboxing and security
- Simplifies installation and updates
- Manages dependencies automatically

## Prerequisites

### System Requirements
- Linux system with Flatpak support
- Internet connection (for downloading dependencies)
- ~2GB free disk space (for build artifacts)
- x86_64 architecture

### Required Tools

Install Flatpak and build tools:

```bash
# Ubuntu/Linux Mint
sudo apt install flatpak flatpak-builder build-essential git

# Fedora
sudo dnf install flatpak flatpak-builder gcc gcc-c++ git

# openSUSE
sudo zypper install flatpak flatpak-builder gcc gcc-c++ git
```

### Add Flathub Repository

```bash
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
```

## Building the Flatpak

### Quick Build (Automated)

The easiest way is to use the provided build script:

```bash
chmod +x flatpak-build.sh
./flatpak-build.sh
```

This script will:
1. Check for required tools
2. Install the Flatpak runtime and SDK
3. Build the Flatpak package
4. Create a distributable bundle

### Manual Build

If you prefer to build manually:

```bash
# Install runtime and SDK
flatpak install flathub org.freedesktop.Platform/x86_64/23.08
flatpak install flathub org.freedesktop.Sdk/x86_64/23.08

# Build the application
flatpak-builder --install-deps-from=flathub \
    --force-clean \
    --ccache \
    build-dir org.winpatable.Winpatable.yml

# Export as repository
flatpak build-export flatpak-repo build-dir

# Create single-file bundle
flatpak build-bundle flatpak-repo Winpatable.flatpak \
    org.winpatable.Winpatable
```

## Installation

### Install Built Flatpak Locally

```bash
flatpak install Winpatable.flatpak
```

### Run Winpatable

```bash
# Via Flatpak command
flatpak run org.winpatable.Winpatable

# Via application menu
# Look for "Winpatable" in your applications menu
```

## Distribution

### Option 1: Upload to Flathub (Recommended)

Flathub is the official app store for Flatpak applications:

1. **Fork the Flathub repository:**
   ```bash
   git clone https://github.com/flathub/flathub.git
   cd flathub
   ```

2. **Create new app directory:**
   ```bash
   mkdir -p new-apps/org.winpatable.Winpatable
   ```

3. **Add the manifest:**
   ```bash
   cp /path/to/org.winpatable.Winpatable.yml \
       new-apps/org.winpatable.Winpatable/org.winpatable.Winpatable.yml
   ```

4. **Create minimal appdata (org.winpatable.Winpatable.appdata.xml):**
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <component type="desktop-application">
     <id>org.winpatable.Winpatable</id>
     <name>Winpatable</name>
     <summary>Windows Compatibility Layer for Linux</summary>
     <description>
       <p>
         Winpatable is a comprehensive Windows compatibility layer that
         brings Windows applications to Linux with full GPU acceleration.
       </p>
       <p>Features:</p>
       <ul>
         <li>Support for 14+ professional Windows applications</li>
         <li>GPU acceleration (NVIDIA, AMD, Intel)</li>
         <li>Automatic driver detection and installation</li>
         <li>DXVK and VKD3D support for gaming</li>
         <li>Wine/Proton integration</li>
       </ul>
     </description>
     <url type="homepage">https://github.com/thomasboy2017/Winpatable-</url>
     <url type="bugtracker">https://github.com/thomasboy2017/Winpatable-/issues</url>
     <metadata_license>CC0-1.0</metadata_license>
     <project_license>MIT</project_license>
     <screenshots>
       <screenshot type="default">
         <image type="source">https://example.com/screenshot1.png</image>
       </screenshot>
     </screenshots>
     <releases>
       <release version="1.0.0" date="2024-11-28">
         <description>
           <p>Initial Flatpak release of Winpatable</p>
         </description>
       </release>
     </releases>
   </component>
   ```

5. **Commit and push:**
   ```bash
   git add new-apps/
   git commit -m "Add Winpatable to Flathub"
   git push -u origin main
   ```

6. **Create a Pull Request** on GitHub

7. **Flathub maintainers will review** and merge

### Option 2: Self-Hosted Distribution

If you prefer not to use Flathub, you can distribute the Flatpak bundle:

```bash
# Host the .flatpak file on your server
scp Winpatable.flatpak user@yourserver:/var/www/html/

# Users can install with:
flatpak install https://yourserver.com/Winpatable.flatpak
```

### Option 3: Create a Flatpak Repository

For organization/company distribution:

```bash
# Create a repository
mkdir flatpak-repo
flatpak build-export flatpak-repo build-dir

# Generate GPG signing key (optional but recommended)
gpg --generate-key

# Sign the repository
flatpak build-update-repo --generate-delta --gpg-sign=YOUR_GPG_KEY flatpak-repo

# Host on web server with .flatpakrepo file:
# https://docs.flatpak.org/en/latest/repos.html
```

## Testing the Flatpak

### Basic Functionality Test

```bash
# Test installation
flatpak install Winpatable.flatpak

# Test execution
flatpak run org.winpatable.Winpatable --help

# Test system integration
flatpak run org.winpatable.Winpatable --list-apps

# Test with verbose output
flatpak run --devel org.winpatable.Winpatable -v
```

### Permission Testing

```bash
# Check what permissions are requested
flatpak info org.winpatable.Winpatable

# View sandbox environment
flatpak run --devel org.winpatable.Winpatable env
```

### GPU Support Testing

```bash
# Test GPU detection
flatpak run org.winpatable.Winpatable --gpu-info

# Run with GPU debugging
flatpak run --devel org.winpatable.Winpatable --gpu-debug
```

## Manifest Reference

The `org.winpatable.Winpatable.yml` manifest contains:

- **app-id**: Unique application identifier
- **runtime**: Base runtime (freedesktop.org for broadest compatibility)
- **sdk**: Build tools SDK
- **command**: Entry point executable
- **finish-args**: Sandbox permissions
- **modules**: Build instructions for dependencies

### Key finish-args Explained

```yaml
--share=display       # Access to X11/Wayland
--socket=pulseaudio   # Audio output
--device=dri          # GPU device access
--filesystem=home     # Home directory access
--share=network       # Network access for downloads
```

## Troubleshooting

### Build Fails with "Runtime not found"

```bash
# Install the required runtime
flatpak install flathub org.freedesktop.Platform/x86_64/23.08
flatpak install flathub org.freedesktop.Sdk/x86_64/23.08
```

### GPU Not Detected in Flatpak

```bash
# GPU drivers must be installed on the host system
# The Flatpak accesses host GPU through /dev/dri

# Verify GPU access
flatpak run org.winpatable.Winpatable --gpu-info
```

### Permission Denied Errors

Check the sandbox permissions:
```bash
flatpak info --show-permissions org.winpatable.Winpatable
```

Add required permissions to `finish-args` in the manifest.

### Large Build Artifacts

Clean up previous builds:
```bash
rm -rf build-dir flatpak-repo
flatpak --uninstall org.winpatable.Winpatable  # Remove installed version
```

## Advanced Topics

### Building for Multiple Architectures

```bash
# Build for ARM64 (on ARM64 system)
flatpak-builder --arch=aarch64 build-dir-arm \
    org.winpatable.Winpatable.yml
```

### Delta Updates

For efficient updates, Flatpak can generate delta files:

```bash
flatpak build-update-repo --generate-delta flatpak-repo
```

### Custom Sandboxing

Modify `finish-args` in the manifest for custom permissions:

```yaml
finish-args:
  - --filesystem=/mnt/games:rw  # Read-write access to games directory
  - --device=all                # All device access
```

## Resources

- [Flathub Documentation](https://docs.flathub.org/)
- [Flatpak Manifests](https://docs.flatpak.org/en/latest/manifests.html)
- [Flatpak Build System](https://docs.flatpak.org/en/latest/building.html)
- [Flathub Submission Process](https://github.com/flathub/flathub/wiki/App-Requirements)

## Support

For issues with the Flatpak build:

1. Check [Winpatable Issues](https://github.com/thomasboy2017/Winpatable-/issues)
2. Review [Flatpak Documentation](https://docs.flatpak.org/)
3. Test on multiple distributions (Ubuntu, Mint, Fedora, etc.)

## License

Winpatable is licensed under the MIT License. See LICENSE file for details.
