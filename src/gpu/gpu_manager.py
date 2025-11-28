#!/usr/bin/env python3
"""
GPU Driver Installation Module
Handles GPU driver setup for NVIDIA, AMD, and Intel GPUs
"""

import subprocess
import sys
import os
from typing import List, Tuple
from src.core.system_info import SystemDetector, GPUType
from src.core.distro_utils import DistroUtils

class GPUDriverManager:
    """Manages GPU driver installation and configuration"""
    
    def __init__(self, use_sudo: bool = True):
        self.use_sudo = use_sudo
        self.package_manager, _ = DistroUtils.get_package_manager()
    
    def run_command(self, cmd: List[str], check: bool = True) -> Tuple[int, str, str]:
        """Run command with optional sudo"""
        full_cmd = cmd
        if self.use_sudo and cmd[0] != 'sudo':
            full_cmd = ['sudo'] + cmd
        
        try:
            result = subprocess.run(full_cmd, capture_output=True, text=True, check=check)
            return result.returncode, result.stdout, result.stderr
        except subprocess.CalledProcessError as e:
            return e.returncode, e.stdout, e.stderr
    
    def install_nvidia_drivers(self) -> bool:
        """Install NVIDIA drivers and CUDA support"""
        print("\n[GPU] Installing NVIDIA drivers...")
        try:
            # Update package manager
            self.run_command([self.package_manager, 'update'])
            
            # Install NVIDIA drivers
            driver_packages = [
                'nvidia-driver-550',
                'nvidia-dkms-550',
                'libnvidia-gl-550',
                'libnvidia-decode-550',
                'libnvidia-encode-550'
            ]
            
            for package in driver_packages:
                self.run_command([self.package_manager, 'install', '-y', package])
            
            # Install CUDA toolkit
            print("[GPU] Installing CUDA toolkit...")
            cuda_packages = [
                'cuda-toolkit-12-3',
                'libcuda1',
                'nvidia-utils'
            ]
            for package in cuda_packages:
                self.run_command([self.package_manager, 'install', '-y', package], check=False)
            
            # Install cuDNN for deep learning support
            print("[GPU] Installing cuDNN...")
            self.run_command([self.package_manager, 'install', '-y', 'libcudnn8'], check=False)
            
            print("✓ NVIDIA drivers installed successfully")
            return True
        except Exception as e:
            print(f"✗ NVIDIA driver installation failed: {e}")
            return False
    
    def install_amd_drivers(self) -> bool:
        """Install AMD drivers (AMDGPU and ROCm)"""
        print("\n[GPU] Installing AMD drivers...")
        try:
            # Update package manager
            self.run_command([self.package_manager, 'update'])
            
            # Install AMDGPU driver
            amd_packages = [
                'amdgpu-install',
                'amdgpu-core',
                'libdrm-amdgpu',
                'mesa-amdgpu'
            ]
            
            for package in amd_packages:
                self.run_command([self.package_manager, 'install', '-y', package], check=False)
            
            # Install ROCm (open-source compute platform)
            print("[GPU] Installing ROCm...")
            rocm_packages = [
                'rocm-hip-sdk',
                'rocm-opencl-sdk'
            ]
            for package in rocm_packages:
                self.run_command([self.package_manager, 'install', '-y', package], check=False)
            
            print("✓ AMD drivers installed successfully")
            return True
        except Exception as e:
            print(f"✗ AMD driver installation failed: {e}")
            return False
    
    def install_intel_drivers(self) -> bool:
        """Install Intel GPU drivers (UHD, ARC)"""
        print("\n[GPU] Installing Intel GPU drivers...")
        try:
            # Update package manager
            self.run_command([self.package_manager, 'update'])
            
            # Install Intel GPU drivers
            intel_packages = [
                'intel-gpu-tools',
                'libva-intel-driver',
                'i965-va-driver',
                'va-driver-all',
                'libva-glx2'
            ]
            
            for package in intel_packages:
                self.run_command([self.package_manager, 'install', '-y', package], check=False)
            
            # Install Intel Arc drivers (if available)
            print("[GPU] Installing Intel Arc drivers...")
            self.run_command([self.package_manager, 'install', '-y', 'intel-arc-gpu-plugin'], check=False)
            
            # Install Intel OneAPI toolkit
            print("[GPU] Installing Intel OneAPI toolkit...")
            self.run_command([self.package_manager, 'install', '-y', 'intel-oneapi-runtime-dpcpp-cpp'], check=False)
            
            print("✓ Intel GPU drivers installed successfully")
            return True
        except Exception as e:
            print(f"✗ Intel driver installation failed: {e}")
            return False
    
    def install_vulkan_support(self) -> bool:
        """Install Vulkan support for all GPUs"""
        print("\n[GPU] Installing Vulkan support...")
        try:
            vulkan_packages = [
                'vulkan-tools',
                'vulkan-loader',
                'libvulkan1',
                'libvulkan-dev',
                'vulkan-validation-layers'
            ]
            
            for package in vulkan_packages:
                self.run_command([self.package_manager, 'install', '-y', package], check=False)
            
            print("✓ Vulkan support installed successfully")
            return True
        except Exception as e:
            print(f"✗ Vulkan installation failed: {e}")
            return False
    
    def install_opengl_support(self) -> bool:
        """Install OpenGL support"""
        print("\n[GPU] Installing OpenGL support...")
        try:
            opengl_packages = [
                'libgl1-mesa-dri',
                'libgl1-mesa-glx',
                'libglx0',
                'libglu1-mesa',
                'mesa-utils'
            ]
            
            for package in opengl_packages:
                self.run_command([self.package_manager, 'install', '-y', package], check=False)
            
            print("✓ OpenGL support installed successfully")
            return True
        except Exception as e:
            print(f"✗ OpenGL installation failed: {e}")
            return False
    
    def install_all_gpu_drivers(self, gpu_types: List[GPUType]) -> bool:
        """Install drivers for all detected GPUs"""
        print("\n" + "="*60)
        print("GPU DRIVER INSTALLATION")
        print("="*60)
        
        success = True
        
        for gpu_type in set(gpu_types):
            if gpu_type == GPUType.NVIDIA:
                success = self.install_nvidia_drivers() and success
            elif gpu_type == GPUType.AMD:
                success = self.install_amd_drivers() and success
            elif gpu_type == GPUType.INTEL:
                success = self.install_intel_drivers() and success
        
        # Install universal support
        success = self.install_vulkan_support() and success
        success = self.install_opengl_support() and success
        
        print("\n" + "="*60)
        print(f"GPU driver installation {'COMPLETED' if success else 'FAILED'}")
        print("="*60 + "\n")
        
        return success
    
    def verify_drivers(self) -> dict:
        """Verify installed drivers"""
        verification = {}
        
        # Check NVIDIA
        try:
            subprocess.run(['nvidia-smi'], capture_output=True, check=True)
            verification['nvidia'] = 'installed'
        except (subprocess.CalledProcessError, FileNotFoundError):
            verification['nvidia'] = 'not_installed'
        
        # Check Vulkan
        try:
            subprocess.run(['vulkaninfo'], capture_output=True, check=True)
            verification['vulkan'] = 'installed'
        except (subprocess.CalledProcessError, FileNotFoundError):
            verification['vulkan'] = 'not_installed'
        
        # Check OpenGL
        try:
            subprocess.run(['glxinfo'], capture_output=True, check=True)
            verification['opengl'] = 'installed'
        except (subprocess.CalledProcessError, FileNotFoundError):
            verification['opengl'] = 'not_installed'
        
        return verification

if __name__ == "__main__":
    detector = SystemDetector()
    system_info = detector.detect_all()
    
    gpu_types = [gpu.type for gpu in system_info.gpus]
    
    manager = GPUDriverManager(use_sudo=True)
    manager.install_all_gpu_drivers(gpu_types)
    
    print("Driver Verification:")
    verification = manager.verify_drivers()
    for driver, status in verification.items():
        symbol = "✓" if status == "installed" else "✗"
        print(f"  {driver}: {symbol} {status}")
