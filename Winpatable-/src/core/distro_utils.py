#!/usr/bin/env python3
"""
Distribution utilities for consistent distro and package manager detection.
Supports Ubuntu, Linux Mint, and other Debian-based systems.
"""

import os
import subprocess
from typing import Tuple, Optional

class DistroUtils:
    """Utilities for distro and package manager detection"""
    
    @staticmethod
    def get_os_release() -> dict:
        """Parse /etc/os-release into a dictionary"""
        data = {}
        try:
            with open('/etc/os-release', 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or '=' not in line:
                        continue
                    key, value = line.split('=', 1)
                    # Strip quotes and extra whitespace
                    value = value.strip().strip('"').strip("'")
                    data[key] = value
        except FileNotFoundError:
            pass
        return data
    
    @staticmethod
    def is_debian_based() -> bool:
        """Check if system is Debian-based (Ubuntu, Mint, Debian, etc.)"""
        data = DistroUtils.get_os_release()
        os_id = data.get('ID', '').lower()
        id_like = data.get('ID_LIKE', '').lower()
        
        # Check ID field and ID_LIKE field for Debian ancestry
        debian_indicators = ['debian', 'ubuntu', 'linuxmint', 'mint']
        return any(indicator in os_id for indicator in debian_indicators) or \
               any(indicator in id_like for indicator in debian_indicators)
    
    @staticmethod
    def get_distro_name() -> str:
        """Get normalized distro name (ubuntu, linuxmint, debian, etc.)"""
        data = DistroUtils.get_os_release()
        os_id = data.get('ID', 'unknown').lower()
        
        # Normalize mint variants
        if 'mint' in os_id:
            return 'linuxmint'
        return os_id
    
    @staticmethod
    def get_package_manager() -> Tuple[str, str]:
        """
        Detect and return package manager command.
        Returns: (manager_name, manager_executable)
        Examples: ('apt', 'apt'), ('apt-get', 'apt-get')
        """
        managers = {
            'apt': '/usr/bin/apt',
            'apt-get': '/usr/bin/apt-get',
        }
        
        # Prefer apt over apt-get on Debian-based systems
        for name, path in managers.items():
            if os.path.exists(path) and os.access(path, os.X_OK):
                return name, name
        
        # Last resort: try to find via which command
        for name in ['apt', 'apt-get']:
            try:
                result = subprocess.run(['which', name], capture_output=True, text=True, check=False)
                if result.returncode == 0:
                    return name, name
            except (FileNotFoundError, subprocess.SubprocessError):
                pass
        
        # Default fallback
        return 'apt', 'apt'
    
    @staticmethod
    def run_package_manager(cmd: list, use_sudo: bool = True, check: bool = False) -> Tuple[int, str, str]:
        """
        Run a package manager command with optional sudo.
        Returns: (returncode, stdout, stderr)
        """
        pkg_mgr, _ = DistroUtils.get_package_manager()
        
        # Build the full command
        if cmd[0] != pkg_mgr:
            cmd = [pkg_mgr] + cmd
        
        if use_sudo and os.geteuid() != 0:
            cmd = ['sudo'] + cmd
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=check)
            return result.returncode, result.stdout, result.stderr
        except subprocess.CalledProcessError as e:
            return e.returncode, e.stdout, e.stderr
        except Exception as e:
            return 1, '', str(e)
    
    @staticmethod
    def install_packages(packages: list, use_sudo: bool = True) -> bool:
        """Install a list of packages, handling Debian/Ubuntu/Mint differences"""
        if not packages:
            return True
        
        pkg_mgr, _ = DistroUtils.get_package_manager()
        
        # Build install command
        cmd = [pkg_mgr, 'install', '-y'] + packages
        
        if use_sudo and os.geteuid() != 0:
            cmd = ['sudo'] + cmd
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0
        except Exception as e:
            print(f"✗ Package installation failed: {e}")
            return False
