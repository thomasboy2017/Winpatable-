# Winpatable Architecture Documentation

## System Overview

Winpatable is a modular Windows compatibility layer that bridges Windows applications with Linux systems through a multi-layered approach:

```
Windows Applications
        ↓
    Wine/Proton
        ↓
  Translation Layers
   (DXVK, VKD3D)
        ↓
  GPU Drivers
   (CUDA, ROCm)
        ↓
  Linux Kernel
        ↓
   Hardware
```

## Component Architecture

### 1. Core Module (`src/core/`)

**System Detection** (`system_info.py`)
- Hardware detection (CPU, GPU, memory)
- OS identification and version
- Compatibility assessment
- System reporting

**Classes**:
- `SystemDetector`: Main detection engine
- `CPUInfo`: CPU specifications
- `GPUInfo`: GPU details
- `SystemInfo`: Complete system profile

### 2. GPU Module (`src/gpu/`)

**GPU Driver Management** (`gpu_manager.py`)
- NVIDIA driver installation (CUDA, cuDNN)
- AMD driver installation (AMDGPU, ROCm)
- Intel driver installation (UHD, Arc)
- Vulkan and OpenGL setup
- Driver verification

**Classes**:
- `GPUDriverManager`: Driver installation orchestrator
- Methods for each GPU vendor

### 3. Wine Module (`src/wine/`)

**Wine/Proton Configuration** (`wine_manager.py`)
- Wine prefix creation and management
- Proton installation
- DXVK and VKD3D setup
- Registry configuration
- Environment variable management

**Classes**:
- `WineManager`: Wine environment orchestrator
- `WineConfig`: Configuration dataclass

### 4. Installers Module (`src/installers/`)

**Application Installation** (`app_installers.py`)
- Application-specific configuration
- DLL installation via winetricks
- Registry tweaks
- Dependency management

**Classes**:
- `ApplicationInstaller`: Base installer class
- `AdobePremiereInstaller`: Premiere Pro setup
- `SonyVegasInstaller`: Vegas Pro setup
- `Autodesk3DSMaxInstaller`: 3DS Max setup
- `MicrosoftOfficeInstaller`: Office setup
- `ApplicationManager`: Installer orchestrator

### 5. CLI Interface (`src/winpatable.py`)

**Main Command-Line Interface**
- User interaction layer
- Command routing
- System diagnostics
- Installation workflows

**Commands**:
- `detect`: System detection
- `install-gpu-drivers`: GPU setup
- `setup-wine`: Wine configuration
- `install-app`: Application installation
- `quick-start`: Full setup
- `performance-tuning`: Optimization guide

## Data Flow

### Installation Workflow

```
User executes: winpatable quick-start
        ↓
    System Detection
        ↓
    Compatibility Check
        ↓
    GPU Driver Installation
        ↓
    Wine/Proton Setup
        ↓
    Configuration
        ↓
    Ready for Applications
```

### Application Launch

```
User launches application
        ↓
Set Wine environment variables
        ↓
Install required DLLs (if needed)
        ↓
Apply registry tweaks
        ↓
Launch with Wine/Proton
        ↓
Application runs with GPU acceleration
```

## Configuration Management

### Config File Structure

```json
{
  "settings": {
    "wine_prefix": "~/.winpatable",
    "enable_dxvk": true,
    "enable_vkd3d": true
  },
  "applications": {
    "app_name": {
      "required_dlls": ["dll1", "dll2"],
      "registry_tweaks": {...},
      "environment_variables": {...}
    }
  }
}
```

### Wine Prefix Structure

```
~/.winpatable/
├── drive_c/                 # Windows C: drive
│   ├── windows/
│   ├── Program Files/
│   └── Users/
├── proton/                  # Proton installation
├── dxvk/                    # DXVK files
├── applications/            # App configs
├── gpu/                     # GPU settings
├── wine/                    # Wine files
└── config.json             # Configuration
```

## GPU Implementation

### NVIDIA Stack
```
Application
    ↓
DXVK (Direct3D→Vulkan)
    ↓
NVIDIA Vulkan Driver
    ↓
CUDA/NVIDIA Driver
    ↓
GPU Hardware
```

### AMD Stack
```
Application
    ↓
DXVK (Direct3D→Vulkan)
    ↓
AMD Vulkan Driver / ROCm
    ↓
AMDGPU Driver
    ↓
GPU Hardware
```

### Intel Stack
```
Application
    ↓
DXVK or VKD3D
    ↓
Intel Vulkan/OpenGL Driver
    ↓
i915 or xe Driver
    ↓
GPU Hardware
```

## Environment Variables

### Critical Variables

| Variable | Purpose | Value |
|----------|---------|-------|
| `WINEPREFIX` | Wine directory | `~/.winpatable` |
| `WINEARCH` | Architecture | `win64` |
| `DXVK_HUD` | DXVK info display | `off` |
| `STAGING_SHARED_MEMORY` | Shared memory | `1` |
| `vblank_mode` | VSync control | `0` |

## Registry Tweaks

Application-specific registry modifications for optimization:

```
HKEY_CURRENT_USER\Software\Wine\Direct3D
  - CSMT: Enabled
  - Renderer: opengl
  - VideoMemorySize: 4096

HKEY_CURRENT_USER\Software\Wine\Explorer
  - Desktop: [Monitor resolution]
```

## Error Handling

### Graceful Degradation
1. GPU drivers: Falls back to software rendering
2. DXVK: Falls back to Wine OpenGL
3. VKD3D: Falls back to D3D11 implementation

### Logging
- System detection: Detailed hardware logs
- Driver installation: Installation progress
- Application launch: Runtime diagnostics

## Performance Optimization

### Shader Caching
- DXVK shader cache: `~/.cache/dxvk`
- Pre-compilation for faster launch
- Configurable cache size

### GPU Memory
- Automatic detection of VRAM
- Optimal allocation based on application
- Memory pooling for multiple applications

### Threading
- Multi-threaded compilation
- Async loading where possible
- Priority-based task scheduling

## Security Considerations

1. **Sandboxing**: Applications isolated in Wine prefix
2. **Registry isolation**: Per-application settings
3. **DLL isolation**: Managed via winetricks
4. **File access**: Restricted to Wine prefix by default

## Extensibility

### Adding New Applications

1. Extend `ApplicationInstaller` class
2. Define `ApplicationConfig`
3. Implement `install()` method
4. Register in `ApplicationManager.APPLICATIONS`

### Custom GPU Support

1. Extend `GPUDriverManager`
2. Implement vendor-specific methods
3. Add package definitions
4. Register in detection logic

## Testing Strategy

### Unit Tests
- System detection
- Configuration management
- DLL installation
- Registry modifications

### Integration Tests
- Full installation workflow
- Application launching
- GPU acceleration verification

### Performance Tests
- Shader compilation time
- Application startup time
- GPU utilization

## Dependencies

### System Level
- Wine/Proton
- GPU drivers (vendor-specific)
- Vulkan/OpenGL libraries
- Development headers

### Python Level
- requests (for downloads)
- setuptools (for packaging)
- subprocess (for system calls)

## Future Enhancements

1. **GUI Interface**: Qt/GTK frontend
2. **Cloud Gaming**: Remote execution support
3. **Containerization**: Docker/Podman support
4. **More Applications**: Extended compatibility
5. **AI Optimization**: Automatic performance tuning
6. **Gaming Support**: Game-specific optimizations

---

This architecture provides a solid foundation for Windows application compatibility while maintaining modularity and extensibility.
