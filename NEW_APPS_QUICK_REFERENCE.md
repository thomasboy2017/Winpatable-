# Quick Reference: New Applications

## All 14 Supported Applications

### Audio Production (3 apps)
| App | RAM | GPU | Cmd |
|-----|-----|-----|-----|
| Adobe Audition | 8GB | Optional | `audition` |
| Cubase | 16GB | Optional | `cubase` |
| Ableton Live | 8GB | Optional | `ableton` |

### 3D/CAD (5 apps)
| App | RAM | GPU | Cmd |
|-----|-----|-----|-----|
| 3DS Max | 16GB | Required | `3dsmax` |
| AutoCAD | 16GB | Required | `autocad` |
| SolidWorks | 16GB | Required | `solidworks` |
| Fusion 360 | 8GB | Required | `fusion360` |
| *Originally in core* | | | |

### Programming/Games (4 apps)
| App | RAM | GPU | Cmd |
|-----|-----|-----|-----|
| Visual Studio | 8GB | Optional | `visualstudio` |
| JetBrains IDEs | 4GB | Optional | `jetbrains` |
| Unity | 8GB | Required | `unity` |
| Unreal | 16GB | Required | `unreal` |

### Video Production (1 app)
| App | RAM | GPU | Cmd |
|-----|-----|-----|-----|
| Premiere Pro | 16GB | Required | `premiere` |

### Office (1 app)
| App | RAM | GPU | Cmd |
|-----|-----|-----|-----|
| Office | 4GB | Optional | `office` |

---

## Installation Template

```bash
# 1. Detect system
winpatable detect

# 2. Install drivers (if needed)
winpatable install-gpu-drivers

# 3. Setup Wine
winpatable setup-wine

# 4. Install app
winpatable install-app <cmd> --installer /path/to/setup.exe

# 5. Optimize
winpatable performance-tuning
```

---

## New Apps Summary

**Added in Latest Update:**
- ✅ Adobe Audition (audio editing)
- ✅ Steinberg Cubase (professional DAW)
- ✅ Ableton Live (music production)
- ✅ Autodesk AutoCAD (CAD design)
- ✅ SolidWorks (3D CAD)
- ✅ Autodesk Fusion 360 (cloud CAD)
- ✅ Microsoft Visual Studio (IDE)
- ✅ JetBrains IDEs (multi-language IDE)
- ✅ Unity Engine (game engine)
- ✅ Unreal Engine (game engine)

**Total: 14 applications across 5 categories**

---

## DLL Support Matrix

All applications include:
- .NET Framework 4.8, 4.6.2
- DirectX 9/10/11/12
- Visual C++ 2019, 2022
- Audio: ALSA, PulseAudio, JACK
- GPU: NVIDIA, AMD, Intel support

---

## Performance Tips

```bash
# Enable ESYNC/FSYNC (low-latency)
winpatable performance-tuning

# Check GPU status
nvidia-smi

# Monitor app performance
top -p $(pgrep -f "wine|proton")

# Profile frame rates
DXVK_HUD=fps wine app.exe
```

---

## Hardware Recommendations

### Budget Build (4-8GB RAM)
- Office, PyCharm, Audition, Ableton

### Mid-Range (8-16GB RAM)
- Audition, Ableton, Fusion 360, Visual Studio, Unity

### High-Performance (16-32GB RAM)
- Premiere Pro, 3DS Max, AutoCAD, SolidWorks, Cubase, Unreal

### Workstation (32GB+ RAM)
- Multiple professional apps simultaneously
- GPU acceleration for all 3D/video apps
- Cloud sync for Fusion 360

---

## Getting Help

```bash
# Quick start with wizard
python scripts/wizard.py

# Check app requirements
winpatable list-apps

# See detailed guides
less docs/APPLICATION_GUIDES.md

# GPU-specific help
less docs/GPU_GUIDE.md

# Troubleshoot issues
less docs/TROUBLESHOOTING.md
```

---

## What Changed

### Code
- `src/installers/app_installers.py`: +10 installers
- `config/config.json`: +10 app configs
- Total new code: ~400 lines

### Documentation
- `SUPPORTED_APPLICATIONS.md`: Complete reference
- `EXPANSION_SUMMARY.md`: Technical details
- `NEW_APPS_QUICK_REFERENCE.md`: This file

### CLI
All 14 apps now accessible via `winpatable install-app <cmd>`

---

## Compatibility

✓ Ubuntu 20.04, 22.04, 24.04  
✓ Linux Mint 20, 21  
✓ x86_64 Intel/AMD CPU  
✓ NVIDIA/AMD/Intel GPU  
✓ Vulkan 1.3+, OpenGL 4.6+  

---

## Licenses

Winpatable: MIT License  
Supported applications retain original licenses

---

## Contributing

To add more applications:

1. Create `NewAppInstaller` class
2. Add to `ApplicationManager.APPLICATIONS`
3. Add config to `config.json`
4. Document in `APPLICATION_GUIDES.md`
5. Test with system

See `ARCHITECTURE.md` for implementation details.
