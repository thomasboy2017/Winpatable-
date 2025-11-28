# Winpatable Supported Applications

## Summary

Winpatable now supports **55+ professional Windows applications** across 20+ categories, making it the most comprehensive Windows compatibility layer for Linux Mint and Ubuntu. Features include AI-powered compatibility analysis and intelligent installation recommendations. (AI massively speeds up development, making it to where you don't have to have extensive coding experience to devleop software.)

## Supported Applications by Category

### Video & Audio Production (3 apps)
- **Adobe Premiere Pro** - Professional video editing with CUDA acceleration
- **Sony Vegas Pro** - Video editing and audio production
- **Adobe Audition** - Professional audio editing and mixing

### Professional Audio Software (5 apps)
- **Steinberg Cubase/Nuendo** - Industry-standard DAW with VST3 support
- **Ableton Live** - Music production and live performance
- **Pro Tools** - Professional audio DAW by Avid
- **Propellerheads Reason** - Music production and synthesis
- **Adobe Audition** - Professional audio editing

### Adobe Creative Suite (5 apps)
- **Adobe Photoshop** - Professional image editing and graphic design
- **Adobe Lightroom** - Photo management and editing
- **Adobe Illustrator** - Vector graphics and illustration
- **Adobe After Effects** - Motion graphics and VFX composition
- **Adobe InDesign** - Layout and publishing design

### 3D Modeling & CAD (8 apps)
- **Autodesk 3DS Max** - Professional 3D modeling and animation
- **Autodesk AutoCAD** - 2D/3D design and drafting
- **SolidWorks** - CAD/CAM 3D design software
- **Autodesk Fusion 360** - Cloud-based CAD/CAM platform
- **Autodesk Revit** - BIM and architectural design software
- **Autodesk Sketchbook** - Digital painting and drawing
- **ArcGIS** - GIS mapping and spatial analysis
- **PrusaSlicer & SuperSlicer** - 3D printer slicing software

### Graphics & Design (4 apps)
- **CorelDRAW** - Professional vector graphics and design
- **Corel Painter** - Professional digital painting and illustration
- **Paint.NET** - Simple yet powerful image editor
- **Figma** - Web-based UI/UX design tool

### Development Tools (3 apps)
- **Microsoft Visual Studio** - C#, C++, Python IDE
- **JetBrains IDEs** - PyCharm, IntelliJ IDEA, WebStorm, etc.
- **Notepad++** - Lightweight text editor with syntax highlighting

### Game Engines (2 apps)
- **Unity Engine** - 3D/2D game engine
- **Unreal Engine** - Professional game engine

### Gaming & Launchers (4 apps)
- **EA App** - EA Games launcher
- **Valorant** - Riot Games tactical shooter (limited - anti-cheat)
- **Rainbow Six Siege** - Ubisoft tactical shooter (limited - anti-cheat)
- **BattlEye** - Anti-cheat system (limited compatibility)

### Office & Productivity (8 apps)
- **Microsoft Office** - Word, Excel, PowerPoint
- **Microsoft Visio** - Diagramming and visualization
- **Microsoft SharePoint** - Collaboration platform
- **Microsoft Access** - Database application
- **Grammarly** - AI-powered writing assistant
- **Notion** - Note-taking and project management
- **WordPress** - Web content management system

### Cloud Storage & Sync (3 apps)
- **Dropbox** - Cloud storage and sync
- **Google Drive** - Cloud Drive sync
- **iTunes** - Apple media player and management

### Business & Finance (5 apps)
- **QuickBooks** - Accounting and bookkeeping
- **TurboTax** - Tax preparation software
- **Tableau** - Business intelligence and analytics
- **Power BI** - Microsoft analytics platform
- **Microsoft Teams** - Meetings, chat and collaboration

### Video & Multimedia (4 apps)
- **VirtualDub** - Video capture and editing
- **AviSynth** - Video scripting language
- **VobSub** - Subtitle manipulation and rendering

### Utilities & Monitoring (2 apps)
- **ShareX** - Screenshot and screen recording
- **HWMonitor** - Hardware monitoring utility

---

## Installation Commands

### Adobe Creative Suite
```bash
winpatable install-app photoshop --installer /path/to/Photoshop_2024.exe
winpatable install-app lightroom --installer /path/to/Lightroom_2024.exe
winpatable install-app illustrator --installer /path/to/Illustrator_2024.exe
winpatable install-app aftereffects --installer /path/to/AfterEffects_2024.exe
winpatable install-app teams --installer /path/to/TeamsSetup.exe
winpatable install-app copilot --installer /path/to/CopilotSetup.exe
```

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
winpatable install-app revit --installer /path/to/Revit_2024.exe
```

### 3D Modeling & Design
```bash
winpatable install-app 3dsmax --installer /path/to/3DSMax_2024.exe
winpatable install-app sketchbook --installer /path/to/Sketchbook_2024.exe
```

### Graphics & Design
```bash
winpatable install-app coreldraw --installer /path/to/CorelDRAW_2024.exe
winpatable install-app corelpainter --installer /path/to/CorelPainter_2024.exe
winpatable install-app access --installer /path/to/AccessSetup.exe
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
- **CPU**: Intel Core i3 (3rd Gen+) / AMD Ryzen 3 (x64)
- **RAM**: 4 GB
- **GPU**: Integrated graphics
- **Storage**: 20 GB SSD

### Recommended Configuration (Photo/Graphics/Light CAD)
- **CPU**: Intel Core i5 (5th Gen+) / AMD Ryzen 5
- **RAM**: 8-16 GB
- **GPU**: Integrated or dedicated graphics
- **Storage**: 40+ GB SSD

### High-Performance Configuration (Video/3D/Professional CAD)
- **CPU**: Intel Core i7+ (6th Gen+) / AMD Ryzen 7+
- **RAM**: 16-32 GB
- **GPU**: NVIDIA GTX 1070+ / AMD Radeon RX 5700+
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

