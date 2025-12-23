# GPU Configuration Guide

## Supported GPU Models

### NVIDIA (Recommended for Professional Work)

#### Consumer Series
- **GeForce GTX 900 series**: GTX 950, 960, 970, 980, 980 Ti
- **GeForce GTX 10 series**: GTX 1050, 1060, 1070, 1080, 1080 Ti
- **GeForce RTX 20 series**: RTX 2060, 2070, 2080, 2080 Ti
- **GeForce RTX 30 series**: RTX 3060, 3070, 3080, 3090
- **GeForce RTX 40 series**: RTX 4060, 4070, 4080, 4090

#### Professional Series
- **NVIDIA RTX A series**: A2000, A4000, A5000, A6000
- **NVIDIA A100**: Data center GPU
- **NVIDIA H100**: Latest flagship

### AMD (Good Alternative)

#### RDNA 1 & 2 (Consumer)
- **RX 5700 XT**
- **RX 6700 XT**
- **RX 6800**
- **RX 6900 XT**

#### RDNA 3 (Latest)
- **RX 7600**
- **RX 7700 XT**
- **RX 7800 XT**
- **RX 7900 GRE**
- **RX 7900 XTX**

#### Professional (Radeon Pro)
- **Radeon Pro W5500**
- **Radeon Pro W6900X**

### Intel (Emerging Support)

#### Integrated Graphics
- **Intel UHD Graphics** (12th+ Gen)
- **Intel Iris Xe** (11th+ Gen)

#### Dedicated (Arc Series)
- **Arc A770**
- **Arc A750**
- **Arc A380**

## Driver Installation

### NVIDIA Installation

```bash
# Automatic installation
winpatable install-gpu-drivers

# Manual installation
sudo apt install nvidia-driver-550
sudo apt install cuda-toolkit-12-3
```

### AMD Installation

```bash
# Automatic installation
winpatable install-gpu-drivers

# Manual installation
sudo apt install amdgpu-install
amdgpu-install --usecase=workstation --opencl=rocm
```

### Intel Installation

```bash
# Automatic installation
winpatable install-gpu-drivers

# Manual installation
sudo apt install intel-gpu-tools
sudo apt install libva-intel-driver
```

## Verification

### Check NVIDIA Driver
```bash
nvidia-smi
```

### Check AMD Driver
```bash
rocm-smi
```

### Check OpenGL Support
```bash
glxinfo | grep "OpenGL version"
```

### Check Vulkan Support
```bash
vulkaninfo | grep "apiVersion"
```

## Performance Optimization

### NVIDIA CUDA
- Enable CUDA in application settings
- Update CUDA toolkit: `cuda-toolkit-12-3`
- Allocate GPU memory appropriately

### AMD ROCm
- Enable HIP/OpenCL in application settings
- Install ROCm libraries: `rocm-hip-sdk`
- Use GPU monitoring: `rocm-smi`

### Intel Arc
- Ensure latest Arc drivers
- Enable Arc GPU acceleration
- Monitor performance with `clpeak`

## Troubleshooting

### GPU Not Detected
```bash
# Check hardware
lspci | grep -i "vga\|3d"

# Check loaded modules
lsmod | grep -i nvidia  # or amdgpu, i915
```

### Low Performance
1. Update GPU drivers
2. Check GPU utilization: `nvidia-smi dmon`
3. Enable hardware acceleration in applications
4. Increase video memory allocation

### Driver Conflicts
```bash
# Remove old drivers
sudo apt remove nvidia-driver-*

# Clean installation
sudo apt autoremove
sudo apt autoclean
```
