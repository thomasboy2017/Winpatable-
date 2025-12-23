# Winpatable Supported Applications

## Summary

Winpatable now supports **14 professional Windows applications** across multiple categories, making it the most comprehensive Windows compatibility layer for Linux Mint and Ubuntu.

## Supported Applications by Category

### Video & Audio Production (3 apps)
- **Adobe Premiere Pro** - Professional video editing with CUDA acceleration
- **Sony Vegas Pro** - Video editing and audio production
- **Adobe Audition** - Professional audio editing and mixing

### Professional Audio Software (2 apps)
- **Steinberg Cubase** - Industry-standard DAW with VST3 support
- **Ableton Live** - Music production and live performance

### 3D Modeling & CAD (5 apps)
- **Autodesk 3DS Max** - Professional 3D modeling and animation
- **Autodesk AutoCAD** - 2D/3D design and drafting
- **SolidWorks** - CAD/CAM 3D design software
- **Autodesk Fusion 360** - Cloud-based CAD/CAM platform

### Programming Tools & Game Engines (4 apps)
- **Microsoft Visual Studio** - C#, C++, Python IDE
- **JetBrains IDEs** - PyCharm, IntelliJ IDEA, WebStorm, etc.
- **Unity Engine** - 3D/2D game engine
- **Unreal Engine** - Professional game engine

### Office & Productivity (1 app)
- **Microsoft Office** - Word, Excel, PowerPoint

---

## Installation Commands

### Audio Software
```bash
winpatable install-app audition --installer /path/to/Audition_2024.exe
winpatable install-app cubase --installer /path/to/Cubase_12.exe
winpatable install-app ableton --installer /path/to/AbeletonLive_12.exe
```

### CAD Software
```bash
winpatable install-app autocad --installer /path/to/AutoCAD_2024.exe
winpatable install-app solidworks --installer /path/to/SolidWorks_2024.exe
winpatable install-app fusion360 --installer /path/to/Fusion360Setup.exe
```

### Programming & Game Engines
```bash
winpatable install-app visualstudio --installer /path/to/vs_setup.exe
winpatable install-app jetbrains --installer /path/to/pycharm-setup.exe
winpatable install-app unity --installer /path/to/UnitySetup-2023.2.exe
winpatable install-app unreal --installer /path/to/UnrealEngineSetup.exe
```

---

## Hardware Requirements

### Minimum Configuration (Most Applications)
- **CPU**: Intel Core i5 / AMD Ryzen 5 (x64)
- **RAM**: 8 GB
- **GPU**: Integrated graphics
- **Storage**: 30 GB SSD

### Recommended Configuration (Video/3D/CAD)
- **CPU**: Intel Core i7/Xeon / AMD Ryzen 7
- **RAM**: 16-32 GB
- **GPU**: NVIDIA RTX 2070+ / AMD Radeon RX / Intel Arc
- **Storage**: 60+ GB SSD

### High-End Configuration (Unreal Engine, SolidWorks)
- **CPU**: Intel Core i7/Xeon / AMD Ryzen 7 (6+ cores)
- **RAM**: 32 GB
- **GPU**: NVIDIA Quadro/RTX or AMD Radeon Pro (6GB+ VRAM)
- **Storage**: 100+ GB SSD

---

## GPU Acceleration Support

### NVIDIA GPUs
- All applications with 3D acceleration
- CUDA acceleration for Adobe Premiere Pro
- RTX hardware acceleration

### AMD GPUs
- AMDGPU driver support
- ROCm HIP SDK for compute tasks
- RDNA architecture optimization

### Intel GPUs
- UHD Graphics support
- Intel Arc integration
- OneAPI toolkit compatibility

---

## DLL & Runtime Support

All applications automatically receive:
- **.NET Framework**: 4.8, 4.6.2 support
- **DirectX**: D3D9, D3D10, D3D11, D3D12
- **Visual C++ Runtimes**: 2019, 2022
- **Audio Stack**: ALSA, PulseAudio, JACK support

---

## System Detection & Compatibility

Before installing any application, run:
```bash
winpatable detect
```

This will verify:
- ✓ CPU architecture (x64 support)
- ✓ Total system RAM
- ✓ GPU vendor and VRAM
- ✓ OS compatibility
- ✓ Required dependencies

---

## Performance Tuning

### Enable Maximum Performance
```bash
winpatable performance-tuning
```

This optimizes:
- ESYNC/FSYNC for low-latency
- GPU acceleration
- Wine cache settings
- DirectX performance

---

## Troubleshooting

### Common Issues & Solutions

**GPU not detected:**
```bash
winpatable install-gpu-drivers
winpatable setup-wine
```

**Missing audio:**
```bash
sudo apt install pulseaudio alsa-utils jackd
```

**Slow performance:**
```bash
# Check GPU memory
nvidia-smi

# Monitor application CPU/RAM
top -p $(pgrep -f "wine|proton")
```

---

## Getting Help

- **Documentation**: See `docs/APPLICATION_GUIDES.md` for detailed setup
- **System Requirements**: See `GPU_GUIDE.md` for GPU-specific config
- **Troubleshooting**: See `TROUBLESHOOTING.md` for common issues
- **Architecture**: See `ARCHITECTURE.md` for technical details

---

## What's Next

To install an application:

1. Run system detection: `winpatable detect`
2. Install GPU drivers: `winpatable install-gpu-drivers`
3. Setup Wine environment: `winpatable setup-wine`
4. Install application: `winpatable install-app <name> --installer /path/to/setup.exe`

For step-by-step guidance:
```bash
python scripts/wizard.py
```

---

## Feature Matrix

| App | OS | GPU | Audio | Multi-core | Network |
|-----|----|----|-------|-----------|---------|
| Premiere Pro | ✓ | ✓ | ✓ | ✓ | ✓ |
| Vegas Pro | ✓ | ✓ | ✓ | ✓ | ✓ |
| Audition | ✓ | ✓ | ✓ | ✓ | ✓ |
| 3DS Max | ✓ | ✓ | ✓ | ✓ | ✓ |
| AutoCAD | ✓ | ✓ | - | ✓ | ✓ |
| SolidWorks | ✓ | ✓ | - | ✓ | ✓ |
| Cubase | ✓ | - | ✓ | ✓ | ✓ |
| Ableton | ✓ | - | ✓ | ✓ | ✓ |
| Fusion 360 | ✓ | ✓ | - | ✓ | ✓ |
| Visual Studio | ✓ | - | - | ✓ | ✓ |
| JetBrains | ✓ | - | - | ✓ | ✓ |
| Office | ✓ | - | - | ✓ | ✓ |
| Unity | ✓ | ✓ | - | ✓ | ✓ |
| Unreal | ✓ | ✓ | - | ✓ | ✓ |

