#!/usr/bin/env python3
"""
Wine/Proton Launcher Utility
Launches Windows applications with proper Wine configuration
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def setup_environment(wine_prefix: str, app_config: dict = None) -> dict:
    """Setup environment variables for running applications"""
    env = os.environ.copy()
    
    env['WINEPREFIX'] = wine_prefix
    env['WINEARCH'] = 'win64'
    env['DXVK_HUD'] = 'off'
    env['STAGING_SHARED_MEMORY'] = '1'
    env['DXVK_NUM_COMPILER_THREADS'] = '4'
    env['vblank_mode'] = '0'
    
    # Additional settings from app config
    if app_config:
        env.update(app_config.get('environment_variables', {}))
    
    # Add Wine/Proton to PATH
    wine_dir = Path(wine_prefix) / 'proton'
    if wine_dir.exists():
        env['PATH'] = f"{wine_dir}:{env.get('PATH', '')}"
    
    return env

def launch_application(app_path: str, wine_prefix: str, args: list = None) -> int:
    """Launch a Windows application with Wine"""
    
    if not os.path.exists(app_path):
        print(f"✗ Application not found: {app_path}")
        return 1
    
    env = setup_environment(wine_prefix)
    
    cmd = ['wine', app_path]
    if args:
        cmd.extend(args)
    
    print(f"[Launch] Starting application: {os.path.basename(app_path)}")
    print(f"[Launch] Wine Prefix: {wine_prefix}")
    
    try:
        result = subprocess.run(cmd, env=env)
        return result.returncode
    except Exception as e:
        print(f"✗ Failed to launch application: {e}")
        return 1

def launch_with_proton(app_path: str, wine_prefix: str, args: list = None) -> int:
    """Launch a Windows application with Proton"""
    
    proton_dir = Path(wine_prefix) / 'proton'
    proton_binary = proton_dir / 'Proton' / 'proton'
    
    if not proton_binary.exists():
        print(f"✗ Proton not found in {proton_dir}")
        return 1
    
    env = setup_environment(wine_prefix)
    
    cmd = [str(proton_binary), app_path]
    if args:
        cmd.extend(args)
    
    print(f"[Launch] Starting application with Proton: {os.path.basename(app_path)}")
    print(f"[Launch] Wine Prefix: {wine_prefix}")
    
    try:
        result = subprocess.run(cmd, env=env)
        return result.returncode
    except Exception as e:
        print(f"✗ Failed to launch application with Proton: {e}")
        return 1

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Wine/Proton launcher for Windows applications'
    )
    
    parser.add_argument('application', help='Path to Windows application executable')
    parser.add_argument('--prefix', default=os.path.expanduser("~/.winpatable"),
                       help='Wine prefix directory')
    parser.add_argument('--proton', action='store_true',
                       help='Use Proton instead of Wine')
    parser.add_argument('--args', help='Arguments to pass to application')
    
    args = parser.parse_args()
    
    app_args = args.args.split() if args.args else None
    
    if args.proton:
        return launch_with_proton(args.application, args.prefix, app_args)
    else:
        return launch_application(args.application, args.prefix, app_args)

if __name__ == "__main__":
    sys.exit(main())
