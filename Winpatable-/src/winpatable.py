#!/usr/bin/env python3
"""
Winpatable - Windows Compatibility Layer for Linux
Main CLI Interface for managing Windows application compatibility
"""

import argparse
import sys
import os
from pathlib import Path
from typing import Optional
import time

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.system_info import SystemDetector, print_system_info
from src.gpu.gpu_manager import GPUDriverManager
from src.wine.wine_manager import WineManager
from src.installers.app_installers import ApplicationManager

# ANSI Colors
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_color(text: str, color: str = Colors.BLUE):
    """Print colored text"""
    print(f"{color}{text}{Colors.END}")

def print_success(text: str):
    """Print success message"""
    print(f"{Colors.GREEN}✓{Colors.END} {text}")

def print_error(text: str):
    """Print error message"""
    print(f"{Colors.RED}✗{Colors.END} {text}")

def print_warning(text: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠{Colors.END} {text}")

def print_info(text: str):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ{Colors.END} {text}")

def progress_bar(iteration: int, total: int, prefix: str = '', length: int = 40):
    """Display progress bar"""
    percent = 100 * (iteration / float(total))
    filled = int(length * iteration // total)
    bar = '█' * filled + '░' * (length - filled)
    print(f'\r{prefix} |{bar}| {percent:.1f}%', end='')
    if iteration == total:
        print()

class WinpatableUI:
    """Main CLI interface for Winpatable"""
    
    def __init__(self):
        self.detector = SystemDetector()
        self.system_info = None
        self.wine_manager = None
        self.gpu_manager = None
        self.app_manager = None
    
    def print_banner(self):
        """Print welcome banner"""
        banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║          WINPATABLE - Windows Compatibility Layer        ║
║              For Linux Mint & Ubuntu                      ║
║                                                           ║
║  Professional Applications Support:                      ║
║    • Adobe Premiere Pro                                  ║
║    • Sony Vegas Pro                                      ║
║    • Autodesk 3DS Max                                    ║
║    • Microsoft Office                                    ║
║                                                           ║
║  GPU Support:                                            ║
║    • NVIDIA (GTX/RTX series)                            ║
║    • AMD (RADEON series)                                ║
║    • Intel (UHD/ARC series)                             ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
        """
        print(banner)
        """Detect system hardware and software"""
        print("\n[System] Detecting system information...")
        self.system_info = self.detector.detect_all()
        print_system_info(self.system_info)
        
        # Check compatibility
        self._check_compatibility()
    
    def _check_compatibility(self):
        """Check system compatibility"""
        print("\n" + "="*60)
        print("COMPATIBILITY CHECK")
        print("="*60)
        
        checks = {
            "OS Support": self.system_info.os_type.value != "unknown",
            "CPU Architecture": self.system_info.is_x64,
            "CPU Vendor": self.system_info.cpu.is_supported,
            "GPU Support": any(gpu.is_supported for gpu in self.system_info.gpus),
            "Memory": self.system_info.memory_gb >= 4.0
        }
        
        all_compatible = True
        for check, status in checks.items():
            symbol = "✓" if status else "✗"
            print(f"{symbol} {check}: {'Yes' if status else 'No'}")
            if not status:
                all_compatible = False
        
        print("="*60)
        
        if all_compatible:
            print("\n✓ System is compatible with Winpatable!")
        else:
            print("\n✗ System has compatibility issues")
            print("  Some features may not work as expected")
    
    def cmd_install_gpu_drivers(self, args):
        """Install GPU drivers"""
        if self.system_info is None:
            self.cmd_detect(None)
        
        self.gpu_manager = GPUDriverManager(use_sudo=True)
        gpu_types = [gpu.type for gpu in self.system_info.gpus]
        self.gpu_manager.install_all_gpu_drivers(gpu_types)
    
    def cmd_setup_wine(self, args):
        """Setup Wine/Proton environment"""
        print("\n[Setup] Configuring Wine/Proton environment...")
        
        prefix = args.prefix or os.path.expanduser("~/.winpatable")
        self.wine_manager = WineManager(prefix)
        self.wine_manager.setup_complete_wine_environment()
    
    def cmd_install_app(self, args):
        """Install Windows application"""
        if args.app not in ['premiere', 'vegas', '3dsmax', 'office']:
            print(f"✗ Unknown application: {args.app}")
            print("  Supported: premiere, vegas, 3dsmax, office")
            return
        
        prefix = args.prefix or os.path.expanduser("~/.winpatable")
        self.app_manager = ApplicationManager(prefix)
        
        installer = self.app_manager.get_installer(args.app)
        if installer:
            if args.installer:
                installer.install(args.installer)
            else:
                print(f"Note: Please provide installer path with --installer")
                print(f"Usage: winpatable install-app {args.app} --installer <path>")
    
    def cmd_list_apps(self, args):
        """List supported applications"""
        prefix = os.path.expanduser("~/.winpatable")
        self.app_manager = ApplicationManager(prefix)
        
        print("\n" + "="*60)
        print("SUPPORTED APPLICATIONS")
        print("="*60)
        
        for app_key, app_info in self.app_manager.list_applications().items():
            print(f"\n{app_info['name']} ({app_key}):")
            print(f"  Minimum RAM: {app_info['minimum_ram_gb']}GB")
            print(f"  GPU Required: {'Yes' if app_info['gpu_required'] else 'No'}")
            print(f"  Notes: {app_info['notes']}")
        print("="*60)
    
    def cmd_quick_start(self, args):
        """Quick setup for all components"""
        print_color("\n" + "="*60)
        print_color("QUICK START - FULL INSTALLATION", Colors.BOLD)
        print_color("="*60 + "\n")
        
        print_info("This will set up Winpatable for you automatically")
        print_info("It will take 10-30 minutes depending on your system")
        
        response = input(f"\n{Colors.YELLOW}Continue with installation? (yes/no){Colors.END} ").lower()
        if response not in ['yes', 'y']:
            print_warning("Installation cancelled")
            return
        
        # Step 1: Detect system
        print_color("\n[1/4] Detecting system information...", Colors.CYAN)
        self.cmd_detect(None)
        
        # Step 2: GPU drivers
        has_gpu = any(gpu.is_supported for gpu in self.system_info.gpus)
        if has_gpu:
            print_color("\n[2/4] Installing GPU drivers...", Colors.CYAN)
            response = input(f"{Colors.YELLOW}Install GPU drivers? (yes/no){Colors.END} ").lower()
            if response in ['yes', 'y']:
                self.cmd_install_gpu_drivers(None)
            else:
                print_info("Skipping GPU driver installation")
        else:
            print_warning("[2/4] No compatible GPU detected, skipping GPU setup")
        
        # Step 3: Wine setup
        print_color("\n[3/4] Setting up Wine/Proton...", Colors.CYAN)
        prefix = args.prefix or os.path.expanduser("~/.winpatable")
        args.prefix = prefix
        self.cmd_setup_wine(args)
        
        # Completion
        print_color("\n[4/4] Installation complete!", Colors.GREEN)
        print_color("\n" + "="*60)
        print_color("SETUP COMPLETE", Colors.BOLD)
        print_color("="*60)
        
        print_color("\nYou can now install applications:", Colors.BLUE)
        print(f"\n{Colors.YELLOW}winpatable install-app <app> --installer <path>{Colors.END}")
        print(f"\nSupported applications:")
        print(f"  • {Colors.YELLOW}premiere{Colors.END}   - Adobe Premiere Pro")
        print(f"  • {Colors.YELLOW}vegas{Colors.END}      - Sony Vegas Pro")
        print(f"  • {Colors.YELLOW}3dsmax{Colors.END}     - Autodesk 3DS Max")
        print(f"  • {Colors.YELLOW}office{Colors.END}     - Microsoft Office")
        
        print(f"\nExample:")
        print(f"  {Colors.YELLOW}winpatable install-app office --installer ~/Downloads/Office.exe{Colors.END}")
        
        print_color("\nNeed help?", Colors.BLUE)
        print(f"  • View all commands: {Colors.YELLOW}winpatable --help{Colors.END}")
        print(f"  • List applications: {Colors.YELLOW}winpatable list-apps{Colors.END}")
        print(f"  • Performance tips: {Colors.YELLOW}winpatable performance-tuning{Colors.END}")
        print_color("="*60 + "\n", Colors.BOLD)
    
    def cmd_performance_tuning(self, args):
        """Show performance tuning recommendations"""
        print("\n" + "="*60)
        print("PERFORMANCE TUNING GUIDE")
        print("="*60)
        
        recommendations = {
            "GPU Optimization": [
                "Enable hardware acceleration in application settings",
                "Update GPU drivers to latest version",
                "Disable VSync for maximum performance",
                "Use dedicated GPU instead of integrated graphics"
            ],
            "Wine/Proton Settings": [
                "Enable DXVK (Direct3D to Vulkan translation)",
                "Enable VKD3D for DirectX 12 support",
                "Increase shader cache size",
                "Use Proton-GE for better compatibility"
            ],
            "System Optimization": [
                "Allocate maximum RAM to application",
                "Disable desktop effects/compositing",
                "Close unnecessary background applications",
                "Use SSD for project files"
            ],
            "Network": [
                "Use wired connection for streaming/collaboration",
                "Disable VPN if possible for local work",
                "Close bandwidth-heavy applications"
            ]
        }
        
        for category, tips in recommendations.items():
            print(f"\n{category}:")
            for i, tip in enumerate(tips, 1):
                print(f"  {i}. {tip}")
        
        print("\n" + "="*60 + "\n")
    
    def run(self):
        """Main entry point"""
        parser = argparse.ArgumentParser(
            description='Winpatable - Windows Compatibility Layer for Linux',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Detect system hardware
  winpatable detect
  
  # Quick setup everything
  winpatable quick-start
  
  # Install GPU drivers
  winpatable install-gpu-drivers
  
  # Setup Wine environment
  winpatable setup-wine
  
  # Install application
  winpatable install-app premiere --installer /path/to/installer.exe
  
  # List supported applications
  winpatable list-apps
  
  # Get performance tuning tips
  winpatable performance-tuning
            """
        )
        
        parser.add_argument('-v', '--version', action='version', 
                          version='Winpatable 1.0.0')
        
        subparsers = parser.add_subparsers(dest='command', help='Commands')
        
        # Detect command
        subparsers.add_parser('detect', help='Detect system hardware and software')
        
        # GPU drivers command
        subparsers.add_parser('install-gpu-drivers', help='Install GPU drivers')
        
        # Setup Wine command
        setup_parser = subparsers.add_parser('setup-wine', help='Setup Wine/Proton environment')
        setup_parser.add_argument('--prefix', help='Wine prefix directory (default: ~/.winpatable)')
        
        # Install app command
        app_parser = subparsers.add_parser('install-app', help='Install Windows application')
        app_parser.add_argument('app', choices=['premiere', 'vegas', '3dsmax', 'office'],
                               help='Application to install')
        app_parser.add_argument('--installer', help='Path to application installer')
        app_parser.add_argument('--prefix', help='Wine prefix directory (default: ~/.winpatable)')
        
        # List apps command
        subparsers.add_parser('list-apps', help='List supported applications')
        
        # Quick start command
        quick_parser = subparsers.add_parser('quick-start', 
                                            help='Quick setup for all components')
        quick_parser.add_argument('--prefix', help='Wine prefix directory (default: ~/.winpatable)')
        
        # Performance tuning command
        subparsers.add_parser('performance-tuning', help='Show performance tuning recommendations')
        
        args = parser.parse_args()
        
        self.print_banner()
        
        if not args.command:
            parser.print_help()
            return
        
        # Route commands
        command_map = {
            'detect': self.cmd_detect,
            'install-gpu-drivers': self.cmd_install_gpu_drivers,
            'setup-wine': self.cmd_setup_wine,
            'install-app': self.cmd_install_app,
            'list-apps': self.cmd_list_apps,
            'quick-start': self.cmd_quick_start,
            'performance-tuning': self.cmd_performance_tuning
        }
        
        if args.command in command_map:
            command_map[args.command](args)
        else:
            print(f"Unknown command: {args.command}")
            parser.print_help()

def main():
    """Main entry point"""
    try:
        ui = WinpatableUI()
        ui.run()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
