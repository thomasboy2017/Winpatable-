#!/usr/bin/env python3
"""
Application-Specific Installers
Handles installation and configuration of professional applications:
- Adobe Premiere Pro
- Sony Vegas Pro
- Autodesk 3DS Max
- Microsoft Office
"""

import os
import json
from pathlib import Path
from typing import Optional, Dict
from dataclasses import dataclass
import subprocess
from src.core.distro_utils import DistroUtils

@dataclass
class ApplicationConfig:
    name: str
    windows_executable: str
    required_dlls: list
    registry_tweaks: dict
    environment_variables: dict
    required_dependencies: list
    minimum_ram_gb: int
    gpu_required: bool
    notes: str

class ApplicationInstaller:
    """Base class for application installation"""
    
    def __init__(self, wine_prefix: str):
        self.wine_prefix = wine_prefix
        self.prefix_path = Path(wine_prefix)
        self.applications_dir = self.prefix_path / "applications"
        self.applications_dir.mkdir(parents=True, exist_ok=True)
    
    def run_with_wine(self, executable: str, args: list = None) -> bool:
        """Run executable with Wine"""
        try:
            env = os.environ.copy()
            env['WINEPREFIX'] = self.wine_prefix
            
            cmd = ['wine', executable]
            if args:
                cmd.extend(args)
            
            subprocess.run(cmd, env=env, check=False)
            return True
        except Exception as e:
            print(f"✗ Failed to run application: {e}")
            return False
    
    def install_required_dlls(self, dlls: list) -> bool:
        """Install required DLLs using winetricks"""
        print(f"[App] Installing required DLLs: {', '.join(dlls)}")
        try:
            env = os.environ.copy()
            env['WINEPREFIX'] = self.wine_prefix
            
            for dll in dlls:
                subprocess.run(['winetricks', dll], env=env, 
                             capture_output=True, check=False)
            
            return True
        except Exception as e:
            print(f"✗ DLL installation failed: {e}")
            return False
    
    def configure_registry(self, tweaks: dict) -> bool:
        """Apply registry tweaks for optimization"""
        print("[App] Applying registry tweaks...")
        try:
            # Create registry file
            reg_file = self.prefix_path / "tweaks.reg"
            
            with open(reg_file, 'w') as f:
                f.write("REGEDIT4\n\n")
                for path, values in tweaks.items():
                    f.write(f"[{path}]\n")
                    for key, value in values.items():
                        if isinstance(value, str):
                            f.write(f'"{key}"="{value}"\n')
                        elif isinstance(value, int):
                            f.write(f'"{key}"=dword:{value:08x}\n')
            
            # Apply registry
            env = os.environ.copy()
            env['WINEPREFIX'] = self.wine_prefix
            
            subprocess.run(['regedit', str(reg_file)], env=env, 
                         capture_output=True, check=False)
            
            return True
        except Exception as e:
            print(f"✗ Registry configuration failed: {e}")
            return False

class AdobePremiereInstaller(ApplicationInstaller):
    """Adobe Premiere Pro installer and configurator"""
    
    CONFIG = ApplicationConfig(
        name="Adobe Premiere Pro",
        windows_executable="Adobe Premiere Pro.exe",
        required_dlls=['dotnet48', 'd3dx9', 'd3dx10', 'd3dx11', 'corefonts'],
        registry_tweaks={
            'HKEY_CURRENT_USER\\Software\\Wine\\Direct3D': {
                'CSMT': 'enabled',
                'Renderer': 'opengl',
                'VideoMemorySize': 4096
            },
            'HKEY_CURRENT_USER\\Software\\Adobe\\Premiere Pro\\14.0': {
                'GPU Acceleration': 1,
                'CUDA': 1,
                'OpenCL': 1
            }
        },
        environment_variables={
            'DXVK_HUD': 'off',
            'PROTON_USE_WINED3D': '0'
        },
        required_dependencies=['libssl-dev', 'libxss1', 'libappindicator1'],
        minimum_ram_gb=16,
        gpu_required=True,
        notes="Adobe Premiere requires NVIDIA GPU for CUDA acceleration"
    )
    
    def install(self, installer_path: str) -> bool:
        """Install Adobe Premiere Pro"""
        print(f"\n[Premiere] Installing {self.CONFIG.name}...")
        
        try:
            # Install dependencies
            print("[Premiere] Installing dependencies...")
            DistroUtils.install_packages(self.CONFIG.required_dependencies, use_sudo=True)
            
            # Install DLLs
            self.install_required_dlls(self.CONFIG.required_dlls)
            
            # Configure registry
            self.configure_registry(self.CONFIG.registry_tweaks)
            
            # Run installer
            if os.path.exists(installer_path):
                print("[Premiere] Running installer...")
                self.run_with_wine(installer_path)
            
            print("✓ Adobe Premiere Pro configured for Wine")
            return True
        except Exception as e:
            print(f"✗ Adobe Premiere installation failed: {e}")
            return False

class SonyVegasInstaller(ApplicationInstaller):
    """Sony Vegas Pro installer and configurator"""
    
    CONFIG = ApplicationConfig(
        name="Sony Vegas Pro",
        windows_executable="Vegas.exe",
        required_dlls=['dotnet48', 'd3dx9', 'd3dx11', 'corefonts', 'vcrun2019'],
        registry_tweaks={
            'HKEY_CURRENT_USER\\Software\\Wine\\Direct3D': {
                'CSMT': 'enabled',
                'Renderer': 'opengl',
                'VideoMemorySize': 2048
            },
            'HKEY_CURRENT_USER\\Software\\Sony\\Vegas\\19.0': {
                'HardwareAcceleration': 1,
                'CUDA': 1
            }
        },
        environment_variables={
            'DXVK_HUD': 'off'
        },
        required_dependencies=['libssl-dev', 'libxss1'],
        minimum_ram_gb=8,
        gpu_required=False,
        notes="Sony Vegas Pro works with GPU acceleration on NVIDIA/AMD"
    )
    
    def install(self, installer_path: str) -> bool:
        """Install Sony Vegas Pro"""
        print(f"\n[Vegas] Installing {self.CONFIG.name}...")
        
        try:
            # Install dependencies
            print("[Vegas] Installing dependencies...")
            DistroUtils.install_packages(self.CONFIG.required_dependencies, use_sudo=True)
            
            # Install DLLs
            self.install_required_dlls(self.CONFIG.required_dlls)
            
            # Configure registry
            self.configure_registry(self.CONFIG.registry_tweaks)
            
            # Run installer
            if os.path.exists(installer_path):
                print("[Vegas] Running installer...")
                self.run_with_wine(installer_path)
            
            print("✓ Sony Vegas Pro configured for Wine")
            return True
        except Exception as e:
            print(f"✗ Sony Vegas installation failed: {e}")
            return False

class Autodesk3DSMaxInstaller(ApplicationInstaller):
    """Autodesk 3DS Max installer and configurator"""
    
    CONFIG = ApplicationConfig(
        name="Autodesk 3DS Max",
        windows_executable="3dsmax.exe",
        required_dlls=['dotnet48', 'd3dx9', 'd3dx10', 'd3dx11', 'd3dx12', 'vcrun2019', 'corefonts'],
        registry_tweaks={
            'HKEY_CURRENT_USER\\Software\\Wine\\Direct3D': {
                'CSMT': 'enabled',
                'Renderer': 'opengl',
                'VideoMemorySize': 4096,
                'StrictDrawOrdering': 'enabled'
            },
            'HKEY_CURRENT_USER\\Software\\Autodesk\\3dsmax\\2024': {
                'HardwareRenderer': 'DirectX11',
                'GPUDeviceIndex': 0
            }
        },
        environment_variables={
            'DXVK_HUD': 'off',
            'PROTON_USE_WINED3D': '0'
        },
        required_dependencies=['libssl-dev', 'libx11-6', 'libxext6', 'libxrender1'],
        minimum_ram_gb=16,
        gpu_required=True,
        notes="3DS Max requires dedicated GPU for viewport performance"
    )
    
    def install(self, installer_path: str) -> bool:
        """Install Autodesk 3DS Max"""
        print(f"\n[3DSMax] Installing {self.CONFIG.name}...")
        
        try:
            # Install dependencies
            print("[3DS Max] Installing dependencies...")
            DistroUtils.install_packages(self.CONFIG.required_dependencies, use_sudo=True)
            
            # Install DLLs
            self.install_required_dlls(self.CONFIG.required_dlls)
            
            # Configure registry
            self.configure_registry(self.CONFIG.registry_tweaks)
            
            # Run installer
            if os.path.exists(installer_path):
                print("[3DSMax] Running installer...")
                self.run_with_wine(installer_path)
            
            print("✓ Autodesk 3DS Max configured for Wine")
            return True
        except Exception as e:
            print(f"✗ Autodesk 3DS Max installation failed: {e}")
            return False

class MicrosoftOfficeInstaller(ApplicationInstaller):
    """Microsoft Office installer and configurator"""
    
    CONFIG = ApplicationConfig(
        name="Microsoft Office",
        windows_executable="WINWORD.EXE",
        required_dlls=['dotnet48', 'corefonts', 'vcrun2019', 'vb6run'],
        registry_tweaks={
            'HKEY_CURRENT_USER\\Software\\Microsoft\\Office\\16.0\\Word': {
                'HardwareAcceleration': 1
            }
        },
        environment_variables={
            'DXVK_HUD': 'off'
        },
        required_dependencies=['libssl-dev'],
        minimum_ram_gb=4,
        gpu_required=False,
        notes="Microsoft Office works well with Wine/Proton"
    )
    
    def install(self, installer_path: str) -> bool:
        """Install Microsoft Office"""
        print(f"\n[Office] Installing {self.CONFIG.name}...")
        
        try:
            # Install dependencies
            print("[Office] Installing dependencies...")
            DistroUtils.install_packages(self.CONFIG.required_dependencies, use_sudo=True)
            
            # Install DLLs
            self.install_required_dlls(self.CONFIG.required_dlls)
            
            # Configure registry
            self.configure_registry(self.CONFIG.registry_tweaks)
            
            # Run installer
            if os.path.exists(installer_path):
                print("[Office] Running installer...")
                self.run_with_wine(installer_path)
            
            print("✓ Microsoft Office configured for Wine")
            return True
        except Exception as e:
            print(f"✗ Microsoft Office installation failed: {e}")
            return False

# ==================== AUDIO SOFTWARE ====================

class AdobeAuditionInstaller(ApplicationInstaller):
    """Adobe Audition installer and configurator"""
    
    CONFIG = ApplicationConfig(
        name="Adobe Audition",
        windows_executable="Audition.exe",
        required_dlls=['dotnet48', 'd3dx9', 'd3dx11', 'corefonts', 'vcrun2019'],
        registry_tweaks={
            'HKEY_CURRENT_USER\\Software\\Adobe\\Audition\\2024': {
                'HardwareAcceleration': 1,
                'AudioBufferSize': 512
            }
        },
        environment_variables={
            'DXVK_HUD': 'off',
            'ALSA_CONFIG_DIR': '/etc/alsa'
        },
        required_dependencies=['libpulse-dev', 'libasound2-dev', 'libsndfile1-dev'],
        minimum_ram_gb=8,
        gpu_required=False,
        notes="Adobe Audition audio editing suite"
    )
    
    def install(self, installer_path: str) -> bool:
        """Install Adobe Audition"""
        print(f"\n[Audition] Installing {self.CONFIG.name}...")
        try:
            for dep in self.CONFIG.required_dependencies:
                subprocess.run(['sudo', 'apt', 'install', '-y', dep],
                             capture_output=True, check=False)
            
            self.install_required_dlls(self.CONFIG.required_dlls)
            self.configure_registry(self.CONFIG.registry_tweaks)
            
            if os.path.exists(installer_path):
                self.run_with_wine(installer_path)
            
            print("✓ Adobe Audition configured for Wine")
            return True
        except Exception as e:
            print(f"✗ Adobe Audition installation failed: {e}")
            return False

class SteinbergCubaseInstaller(ApplicationInstaller):
    """Steinberg Cubase DAW installer and configurator"""
    
    CONFIG = ApplicationConfig(
        name="Steinberg Cubase",
        windows_executable="Cubase.exe",
        required_dlls=['dotnet48', 'd3dx9', 'd3dx11', 'corefonts', 'vcrun2019'],
        registry_tweaks={
            'HKEY_CURRENT_USER\\Software\\Steinberg\\Cubase\\12.0': {
                'BufferSize': 512,
                'SampleRate': 48000
            }
        },
        environment_variables={
            'DXVK_HUD': 'off',
            'WINE_CPU_TOPOLOGY': '4:2'
        },
        required_dependencies=['libpulse-dev', 'libasound2-dev', 'libsndfile1-dev', 'jackd'],
        minimum_ram_gb=16,
        gpu_required=False,
        notes="Professional DAW with VST support"
    )
    
    def install(self, installer_path: str) -> bool:
        """Install Cubase"""
        print(f"\n[Cubase] Installing {self.CONFIG.name}...")
        try:
            for dep in self.CONFIG.required_dependencies:
                subprocess.run(['sudo', 'apt', 'install', '-y', dep],
                             capture_output=True, check=False)
            
            self.install_required_dlls(self.CONFIG.required_dlls)
            self.configure_registry(self.CONFIG.registry_tweaks)
            
            if os.path.exists(installer_path):
                self.run_with_wine(installer_path)
            
            print("✓ Cubase configured for Wine")
            return True
        except Exception as e:
            print(f"✗ Cubase installation failed: {e}")
            return False

class ABLETONLiveInstaller(ApplicationInstaller):
    """Ableton Live installer and configurator"""
    
    CONFIG = ApplicationConfig(
        name="Ableton Live",
        windows_executable="Ableton Live 12 Suite.exe",
        required_dlls=['dotnet48', 'd3dx9', 'd3dx11', 'corefonts', 'vcrun2019'],
        registry_tweaks={
            'HKEY_CURRENT_USER\\Software\\Ableton\\Live\\12.0': {
                'AudioBufferSize': 256,
                'BufferSize': 512
            }
        },
        environment_variables={
            'DXVK_HUD': 'off'
        },
        required_dependencies=['libpulse-dev', 'libasound2-dev', 'jackd'],
        minimum_ram_gb=8,
        gpu_required=False,
        notes="Music production DAW"
    )
    
    def install(self, installer_path: str) -> bool:
        """Install Ableton Live"""
        print(f"\n[Ableton] Installing {self.CONFIG.name}...")
        try:
            for dep in self.CONFIG.required_dependencies:
                subprocess.run(['sudo', 'apt', 'install', '-y', dep],
                             capture_output=True, check=False)
            
            self.install_required_dlls(self.CONFIG.required_dlls)
            self.configure_registry(self.CONFIG.registry_tweaks)
            
            if os.path.exists(installer_path):
                self.run_with_wine(installer_path)
            
            print("✓ Ableton Live configured for Wine")
            return True
        except Exception as e:
            print(f"✗ Ableton Live installation failed: {e}")
            return False

# ==================== CAD SOFTWARE ====================

class AutodeskAutoCADInstaller(ApplicationInstaller):
    """Autodesk AutoCAD installer and configurator"""
    
    CONFIG = ApplicationConfig(
        name="Autodesk AutoCAD",
        windows_executable="acad.exe",
        required_dlls=['dotnet48', 'd3dx9', 'd3dx10', 'd3dx11', 'd3dx12', 'vcrun2019', 'corefonts'],
        registry_tweaks={
            'HKEY_CURRENT_USER\\Software\\Autodesk\\AutoCAD\\2024': {
                'HardwareRenderer': 'DirectX11',
                'Performance': 'High'
            }
        },
        environment_variables={
            'DXVK_HUD': 'off',
            'PROTON_USE_WINED3D': '0'
        },
        required_dependencies=['libssl-dev', 'libx11-6', 'libxext6', 'libxrender1'],
        minimum_ram_gb=16,
        gpu_required=True,
        notes="Professional 2D/3D CAD software"
    )
    
    def install(self, installer_path: str) -> bool:
        """Install AutoCAD"""
        print(f"\n[AutoCAD] Installing {self.CONFIG.name}...")
        try:
            for dep in self.CONFIG.required_dependencies:
                subprocess.run(['sudo', 'apt', 'install', '-y', dep],
                             capture_output=True, check=False)
            
            self.install_required_dlls(self.CONFIG.required_dlls)
            self.configure_registry(self.CONFIG.registry_tweaks)
            
            if os.path.exists(installer_path):
                self.run_with_wine(installer_path)
            
            print("✓ AutoCAD configured for Wine")
            return True
        except Exception as e:
            print(f"✗ AutoCAD installation failed: {e}")
            return False

class SolidWorksInstaller(ApplicationInstaller):
    """SolidWorks CAD installer and configurator"""
    
    CONFIG = ApplicationConfig(
        name="SolidWorks",
        windows_executable="sldworks.exe",
        required_dlls=['dotnet48', 'd3dx9', 'd3dx10', 'd3dx11', 'd3dx12', 'vcrun2019', 'corefonts'],
        registry_tweaks={
            'HKEY_CURRENT_USER\\Software\\SolidWorks\\SolidWorks 2024': {
                'Performance': 'Maximum',
                'GPU': 'Enabled'
            }
        },
        environment_variables={
            'DXVK_HUD': 'off',
            'PROTON_USE_WINED3D': '0'
        },
        required_dependencies=['libssl-dev', 'libx11-6', 'libxext6'],
        minimum_ram_gb=16,
        gpu_required=True,
        notes="3D CAD design software"
    )
    
    def install(self, installer_path: str) -> bool:
        """Install SolidWorks"""
        print(f"\n[SolidWorks] Installing {self.CONFIG.name}...")
        try:
            for dep in self.CONFIG.required_dependencies:
                subprocess.run(['sudo', 'apt', 'install', '-y', dep],
                             capture_output=True, check=False)
            
            self.install_required_dlls(self.CONFIG.required_dlls)
            self.configure_registry(self.CONFIG.registry_tweaks)
            
            if os.path.exists(installer_path):
                self.run_with_wine(installer_path)
            
            print("✓ SolidWorks configured for Wine")
            return True
        except Exception as e:
            print(f"✗ SolidWorks installation failed: {e}")
            return False

class FusionInstaller(ApplicationInstaller):
    """Autodesk Fusion 360 installer and configurator"""
    
    CONFIG = ApplicationConfig(
        name="Autodesk Fusion 360",
        windows_executable="Fusion360.exe",
        required_dlls=['dotnet48', 'd3dx9', 'd3dx10', 'd3dx11', 'd3dx12', 'vcrun2019', 'corefonts'],
        registry_tweaks={
            'HKEY_CURRENT_USER\\Software\\Autodesk\\Fusion360\\1.0': {
                'GPU': 'Enabled',
                'ViewportPerformance': 'High'
            }
        },
        environment_variables={
            'DXVK_HUD': 'off',
            'PROTON_USE_WINED3D': '0'
        },
        required_dependencies=['libssl-dev', 'libx11-6'],
        minimum_ram_gb=8,
        gpu_required=True,
        notes="Cloud-based 3D CAD/CAM platform"
    )
    
    def install(self, installer_path: str) -> bool:
        """Install Fusion 360"""
        print(f"\n[Fusion] Installing {self.CONFIG.name}...")
        try:
            for dep in self.CONFIG.required_dependencies:
                subprocess.run(['sudo', 'apt', 'install', '-y', dep],
                             capture_output=True, check=False)
            
            self.install_required_dlls(self.CONFIG.required_dlls)
            self.configure_registry(self.CONFIG.registry_tweaks)
            
            if os.path.exists(installer_path):
                self.run_with_wine(installer_path)
            
            print("✓ Fusion 360 configured for Wine")
            return True
        except Exception as e:
            print(f"✗ Fusion 360 installation failed: {e}")
            return False

# ==================== PROGRAMMING TOOLS ====================

class VisualStudioInstaller(ApplicationInstaller):
    """Microsoft Visual Studio installer and configurator"""
    
    CONFIG = ApplicationConfig(
        name="Microsoft Visual Studio",
        windows_executable="devenv.exe",
        required_dlls=['dotnet48', 'dotnet462', 'vcrun2019', 'corefonts'],
        registry_tweaks={
            'HKEY_CURRENT_USER\\Software\\Microsoft\\VisualStudio\\17.0': {
                'Performance': 'Optimized'
            }
        },
        environment_variables={
            'DXVK_HUD': 'off'
        },
        required_dependencies=['libssl-dev', 'libxml2-dev'],
        minimum_ram_gb=8,
        gpu_required=False,
        notes="IDE for C#, C++, Python development"
    )
    
    def install(self, installer_path: str) -> bool:
        """Install Visual Studio"""
        print(f"\n[VS] Installing {self.CONFIG.name}...")
        try:
            for dep in self.CONFIG.required_dependencies:
                subprocess.run(['sudo', 'apt', 'install', '-y', dep],
                             capture_output=True, check=False)
            
            self.install_required_dlls(self.CONFIG.required_dlls)
            self.configure_registry(self.CONFIG.registry_tweaks)
            
            if os.path.exists(installer_path):
                self.run_with_wine(installer_path)
            
            print("✓ Visual Studio configured for Wine")
            return True
        except Exception as e:
            print(f"✗ Visual Studio installation failed: {e}")
            return False

class JetBrainsIDEInstaller(ApplicationInstaller):
    """JetBrains IDE installer (PyCharm, IntelliJ IDEA, WebStorm, etc.)"""
    
    CONFIG = ApplicationConfig(
        name="JetBrains IDE",
        windows_executable="bin/idea.exe",
        required_dlls=['dotnet48', 'vcrun2019', 'corefonts'],
        registry_tweaks={
            'HKEY_CURRENT_USER\\Software\\JetBrains\\IDE': {
                'Performance': 'Maximum'
            }
        },
        environment_variables={
            'DXVK_HUD': 'off',
            '_JAVA_OPTIONS': '-Xmx4096m'
        },
        required_dependencies=['openjdk-17-jdk', 'libssl-dev'],
        minimum_ram_gb=4,
        gpu_required=False,
        notes="PyCharm, IntelliJ IDEA, WebStorm, Rider, etc."
    )
    
    def install(self, installer_path: str) -> bool:
        """Install JetBrains IDE"""
        print(f"\n[JetBrains] Installing {self.CONFIG.name}...")
        try:
            for dep in self.CONFIG.required_dependencies:
                subprocess.run(['sudo', 'apt', 'install', '-y', dep],
                             capture_output=True, check=False)
            
            self.install_required_dlls(self.CONFIG.required_dlls)
            self.configure_registry(self.CONFIG.registry_tweaks)
            
            if os.path.exists(installer_path):
                self.run_with_wine(installer_path)
            
            print("✓ JetBrains IDE configured for Wine")
            return True
        except Exception as e:
            print(f"✗ JetBrains IDE installation failed: {e}")
            return False

class UnityInstaller(ApplicationInstaller):
    """Unity Game Engine installer and configurator"""
    
    CONFIG = ApplicationConfig(
        name="Unity Engine",
        windows_executable="Unity.exe",
        required_dlls=['dotnet48', 'd3dx9', 'd3dx10', 'd3dx11', 'd3dx12', 'vcrun2019', 'corefonts'],
        registry_tweaks={
            'HKEY_CURRENT_USER\\Software\\Unity\\Editor\\2023.2': {
                'Performance': 'Maximum',
                'GPU': 'Enabled'
            }
        },
        environment_variables={
            'DXVK_HUD': 'off',
            'PROTON_USE_WINED3D': '0'
        },
        required_dependencies=['libssl-dev', 'libx11-6'],
        minimum_ram_gb=8,
        gpu_required=True,
        notes="Game engine and development platform"
    )
    
    def install(self, installer_path: str) -> bool:
        """Install Unity"""
        print(f"\n[Unity] Installing {self.CONFIG.name}...")
        try:
            for dep in self.CONFIG.required_dependencies:
                subprocess.run(['sudo', 'apt', 'install', '-y', dep],
                             capture_output=True, check=False)
            
            self.install_required_dlls(self.CONFIG.required_dlls)
            self.configure_registry(self.CONFIG.registry_tweaks)
            
            if os.path.exists(installer_path):
                self.run_with_wine(installer_path)
            
            print("✓ Unity configured for Wine")
            return True
        except Exception as e:
            print(f"✗ Unity installation failed: {e}")
            return False

class UnrealEngineInstaller(ApplicationInstaller):
    """Unreal Engine installer and configurator"""
    
    CONFIG = ApplicationConfig(
        name="Unreal Engine",
        windows_executable="UE4Editor.exe",
        required_dlls=['dotnet48', 'd3dx9', 'd3dx10', 'd3dx11', 'd3dx12', 'vcrun2019', 'corefonts'],
        registry_tweaks={
            'HKEY_CURRENT_USER\\Software\\EpicGames\\Unreal Engine\\5.3': {
                'GPU': 'Enabled',
                'Performance': 'Maximum'
            }
        },
        environment_variables={
            'DXVK_HUD': 'off',
            'PROTON_USE_WINED3D': '0'
        },
        required_dependencies=['libssl-dev', 'libx11-6'],
        minimum_ram_gb=16,
        gpu_required=True,
        notes="Professional game engine"
    )
    
    def install(self, installer_path: str) -> bool:
        """Install Unreal Engine"""
        print(f"\n[UE] Installing {self.CONFIG.name}...")
        try:
            for dep in self.CONFIG.required_dependencies:
                subprocess.run(['sudo', 'apt', 'install', '-y', dep],
                             capture_output=True, check=False)
            
            self.install_required_dlls(self.CONFIG.required_dlls)
            self.configure_registry(self.CONFIG.registry_tweaks)
            
            if os.path.exists(installer_path):
                self.run_with_wine(installer_path)
            
            print("✓ Unreal Engine configured for Wine")
            return True
        except Exception as e:
            print(f"✗ Unreal Engine installation failed: {e}")
            return False

# ==================== ADOBE CREATIVE SUITE ====================

class AdobePhotoshopInstaller(ApplicationInstaller):
    """Adobe Photoshop installer and configurator"""
    
    CONFIG = ApplicationConfig(
        name="Adobe Photoshop",
        windows_executable="Photoshop.exe",
        required_dlls=['dotnet48', 'd3dx9', 'd3dx11', 'corefonts', 'vcrun2019'],
        registry_tweaks={
            'HKEY_CURRENT_USER\\Software\\Adobe\\Photoshop\\2024': {
                'GPUAcceleration': 1,
                'VRAM': 2048
            }
        },
        environment_variables={
            'DXVK_HUD': 'off'
        },
        required_dependencies=['libssl-dev', 'libx11-6', 'libxext6'],
        minimum_ram_gb=4,
        gpu_required=False,
        notes="Professional image editing and graphic design"
    )
    
    def install(self, installer_path: str) -> bool:
        """Install Adobe Photoshop"""
        print(f"\n[Photoshop] Installing {self.CONFIG.name}...")
        try:
            print("[Photoshop] Installing dependencies...")
            DistroUtils.install_packages(self.CONFIG.required_dependencies, use_sudo=True)
            
            self.install_required_dlls(self.CONFIG.required_dlls)
            self.configure_registry(self.CONFIG.registry_tweaks)
            
            if os.path.exists(installer_path):
                print("[Photoshop] Running installer...")
                self.run_with_wine(installer_path)
            
            print("✓ Adobe Photoshop configured for Wine")
            return True
        except Exception as e:
            print(f"✗ Adobe Photoshop installation failed: {e}")
            return False

class AdobeLightroomInstaller(ApplicationInstaller):
    """Adobe Lightroom installer and configurator"""
    
    CONFIG = ApplicationConfig(
        name="Adobe Lightroom",
        windows_executable="Lightroom.exe",
        required_dlls=['dotnet48', 'd3dx9', 'd3dx11', 'corefonts', 'vcrun2019'],
        registry_tweaks={
            'HKEY_CURRENT_USER\\Software\\Adobe\\Lightroom\\2024': {
                'GPU': 'enabled',
                'CacheSize': 4096
            }
        },
        environment_variables={
            'DXVK_HUD': 'off'
        },
        required_dependencies=['libssl-dev', 'libx11-6'],
        minimum_ram_gb=4,
        gpu_required=False,
        notes="Professional photo management and editing"
    )
    
    def install(self, installer_path: str) -> bool:
        """Install Adobe Lightroom"""
        print(f"\n[Lightroom] Installing {self.CONFIG.name}...")
        try:
            print("[Lightroom] Installing dependencies...")
            DistroUtils.install_packages(self.CONFIG.required_dependencies, use_sudo=True)
            
            self.install_required_dlls(self.CONFIG.required_dlls)
            self.configure_registry(self.CONFIG.registry_tweaks)
            
            if os.path.exists(installer_path):
                print("[Lightroom] Running installer...")
                self.run_with_wine(installer_path)
            
            print("✓ Adobe Lightroom configured for Wine")
            return True
        except Exception as e:
            print(f"✗ Adobe Lightroom installation failed: {e}")
            return False

class AdobeIllustratorInstaller(ApplicationInstaller):
    """Adobe Illustrator installer and configurator"""
    
    CONFIG = ApplicationConfig(
        name="Adobe Illustrator",
        windows_executable="Illustrator.exe",
        required_dlls=['dotnet48', 'd3dx9', 'd3dx11', 'corefonts', 'vcrun2019'],
        registry_tweaks={
            'HKEY_CURRENT_USER\\Software\\Adobe\\Illustrator\\2024': {
                'GPU': 'enabled',
                'Performance': 'high'
            }
        },
        environment_variables={
            'DXVK_HUD': 'off'
        },
        required_dependencies=['libssl-dev', 'libx11-6', 'libxext6'],
        minimum_ram_gb=4,
        gpu_required=False,
        notes="Professional vector graphics and illustration"
    )
    
    def install(self, installer_path: str) -> bool:
        """Install Adobe Illustrator"""
        print(f"\n[Illustrator] Installing {self.CONFIG.name}...")
        try:
            print("[Illustrator] Installing dependencies...")
            DistroUtils.install_packages(self.CONFIG.required_dependencies, use_sudo=True)
            
            self.install_required_dlls(self.CONFIG.required_dlls)
            self.configure_registry(self.CONFIG.registry_tweaks)
            
            if os.path.exists(installer_path):
                print("[Illustrator] Running installer...")
                self.run_with_wine(installer_path)
            
            print("✓ Adobe Illustrator configured for Wine")
            return True
        except Exception as e:
            print(f"✗ Adobe Illustrator installation failed: {e}")
            return False

class AdobeAfterEffectsInstaller(ApplicationInstaller):
    """Adobe After Effects installer and configurator"""
    
    CONFIG = ApplicationConfig(
        name="Adobe After Effects",
        windows_executable="AfterFX.exe",
        required_dlls=['dotnet48', 'd3dx9', 'd3dx10', 'd3dx11', 'd3dx12', 'corefonts', 'vcrun2019'],
        registry_tweaks={
            'HKEY_CURRENT_USER\\Software\\Adobe\\After Effects\\2024': {
                'GPUAcceleration': 1,
                'CUDA': 1,
                'RayTracing': 1
            }
        },
        environment_variables={
            'DXVK_HUD': 'off',
            'PROTON_USE_WINED3D': '0'
        },
        required_dependencies=['libssl-dev', 'libx11-6', 'libxext6'],
        minimum_ram_gb=4,
        gpu_required=False,
        notes="Professional motion graphics and VFX composition"
    )
    
    def install(self, installer_path: str) -> bool:
        """Install Adobe After Effects"""
        print(f"\n[AfterFX] Installing {self.CONFIG.name}...")
        try:
            print("[AfterFX] Installing dependencies...")
            DistroUtils.install_packages(self.CONFIG.required_dependencies, use_sudo=True)
            
            self.install_required_dlls(self.CONFIG.required_dlls)
            self.configure_registry(self.CONFIG.registry_tweaks)
            
            if os.path.exists(installer_path):
                print("[AfterFX] Running installer...")
                self.run_with_wine(installer_path)
            
            print("✓ Adobe After Effects configured for Wine")
            return True
        except Exception as e:
            print(f"✗ Adobe After Effects installation failed: {e}")
            return False

# ==================== AUTODESK & 3D SOFTWARE ====================

class AutodeskRevitInstaller(ApplicationInstaller):
    """Autodesk Revit installer and configurator"""
    
    CONFIG = ApplicationConfig(
        name="Autodesk Revit",
        windows_executable="Revit.exe",
        required_dlls=['dotnet48', 'd3dx9', 'd3dx10', 'd3dx11', 'd3dx12', 'vcrun2019', 'corefonts'],
        registry_tweaks={
            'HKEY_CURRENT_USER\\Software\\Autodesk\\Revit\\2024': {
                'GPU': 'enabled',
                'ViewportPerformance': 'high',
                'HardwareAcceleration': 1
            }
        },
        environment_variables={
            'DXVK_HUD': 'off',
            'PROTON_USE_WINED3D': '0'
        },
        required_dependencies=['libssl-dev', 'libx11-6', 'libxext6'],
        minimum_ram_gb=4,
        gpu_required=False,
        notes="BIM and architectural design software"
    )
    
    def install(self, installer_path: str) -> bool:
        """Install Autodesk Revit"""
        print(f"\n[Revit] Installing {self.CONFIG.name}...")
        try:
            print("[Revit] Installing dependencies...")
            DistroUtils.install_packages(self.CONFIG.required_dependencies, use_sudo=True)
            
            self.install_required_dlls(self.CONFIG.required_dlls)
            self.configure_registry(self.CONFIG.registry_tweaks)
            
            if os.path.exists(installer_path):
                print("[Revit] Running installer...")
                self.run_with_wine(installer_path)
            
            print("✓ Autodesk Revit configured for Wine")
            return True
        except Exception as e:
            print(f"✗ Autodesk Revit installation failed: {e}")
            return False

class AutodeskSketchbookInstaller(ApplicationInstaller):
    """Autodesk Sketchbook installer and configurator"""
    
    CONFIG = ApplicationConfig(
        name="Autodesk Sketchbook",
        windows_executable="Sketchbook.exe",
        required_dlls=['dotnet48', 'd3dx9', 'd3dx11', 'corefonts', 'vcrun2019'],
        registry_tweaks={
            'HKEY_CURRENT_USER\\Software\\Autodesk\\Sketchbook\\2024': {
                'HardwareAcceleration': 1
            }
        },
        environment_variables={
            'DXVK_HUD': 'off'
        },
        required_dependencies=['libssl-dev', 'libx11-6'],
        minimum_ram_gb=4,
        gpu_required=False,
        notes="Digital painting and drawing software"
    )
    
    def install(self, installer_path: str) -> bool:
        """Install Autodesk Sketchbook"""
        print(f"\n[Sketchbook] Installing {self.CONFIG.name}...")
        try:
            print("[Sketchbook] Installing dependencies...")
            DistroUtils.install_packages(self.CONFIG.required_dependencies, use_sudo=True)
            
            self.install_required_dlls(self.CONFIG.required_dlls)
            self.configure_registry(self.CONFIG.registry_tweaks)
            
            if os.path.exists(installer_path):
                print("[Sketchbook] Running installer...")
                self.run_with_wine(installer_path)
            
            print("✓ Autodesk Sketchbook configured for Wine")
            return True
        except Exception as e:
            print(f"✗ Autodesk Sketchbook installation failed: {e}")
            return False

# ==================== COREL SOFTWARE ====================

class CorelDrawInstaller(ApplicationInstaller):
    """Corel Draw installer and configurator"""
    
    CONFIG = ApplicationConfig(
        name="CorelDRAW",
        windows_executable="CorelDRAW.exe",
        required_dlls=['dotnet48', 'd3dx9', 'd3dx11', 'corefonts', 'vcrun2019'],
        registry_tweaks={
            'HKEY_CURRENT_USER\\Software\\Corel\\CorelDRAW\\2024': {
                'GPU': 'enabled',
                'Performance': 'high'
            }
        },
        environment_variables={
            'DXVK_HUD': 'off'
        },
        required_dependencies=['libssl-dev', 'libx11-6', 'libxext6'],
        minimum_ram_gb=4,
        gpu_required=False,
        notes="Professional vector graphics and design"
    )
    
    def install(self, installer_path: str) -> bool:
        """Install CorelDRAW"""
        print(f"\n[CorelDRAW] Installing {self.CONFIG.name}...")
        try:
            print("[CorelDRAW] Installing dependencies...")
            DistroUtils.install_packages(self.CONFIG.required_dependencies, use_sudo=True)
            
            self.install_required_dlls(self.CONFIG.required_dlls)
            self.configure_registry(self.CONFIG.registry_tweaks)
            
            if os.path.exists(installer_path):
                print("[CorelDRAW] Running installer...")
                self.run_with_wine(installer_path)
            
            print("✓ CorelDRAW configured for Wine")
            return True
        except Exception as e:
            print(f"✗ CorelDRAW installation failed: {e}")
            return False

class CorelPaintInstaller(ApplicationInstaller):
    """Corel Painter installer and configurator"""
    
    CONFIG = ApplicationConfig(
        name="Corel Painter",
        windows_executable="Painter.exe",
        required_dlls=['dotnet48', 'd3dx9', 'd3dx11', 'corefonts', 'vcrun2019'],
        registry_tweaks={
            'HKEY_CURRENT_USER\\Software\\Corel\\Painter\\2024': {
                'HardwareAcceleration': 1
            }
        },
        environment_variables={
            'DXVK_HUD': 'off'
        },
        required_dependencies=['libssl-dev', 'libx11-6'],
        minimum_ram_gb=4,
        gpu_required=False,
        notes="Professional digital painting and illustration"
    )
    
    def install(self, installer_path: str) -> bool:
        """Install Corel Painter"""
        print(f"\n[CorelPainter] Installing {self.CONFIG.name}...")
        try:
            print("[CorelPainter] Installing dependencies...")
            DistroUtils.install_packages(self.CONFIG.required_dependencies, use_sudo=True)
            
            self.install_required_dlls(self.CONFIG.required_dlls)
            self.configure_registry(self.CONFIG.registry_tweaks)
            
            if os.path.exists(installer_path):
                print("[CorelPainter] Running installer...")
                self.run_with_wine(installer_path)
            
            print("✓ Corel Painter configured for Wine")
            return True
        except Exception as e:
            print(f"✗ Corel Painter installation failed: {e}")
            return False

class MicrosoftTeamsInstaller(ApplicationInstaller):
    """Microsoft Teams installer and configurator"""

    CONFIG = ApplicationConfig(
        name="Microsoft Teams",
        windows_executable="Teams.exe",
        required_dlls=['dotnet48', 'corefonts', 'vcrun2019'],
        registry_tweaks={
            'HKEY_CURRENT_USER\\Software\\Microsoft\\Teams': {
                'HardwareAcceleration': 1
            }
        },
        environment_variables={
            'DXVK_HUD': 'off'
        },
        required_dependencies=['libssl-dev', 'libx11-6'],
        minimum_ram_gb=4,
        gpu_required=False,
        notes="Collaboration and meetings client"
    )

    def install(self, installer_path: str) -> bool:
        """Install Microsoft Teams"""
        print(f"\n[Teams] Installing {self.CONFIG.name}...")
        try:
            DistroUtils.install_packages(self.CONFIG.required_dependencies, use_sudo=True)
            self.install_required_dlls(self.CONFIG.required_dlls)
            self.configure_registry(self.CONFIG.registry_tweaks)

            if os.path.exists(installer_path):
                print("[Teams] Running installer...")
                self.run_with_wine(installer_path)

            print("✓ Microsoft Teams configured for Wine")
            return True
        except Exception as e:
            print(f"✗ Microsoft Teams installation failed: {e}")
            return False


class MicrosoftCopilotInstaller(ApplicationInstaller):
    """Microsoft Copilot (desktop) installer and configurator"""

    CONFIG = ApplicationConfig(
        name="Microsoft Copilot",
        windows_executable="Copilot.exe",
        required_dlls=['dotnet48', 'corefonts'],
        registry_tweaks={
            'HKEY_CURRENT_USER\\Software\\Microsoft\\Copilot': {
                'EnableGPU': 0
            }
        },
        environment_variables={
            'DXVK_HUD': 'off'
        },
        required_dependencies=['libssl-dev'],
        minimum_ram_gb=4,
        gpu_required=False,
        notes="AI assistant integrations and widgets"
    )

    def install(self, installer_path: str) -> bool:
        """Install Microsoft Copilot"""
        print(f"\n[Copilot] Installing {self.CONFIG.name}...")
        try:
            DistroUtils.install_packages(self.CONFIG.required_dependencies, use_sudo=True)
            self.install_required_dlls(self.CONFIG.required_dlls)
            self.configure_registry(self.CONFIG.registry_tweaks)

            if os.path.exists(installer_path):
                print("[Copilot] Running installer...")
                self.run_with_wine(installer_path)

            print("✓ Microsoft Copilot configured for Wine")
            return True
        except Exception as e:
            print(f"✗ Microsoft Copilot installation failed: {e}")
            return False


class MicrosoftAccessInstaller(ApplicationInstaller):
    """Microsoft Access installer and configurator"""

    CONFIG = ApplicationConfig(
        name="Microsoft Access",
        windows_executable="MSACCESS.EXE",
        required_dlls=['dotnet48', 'corefonts', 'vcrun2019', 'vb6run'],
        registry_tweaks={
            'HKEY_CURRENT_USER\\Software\\Microsoft\\Office\\16.0\\Access': {
                'HardwareAcceleration': 0
            }
        },
        environment_variables={
            'DXVK_HUD': 'off'
        },
        required_dependencies=['libssl-dev'],
        minimum_ram_gb=4,
        gpu_required=False,
        notes="Database desktop application (part of Microsoft Office)"
    )

    def install(self, installer_path: str) -> bool:
        """Install Microsoft Access"""
        print(f"\n[Access] Installing {self.CONFIG.name}...")
        try:
            DistroUtils.install_packages(self.CONFIG.required_dependencies, use_sudo=True)
            self.install_required_dlls(self.CONFIG.required_dlls)
            self.configure_registry(self.CONFIG.registry_tweaks)

            if os.path.exists(installer_path):
                print("[Access] Running installer...")
                self.run_with_wine(installer_path)

            print("✓ Microsoft Access configured for Wine")
            return True
        except Exception as e:
            print(f"✗ Microsoft Access installation failed: {e}")
            return False


class ApplicationManager:
    """Manages all application installations"""
    
    APPLICATIONS = {
        # Video/Audio Production
        'premiere': AdobePremiereInstaller,
        'vegas': SonyVegasInstaller,
        '3dsmax': Autodesk3DSMaxInstaller,
        'office': MicrosoftOfficeInstaller,
        # Audio Production
        'audition': AdobeAuditionInstaller,
        'cubase': SteinbergCubaseInstaller,
        'ableton': ABLETONLiveInstaller,
        # CAD Software
        'autocad': AutodeskAutoCADInstaller,
        'solidworks': SolidWorksInstaller,
        'fusion360': FusionInstaller,
        # Adobe Creative Suite
        'photoshop': AdobePhotoshopInstaller,
        'lightroom': AdobeLightroomInstaller,
        'illustrator': AdobeIllustratorInstaller,
        'aftereffects': AdobeAfterEffectsInstaller,
        # Autodesk & 3D Software
        'revit': AutodeskRevitInstaller,
        'sketchbook': AutodeskSketchbookInstaller,
        # Corel Software
        'coreldraw': CorelDrawInstaller,
        'corelpainter': CorelPaintInstaller,
        # Microsoft Productivity
        'teams': MicrosoftTeamsInstaller,
        'copilot': MicrosoftCopilotInstaller,
        'access': MicrosoftAccessInstaller,
        # Programming & Game Engines
        'visualstudio': VisualStudioInstaller,
        'jetbrains': JetBrainsIDEInstaller,
        'unity': UnityInstaller,
        'unreal': UnrealEngineInstaller
    }
    
    def __init__(self, wine_prefix: str):
        self.wine_prefix = wine_prefix
    
    def get_installer(self, app_name: str) -> Optional[ApplicationInstaller]:
        """Get installer for application"""
        installer_class = self.APPLICATIONS.get(app_name.lower())
        if installer_class:
            return installer_class(self.wine_prefix)
        return None
    
    def list_applications(self) -> dict:
        """List all supported applications with requirements"""
        apps = {}
        for key, installer_class in self.APPLICATIONS.items():
            config = installer_class.CONFIG
            apps[key] = {
                'name': config.name,
                'minimum_ram_gb': config.minimum_ram_gb,
                'gpu_required': config.gpu_required,
                'notes': config.notes
            }
        return apps

if __name__ == "__main__":
    # Example usage
    wine_prefix = os.path.expanduser("~/.winpatable")
    manager = ApplicationManager(wine_prefix)
    
    print("\n" + "="*60)
    print("SUPPORTED APPLICATIONS")
    print("="*60)
    
    for app_key, app_info in manager.list_applications().items():
        print(f"\n{app_info['name']}:")
        print(f"  Minimum RAM: {app_info['minimum_ram_gb']}GB")
        print(f"  GPU Required: {'Yes' if app_info['gpu_required'] else 'No'}")
        print(f"  Notes: {app_info['notes']}")
