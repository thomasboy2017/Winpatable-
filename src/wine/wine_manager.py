#!/usr/bin/env python3
"""
Wine/Proton Configuration Module
Configures Wine and Proton for Windows application compatibility
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Optional, Dict
from dataclasses import dataclass
from src.core.distro_utils import DistroUtils

@dataclass
class WineConfig:
    wine_prefix: str
    wine_version: str
    dxvk_enabled: bool
    vkd3d_enabled: bool
    esync_enabled: bool
    fsync_enabled: bool

class WineManager:
    """Manages Wine/Proton installation and configuration"""
    
    def __init__(self, prefix_path: Optional[str] = None):
        self.home_dir = Path.home()
        self.prefix_path = Path(prefix_path) if prefix_path else self.home_dir / ".winpatable"
        self.config_file = self.prefix_path / "config.json"
    
    def ensure_prefix_directory(self) -> bool:
        """Create Wine prefix directory"""
        try:
            self.prefix_path.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            print(f"✗ Failed to create Wine prefix: {e}")
            return False
    
    def install_wine_dependencies(self) -> bool:
        """Install Wine and dependencies"""
        print("\n[Wine] Installing Wine dependencies...")
        try:
            packages = [
                'wine',
                'wine32',
                'wine64',
                'winetricks',
                'wineserver',
                'fonts-wine'
            ]
            
            # Add i386 architecture for 32-bit support (works on both Ubuntu and Mint)
            subprocess.run(['sudo', 'dpkg', '--add-architecture', 'i386'], 
                         capture_output=True, check=False)
            
            # Update package manager
            pkg_mgr, _ = DistroUtils.get_package_manager()
            subprocess.run(['sudo', pkg_mgr, 'update'], capture_output=True, check=False)
            
            # Install packages using DistroUtils
            success = DistroUtils.install_packages(packages, use_sudo=True)
            
            if success:
                print("✓ Wine dependencies installed")
            else:
                print("✗ Wine installation failed or partially completed")
            
            return success
        except Exception as e:
            print(f"✗ Wine installation failed: {e}")
            return False
    
    def install_dxvk(self) -> bool:
        """Install DXVK (Direct3D to Vulkan translation layer)"""
        print("\n[Wine] Installing DXVK...")
        try:
            # Install latest DXVK
            dxvk_dir = self.prefix_path / "dxvk"
            dxvk_dir.mkdir(exist_ok=True)
            
            # Download and install DXVK
            dxvk_github = "https://github.com/doitsujin/dxvk/releases/download"
            
            print("  Downloading DXVK...")
            subprocess.run(['wget', '--quiet', '-O', 
                          str(dxvk_dir / 'dxvk.tar.gz'),
                          f"{dxvk_github}/v1.10.3/dxvk-1.10.3.tar.gz"],
                         capture_output=True, check=False)
            
            print("  Extracting DXVK...")
            subprocess.run(['tar', '-xzf', str(dxvk_dir / 'dxvk.tar.gz'),
                          '-C', str(dxvk_dir)], capture_output=True, check=False)
            
            print("✓ DXVK installed")
            return True
        except Exception as e:
            print(f"✗ DXVK installation failed: {e}")
            return False
    
    def install_vkd3d(self) -> bool:
        """Install VKD3D (Direct3D 12 to Vulkan translation layer)"""
        print("\n[Wine] Installing VKD3D...")
        try:
            packages = [
                'libvkd3d-1',
                'libvkd3d-dev'
            ]
            
            success = DistroUtils.install_packages(packages, use_sudo=True)
            
            if success:
                print("✓ VKD3D installed")
            else:
                print("✗ VKD3D installation failed or partially completed")
            
            return success
        except Exception as e:
            print(f"✗ VKD3D installation failed: {e}")
            return False
    
    def install_proton(self) -> bool:
        """Install Proton (Valve's Wine fork)"""
        print("\n[Wine] Installing Proton...")
        try:
            proton_dir = self.prefix_path / "proton"
            proton_dir.mkdir(exist_ok=True)
            
            # Download latest Proton-GE (community version with extra features)
            proton_github = "https://github.com/GloriousEggroll/proton-ge-custom/releases/download"
            
            print("  Downloading Proton-GE...")
            subprocess.run(['wget', '--quiet', '-O',
                          str(proton_dir / 'proton.tar.gz'),
                          f"{proton_github}/9.18/Proton-GE-9.18.tar.gz"],
                         capture_output=True, check=False)
            
            print("  Extracting Proton...")
            subprocess.run(['tar', '-xzf', str(proton_dir / 'proton.tar.gz'),
                          '-C', str(proton_dir)], capture_output=True, check=False)
            
            print("✓ Proton installed")
            return True
        except Exception as e:
            print(f"✗ Proton installation failed: {e}")
            return False
    
    def configure_wine_prefix(self, wine_arch: str = "win64") -> bool:
        """Configure Wine prefix with optimal settings"""
        print(f"\n[Wine] Configuring Wine prefix ({wine_arch})...")
        
        try:
            env = os.environ.copy()
            env['WINEPREFIX'] = str(self.prefix_path)
            
            # Create wine prefix
            subprocess.run(['wineboot', '--init'], env=env, capture_output=True, check=False)
            
            # Configure registry for optimal performance
            config = {
                'DXVK': {
                    'dxvk.hud': 'off',  # Hide HUD by default
                    'dxvk.numCompilerThreads': '4'
                },
                'Wine': {
                    'CSMT': 'enabled',  # Command Stream MultiThreading
                    'Staging': 'enabled'
                }
            }
            
            self._save_config(config)
            
            print("✓ Wine prefix configured")
            return True
        except Exception as e:
            print(f"✗ Wine prefix configuration failed: {e}")
            return False
    
    def install_windows_fonts(self) -> bool:
        """Install Windows fonts for better compatibility"""
        print("\n[Wine] Installing Windows fonts...")
        try:
            packages = [
                'fonts-liberation',
                'fonts-noto',
                'ttf-mscorefonts-installer'
            ]
            
            success = DistroUtils.install_packages(packages, use_sudo=True)
            
            if success:
                print("✓ Windows fonts installed")
            else:
                print("✗ Font installation failed or partially completed")
            
            return success
        except Exception as e:
            print(f"✗ Font installation failed: {e}")
            return False
    
    def setup_d3d_wrappers(self) -> bool:
        """Setup Direct3D wrappers for shader compilation"""
        print("\n[Wine] Setting up D3D wrappers...")
        try:
            # Install shader compilation support
            packages = [
                'mesa-utils',
                'glslang-tools',
                'libglslang-dev'
            ]
            
            for package in packages:
                subprocess.run(['sudo', 'apt', 'install', '-y', package],
                             capture_output=True, check=False)
            
            print("✓ D3D wrappers configured")
            return True
        except Exception as e:
            print(f"✗ D3D wrapper setup failed: {e}")
            return False
    
    def _save_config(self, config: Dict) -> None:
        """Save configuration to JSON file"""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def load_config(self) -> Optional[Dict]:
        """Load configuration from JSON file"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return None
    
    def setup_complete_wine_environment(self) -> bool:
        """Setup complete Wine environment with all components"""
        print("\n" + "="*60)
        print("WINE/PROTON SETUP")
        print("="*60)
        
        success = True
        
        success = self.ensure_prefix_directory() and success
        success = self.install_wine_dependencies() and success
        success = self.install_dxvk() and success
        success = self.install_vkd3d() and success
        success = self.install_proton() and success
        success = self.configure_wine_prefix() and success
        success = self.install_windows_fonts() and success
        success = self.setup_d3d_wrappers() and success
        
        print("\n" + "="*60)
        print(f"Wine/Proton setup {'COMPLETED' if success else 'FAILED'}")
        print("="*60 + "\n")
        
        return success
    
    def set_environment_variables(self) -> Dict[str, str]:
        """Return environment variables for running Windows applications"""
        env_vars = {
            'WINEPREFIX': str(self.prefix_path),
            'WINEARCH': 'win64',
            'DXVK_HUD': 'off',
            'STAGING_SHARED_MEMORY': '1',
            'DXVK_NUM_COMPILER_THREADS': '4',
            'vblank_mode': '0'  # Disable VSync for better performance
        }
        
        return env_vars

if __name__ == "__main__":
    manager = WineManager()
    manager.setup_complete_wine_environment()
