# Quick Start: Linux Mint & Flatpak

## For Linux Mint Users

### Install Winpatable on Linux Mint

```bash
# Option 1: From built Flatpak (fastest)
./flatpak-build.sh
flatpak install Winpatable.flatpak
flatpak run org.winpatable.Winpatable

# Option 2: Traditional installation
bash install.sh

# Option 3: From Flathub (when available)
flatpak install flathub org.winpatable.Winpatable
```

### First Run
```bash
# Run installation wizard
flatpak run org.winpatable.Winpatable --wizard

# Or traditional script
python3 scripts/launcher.py
```

---

## For Package Maintainers

### Build Flatpak

```bash
# Prerequisites
sudo apt install flatpak flatpak-builder
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo

# Build
chmod +x flatpak-build.sh
./flatpak-build.sh

# Result: Winpatable.flatpak
```

### Distribute via Flathub

```bash
# 1. Fork: https://github.com/flathub/flathub
# 2. Add: new-apps/org.winpatable.Winpatable/org.winpatable.Winpatable.yml
# 3. Create appdata.xml (see FLATPAK_GUIDE.md)
# 4. Submit PR
# 5. Flathub maintainers review and merge
# 6. Users install: flatpak install flathub org.winpatable.Winpatable
```

---

## Key Files

| File | Purpose |
|------|---------|
| `src/core/distro_utils.py` | Cross-distro compatibility utilities |
| `src/core/system_info.py` | Robust OS detection (updated) |
| `src/gpu/gpu_manager.py` | GPU driver management (updated) |
| `src/wine/wine_manager.py` | Wine/Proton setup (updated) |
| `org.winpatable.Winpatable.yml` | Flatpak manifest |
| `flatpak-build.sh` | Automated build script |
| `FLATPAK_GUIDE.md` | Complete Flatpak documentation |
| `LINUX_MINT_FLATPAK_SUMMARY.md` | This summary document |

---

## Linux Mint Compatibility

✅ All distributions supported:
- Ubuntu 20.04, 22.04, 24.04
- Linux Mint 20, 21, 22
- Debian 11, 12
- Other Debian-based distros

✅ Package managers:
- `apt` (preferred)
- `apt-get` (fallback)

✅ GPUs supported:
- NVIDIA (CUDA, DXVK, VKD3D)
- AMD (AMDGPU, ROCm)
- Intel (UHD, Arc)

---

## Troubleshooting

### Wine not detected
```bash
sudo apt install wine wine32 wine64 winetricks
```

### GPU drivers missing
```bash
# NVIDIA
sudo apt install nvidia-driver-545

# AMD
sudo apt install amdgpu-dkms

# Intel
sudo apt install intel-gpu-tools mesa-opencl-icd
```

### Flatpak runtime missing
```bash
flatpak install flathub org.freedesktop.Platform/x86_64/23.08
flatpak install flathub org.freedesktop.Sdk/x86_64/23.08
```

### Permission denied
```bash
# Check sandbox permissions
flatpak info org.winpatable.Winpatable

# Run with verbose output
flatpak run --devel org.winpatable.Winpatable -v
```

---

## Resources

- **GitHub:** https://github.com/thomasboy2017/Winpatable-
- **Flatpak Docs:** https://docs.flatpak.org/
- **Flathub:** https://flathub.org/
- **Linux Mint:** https://linuxmint.com/

---

**Last Updated:** November 28, 2024  
**Status:** Production Ready ✅
