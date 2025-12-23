#!/usr/bin/env python3
"""
Winpatable Interactive Setup Wizard
User-friendly step-by-step setup for first-time users
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.system_info import SystemDetector
from src.gpu.gpu_manager import GPUDriverManager
from src.wine.wine_manager import WineManager

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_step(number: int, title: str):
    """Print step header"""
    print(f"\n{Colors.CYAN}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}Step {number}: {title}{Colors.END}")
    print(f"{Colors.CYAN}{'='*60}{Colors.END}\n")

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

def prompt_yes_no(question: str) -> bool:
    """Ask yes/no question"""
    while True:
        response = input(f"\n{Colors.YELLOW}{question} (yes/no/skip){Colors.END}: ").lower().strip()
        if response in ['yes', 'y']:
            return True
        elif response in ['no', 'n', 'skip']:
            return False
        print_warning("Please answer 'yes' or 'no'")

def welcome_screen():
    """Show welcome screen"""
    print(f"\n{Colors.BOLD}")
    print("╔" + "═"*58 + "╗")
    print("║" + " "*58 + "║")
    print("║  WINPATABLE - Interactive Setup Wizard".center(58) + "║")
    print("║  Windows Apps on Linux Made Easy".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "═"*58 + "╝")
    print(f"{Colors.END}\n")
    
    print_info("This wizard will guide you through setting up Winpatable")
    print_info("It takes about 15-30 minutes depending on your internet")
    
    if not prompt_yes_no("Ready to get started?"):
        print_warning("Setup cancelled")
        sys.exit(0)

def step_1_welcome():
    """Step 1: Welcome and overview"""
    print_step(1, "Welcome to Winpatable")
    
    print("Winpatable lets you run Windows applications on Linux with:")
    print("  • {0}Full GPU acceleration{1}".format(Colors.GREEN, Colors.END))
    print("  • {0}Near-native performance{1}".format(Colors.GREEN, Colors.END))
    print("  • {0}Easy one-click installation{1}".format(Colors.GREEN, Colors.END))
    print()
    print_info("Supported applications:")
    print("  • Adobe Premiere Pro (video editing)")
    print("  • Sony Vegas Pro (audio/video)")
    print("  • Autodesk 3DS Max (3D modeling)")
    print("  • Microsoft Office (productivity)")
    print()
    
    input(f"{Colors.YELLOW}Press Enter to continue...{Colors.END}")

def step_2_system_check():
    """Step 2: Check system compatibility"""
    print_step(2, "Checking Your System")
    
    print_info("Detecting system hardware...")
    detector = SystemDetector()
    info = detector.detect_all()
    
    print()
    print("System Information:")
    print(f"  • OS: {info.os_type.value.replace('_', ' ').title()} {info.os_version}")
    print(f"  • CPU: {info.cpu.model}")
    print(f"  • CPU Cores: {info.cpu.cores}")
    print(f"  • RAM: {info.memory_gb:.1f} GB")
    print(f"  • Kernel: {info.kernel_version}")
    print()
    
    # Check compatibility
    checks = {
        "OS Support": info.os_type.value != "unknown",
        "CPU Architecture (x64)": info.is_x64,
        "CPU Vendor (Intel/AMD)": info.cpu.is_supported,
        "Minimum RAM (4GB)": info.memory_gb >= 4.0,
    }
    
    print("Compatibility Check:")
    all_passed = True
    for check, status in checks.items():
        symbol = "✓" if status else "✗"
        color = Colors.GREEN if status else Colors.RED
        print(f"  {color}{symbol}{Colors.END} {check}")
        if not status:
            all_passed = False
    
    print()
    if all_passed:
        print_success("Your system is compatible!")
    else:
        print_error("Some compatibility issues found")
        print_warning("You may still proceed, but some features may not work")
    
    # Show GPU info
    print()
    print("GPU Information:")
    if info.gpus and info.gpus[0].type.value != "unknown":
        for gpu in info.gpus:
            print(f"  • {gpu.name} ({gpu.type.value.upper()})")
            if gpu.driver_version:
                print(f"    Driver: {gpu.driver_version}")
    else:
        print_info("No GPU detected (using integrated graphics)")
    
    input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")
    return info

def step_3_disk_space():
    """Step 3: Check disk space"""
    print_step(3, "Disk Space Requirements")
    
    home_path = Path.home()
    stat = os.statvfs(str(home_path))
    free_gb = (stat.f_bavail * stat.f_frsize) / (1024**3)
    
    required_gb = 30
    
    print(f"Free space in home directory: {Colors.YELLOW}{free_gb:.1f} GB{Colors.END}")
    print(f"Required space: {Colors.YELLOW}{required_gb} GB{Colors.END}")
    print()
    
    if free_gb < required_gb:
        print_error(f"Only {free_gb:.1f} GB available, need {required_gb} GB")
        print_warning("You may not have enough space")
        if not prompt_yes_no("Continue anyway?"):
            print_error("Setup cancelled due to insufficient disk space")
            sys.exit(1)
    else:
        print_success(f"Sufficient disk space available ({free_gb:.1f} GB)")
    
    input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")

def step_4_gpu_setup(info):
    """Step 4: GPU driver setup"""
    print_step(4, "GPU Driver Installation")
    
    has_nvidia = any(gpu.type.value == "nvidia" for gpu in info.gpus)
    has_amd = any(gpu.type.value == "amd" for gpu in info.gpus)
    has_intel = any(gpu.type.value == "intel" for gpu in info.gpus)
    
    if has_nvidia or has_amd or has_intel:
        print_info("Detected compatible GPU:")
        if has_nvidia:
            print("  • NVIDIA GPU found")
            print_info("NVIDIA drivers will enable CUDA acceleration")
        if has_amd:
            print("  • AMD GPU found")
            print_info("AMD drivers will enable ROCm acceleration")
        if has_intel:
            print("  • Intel GPU found")
            print_info("Intel drivers will enable GPU acceleration")
        
        print()
        if prompt_yes_no("Install GPU drivers now?"):
            print_info("Installing GPU drivers (this may take 10-20 minutes)...")
            manager = GPUDriverManager(use_sudo=True)
            gpu_types = [gpu.type for gpu in info.gpus]
            if manager.install_all_gpu_drivers(gpu_types):
                print_success("GPU drivers installed")
            else:
                print_warning("GPU driver installation had issues")
                print_info("You can still use integrated graphics or CPU rendering")
        else:
            print_info("Skipping GPU driver installation")
            print_warning("GPU acceleration will not be available")
    else:
        print_warning("No compatible GPU detected")
        print_info("You can still run applications using integrated graphics")
    
    input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")

def step_5_wine_setup():
    """Step 5: Wine/Proton setup"""
    print_step(5, "Setting Up Wine Environment")
    
    print_info("This will install:")
    print("  • Wine (Windows compatibility layer)")
    print("  • Proton (enhanced version)")
    print("  • DXVK (graphics support)")
    print("  • Required libraries")
    print()
    
    print_warning("This step takes 10-30 minutes")
    
    if prompt_yes_no("Continue with Wine setup?"):
        print_info("Setting up Wine environment...")
        
        wine_prefix = os.path.expanduser("~/.winpatable")
        manager = WineManager(wine_prefix)
        
        if manager.setup_complete_wine_environment():
            print_success("Wine environment configured successfully")
        else:
            print_error("Wine setup encountered issues")
            print_info("Try running: winpatable setup-wine")
    else:
        print_warning("Wine setup skipped")
        print_error("You cannot run applications without Wine")
    
    input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")

def step_6_test_installation():
    """Step 6: Test installation"""
    print_step(6, "Verifying Installation")
    
    checks = []
    
    # Check Wine
    try:
        import subprocess
        subprocess.run(['wine', '--version'], capture_output=True, check=True)
        checks.append(("Wine installed", True))
    except:
        checks.append(("Wine installed", False))
    
    # Check winetricks
    try:
        subprocess.run(['which', 'winetricks'], capture_output=True, check=True)
        checks.append(("Winetricks available", True))
    except:
        checks.append(("Winetricks available", False))
    
    # Check wine prefix
    wine_prefix = Path.home() / ".winpatable"
    checks.append(("Wine prefix created", wine_prefix.exists()))
    
    print("Verification Results:")
    all_passed = True
    for check_name, status in checks:
        symbol = "✓" if status else "✗"
        color = Colors.GREEN if status else Colors.RED
        print(f"  {color}{symbol}{Colors.END} {check_name}")
        if not status:
            all_passed = False
    
    print()
    if all_passed:
        print_success("All checks passed!")
    else:
        print_warning("Some issues detected, but you may still proceed")
    
    input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")

def step_7_completion():
    """Step 7: Completion and next steps"""
    print_step(7, "Setup Complete!")
    
    print_success("Winpatable is ready to use!")
    print()
    
    print(f"{Colors.BOLD}Next Steps:{Colors.END}")
    print()
    print("1. Install an application:")
    print(f"   {Colors.YELLOW}winpatable install-app office --installer ~/Downloads/office.exe{Colors.END}")
    print()
    print("2. View available commands:")
    print(f"   {Colors.YELLOW}winpatable --help{Colors.END}")
    print()
    print("3. See installed applications:")
    print(f"   {Colors.YELLOW}winpatable list-apps{Colors.END}")
    print()
    print("4. Get performance tips:")
    print(f"   {Colors.YELLOW}winpatable performance-tuning{Colors.END}")
    print()
    
    print(f"{Colors.BOLD}Supported Applications:{Colors.END}")
    print("  • Microsoft Office")
    print("  • Adobe Premiere Pro")
    print("  • Sony Vegas Pro")
    print("  • Autodesk 3DS Max")
    print()
    
    print(f"{Colors.BOLD}Documentation:{Colors.END}")
    print("  • README.md - Overview and features")
    print("  • QUICK_START.md - Fast reference")
    print("  • docs/APPLICATION_GUIDES.md - App-specific setup")
    print("  • docs/GPU_GUIDE.md - GPU configuration")
    print()

def main():
    """Run the wizard"""
    try:
        welcome_screen()
        step_1_welcome()
        info = step_2_system_check()
        step_3_disk_space()
        step_4_gpu_setup(info)
        step_5_wine_setup()
        step_6_test_installation()
        step_7_completion()
        
        print(f"\n{Colors.BOLD}{Colors.GREEN}Thank you for using Winpatable!{Colors.END}\n")
        
    except KeyboardInterrupt:
        print_error("\nSetup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
