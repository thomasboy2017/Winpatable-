#!/usr/bin/env python3
"""
System Information Detection Module
Detects CPU, GPU, OS, and system compatibility information
"""

import subprocess
import os
import re
from dataclasses import dataclass
from typing import Optional, List
from enum import Enum

class OSType(Enum):
    UBUNTU = "ubuntu"
    LINUX_MINT = "linux-mint"
    UNKNOWN = "unknown"

class CPUArch(Enum):
    X86_64 = "x86_64"
    UNKNOWN = "unknown"

class GPUType(Enum):
    NVIDIA = "nvidia"
    AMD = "amd"
    INTEL = "intel"
    UNKNOWN = "unknown"

@dataclass
class GPUInfo:
    type: GPUType
    name: str
    driver_version: Optional[str]
    is_supported: bool

@dataclass
class CPUInfo:
    arch: CPUArch
    vendor: str
    model: str
    cores: int
    is_supported: bool

@dataclass
class SystemInfo:
    os_type: OSType
    os_version: str
    cpu: CPUInfo
    gpus: List[GPUInfo]
    kernel_version: str
    memory_gb: float
    is_x64: bool

class SystemDetector:
    """Detects system hardware and software information"""
    
    @staticmethod
    def detect_os() -> tuple[OSType, str]:
        """Detect Linux distribution and version"""
        try:
            # Read and parse /etc/os-release into a dict of keys
            with open('/etc/os-release', 'r') as f:
                lines = [l.strip() for l in f.readlines() if l.strip() and '=' in l]

            data = {}
            for line in lines:
                k, v = line.split('=', 1)
                v = v.strip().strip('"')
                data[k.upper()] = v

            # Prefer ID and VERSION_ID fields for robust detection
            os_id = data.get('ID', '').lower()
            pretty_name = data.get('NAME', '').lower()
            version_str = data.get('VERSION_ID', 'Unknown')

            if 'ubuntu' in os_id or 'ubuntu' in pretty_name:
                return OSType.UBUNTU, version_str
            if 'linuxmint' in os_id or 'mint' in pretty_name or 'mint' in os_id:
                return OSType.LINUX_MINT, version_str
        except FileNotFoundError:
            pass
        
        return OSType.UNKNOWN, "Unknown"
    
    @staticmethod
    def detect_cpu() -> CPUInfo:
        """Detect CPU information"""
        try:
            with open('/proc/cpuinfo', 'r') as f:
                cpuinfo = f.read()
            
            # Determine architecture
            arch = CPUArch.X86_64 if os.uname().machine == 'x86_64' else CPUArch.UNKNOWN
            
            # Extract vendor
            vendor_match = re.search(r'vendor_id\s*:\s*(.+)', cpuinfo)
            vendor = vendor_match.group(1).strip() if vendor_match else "Unknown"
            
            # Extract model name
            model_match = re.search(r'model name\s*:\s*(.+)', cpuinfo)
            model = model_match.group(1).strip() if model_match else "Unknown"
            
            # Count cores
            cores = cpuinfo.count('processor')
            
            # Check if supported (x64 AMD or Intel)
            is_supported = arch == CPUArch.X86_64 and vendor in ['GenuineIntel', 'AuthenticAMD']
            
            return CPUInfo(
                arch=arch,
                vendor=vendor,
                model=model,
                cores=cores,
                is_supported=is_supported
            )
        except Exception as e:
            return CPUInfo(
                arch=CPUArch.UNKNOWN,
                vendor="Unknown",
                model="Unknown",
                cores=0,
                is_supported=False
            )
    
    @staticmethod
    def detect_gpus() -> List[GPUInfo]:
        """Detect GPU information and drivers"""
        gpus = []
        
        # Check NVIDIA GPUs
        nvidia_gpus = SystemDetector._detect_nvidia_gpus()
        gpus.extend(nvidia_gpus)
        
        # Check AMD GPUs
        amd_gpus = SystemDetector._detect_amd_gpus()
        gpus.extend(amd_gpus)
        
        # Check Intel GPUs
        intel_gpus = SystemDetector._detect_intel_gpus()
        gpus.extend(intel_gpus)
        
        return gpus if gpus else [GPUInfo(GPUType.UNKNOWN, "Unknown", None, False)]
    
    @staticmethod
    def _detect_nvidia_gpus() -> List[GPUInfo]:
        """Detect NVIDIA GPUs using nvidia-smi"""
        gpus = []
        try:
            output = subprocess.check_output(['nvidia-smi', '--query-gpu=name,driver_version', '--format=csv,noheader'], 
                                           timeout=5, text=True)
            lines = output.strip().split('\n')
            for line in lines:
                parts = line.split(',')
                if len(parts) >= 2:
                    name = parts[0].strip()
                    driver = parts[1].strip()
                    gpus.append(GPUInfo(
                        type=GPUType.NVIDIA,
                        name=name,
                        driver_version=driver,
                        is_supported=True
                    ))
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        return gpus
    
    @staticmethod
    def _detect_amd_gpus() -> List[GPUInfo]:
        """Detect AMD GPUs"""
        gpus = []
        try:
            # Check using lspci for AMD devices
            output = subprocess.check_output(['lspci'], timeout=5, text=True)
            for line in output.split('\n'):
                if 'AMD' in line and ('VGA' in line or 'Display' in line):
                    gpus.append(GPUInfo(
                        type=GPUType.AMD,
                        name=line.split(': ', 1)[1] if ': ' in line else "AMD GPU",
                        driver_version=None,
                        is_supported=True
                    ))
            
            # Try to get more details from AMDGPU driver
            if os.path.exists('/sys/module/amdgpu'):
                gpus_found = len(gpus)
                if gpus_found > 0:
                    for gpu in gpus:
                        if gpu.type == GPUType.AMD:
                            gpu.driver_version = "AMDGPU"
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        return gpus
    
    @staticmethod
    def _detect_intel_gpus() -> List[GPUInfo]:
        """Detect Intel GPUs (UHD, ARC)"""
        gpus = []
        try:
            output = subprocess.check_output(['lspci'], timeout=5, text=True)
            for line in output.split('\n'):
                if 'Intel' in line and ('VGA' in line or 'Display' in line or '3D' in line):
                    gpu_name = "Intel"
                    if 'UHD' in line:
                        gpu_name = "Intel UHD"
                    elif 'Iris' in line:
                        gpu_name = "Intel Iris"
                    elif 'Arc' in line or 'ARC' in line:
                        gpu_name = "Intel Arc"
                    
                    gpus.append(GPUInfo(
                        type=GPUType.INTEL,
                        name=gpu_name,
                        driver_version=None,
                        is_supported=True
                    ))
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        return gpus
    
    @staticmethod
    def detect_memory() -> float:
        """Detect total system memory in GB"""
        try:
            with open('/proc/meminfo', 'r') as f:
                for line in f:
                    if line.startswith('MemTotal:'):
                        kb = int(line.split()[1])
                        return kb / (1024 * 1024)
        except Exception:
            pass
        return 0.0
    
    @staticmethod
    def get_kernel_version() -> str:
        """Get kernel version"""
        try:
            return os.uname().release
        except Exception:
            return "Unknown"
    
    @classmethod
    def detect_all(cls) -> SystemInfo:
        """Detect all system information"""
        os_type, os_version = cls.detect_os()
        cpu = cls.detect_cpu()
        gpus = cls.detect_gpus()
        kernel_version = cls.get_kernel_version()
        memory_gb = cls.detect_memory()
        
        return SystemInfo(
            os_type=os_type,
            os_version=os_version,
            cpu=cpu,
            gpus=gpus,
            kernel_version=kernel_version,
            memory_gb=memory_gb,
            is_x64=cpu.arch == CPUArch.X86_64
        )

def print_system_info(info: SystemInfo):
    """Pretty print system information"""
    print("\n" + "="*60)
    print("SYSTEM INFORMATION")
    print("="*60)
    print(f"OS: {info.os_type.value.replace('_', ' ').title()} {info.os_version}")
    print(f"Kernel: {info.kernel_version}")
    print(f"Memory: {info.memory_gb:.2f} GB")
    print(f"\nCPU Information:")
    print(f"  Architecture: {info.cpu.arch.value}")
    print(f"  Vendor: {info.cpu.vendor}")
    print(f"  Model: {info.cpu.model}")
    print(f"  Cores: {info.cpu.cores}")
    print(f"  Supported: {'✓' if info.cpu.is_supported else '✗'}")
    print(f"\nGPU Information:")
    for i, gpu in enumerate(info.gpus, 1):
        print(f"  GPU {i}: {gpu.name} ({gpu.type.value.upper()})")
        if gpu.driver_version:
            print(f"    Driver: {gpu.driver_version}")
        print(f"    Supported: {'✓' if gpu.is_supported else '✗'}")
    print("="*60 + "\n")

if __name__ == "__main__":
    info = SystemDetector.detect_all()
    print_system_info(info)
