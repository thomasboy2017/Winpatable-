#!/usr/bin/env python3
"""
Winpatable - Windows Compatibility Layer for Linux
Main CLI Interface for managing Windows application compatibility
"""

import argparse
import sys
import os
import webbrowser
from pathlib import Path
from typing import Optional
import time
import platform
import getpass
import json
from urllib.parse import quote as urllib_request_quote

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.system_info import SystemDetector, print_system_info
from src.gpu.gpu_manager import GPUDriverManager
from src.wine.wine_manager import WineManager
from src.installers.app_installers import ApplicationManager
from src.core.updater import auto_update, UpdateChecker
from src.core.ai_assistant import WinpatableAI, ai_analyze_app
from src.core.performance import ConfigurationProfile, PerformanceBenchmark, PerformanceCache
from src.core.security import SecurityAuditor, MalwareDetector, CodeSigner
import stat

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
        
        # If simple mode, run with defaults
        if getattr(args, 'simple', False):
            print_info("Running quick-start in simple mode (defaults will be applied)")
            response = 'yes'
        else:
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
            if getattr(args, 'simple', False):
                response = 'yes'
            else:
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
    
    def cmd_update(self, args):
        """Check for and install updates"""
        print_color("\n" + "="*60)
        print_color("WINPATABLE UPDATE CLIENT", Colors.BOLD)
        print_color("="*60 + "\n")
        success = auto_update(check_only=args.check_only, verbose=True, mode=getattr(args, 'mode', 'auto'), force=getattr(args, 'force', False))
        
        if not success:
            print_error("Update check failed or was cancelled")
            return
        
        print_color("="*60 + "\n", Colors.BOLD)
    
    def cmd_ai(self, args):
        """AI Assistant command handler"""
        ai = WinpatableAI()
        
        if not hasattr(args, 'ai_command') or not args.ai_command:
            print_color("\n" + "="*70)
            print_color("WINPATABLE AI ASSISTANT", Colors.BOLD)
            print_color("="*70 + "\n")
            print("Available commands:")
            print("  ai list       - List all apps with AI compatibility scores")
            print("  ai analyze    - Analyze compatibility of a specific app")
            print("  ai recommend  - Get recommendations for your system")
            print_color("="*70 + "\n", Colors.BOLD)
            return
        
        if args.ai_command == 'list':
            print_color("\n" + "="*70)
            print_color("WINPATABLE AI - APPLICATION COMPATIBILITY ANALYSIS", Colors.BOLD)
            print_color("="*70 + "\n")
            
            recommendations = ai.get_all_recommendations()
            sorted_apps = sorted(
                recommendations.items(),
                key=lambda x: x[1].compatibility_score,
                reverse=True
            )
            
            for app_key, rec in sorted_apps:
                score = rec.compatibility_score * 100
                score_color = "🟢" if score >= 90 else \
                              "🟡" if score >= 80 else \
                              "🟠" if score >= 60 else "🔴"
                print(f"{score_color} {rec.app_name:25s} | {score:5.0f}% | {rec.estimated_performance:10s}")
            
            print("\n🟢 Excellent (90-100%) | 🟡 Good (80-89%) | 🟠 Moderate (60-79%) | 🔴 Limited (0-59%)")
            print_color("="*70 + "\n", Colors.BOLD)
        
        elif args.ai_command == 'analyze':
            app_name = args.app
            print(ai.analyze_compatibility(app_name))
        
        elif args.ai_command == 'recommend':
            print_color("\n" + "="*70)
            print_color("WINPATABLE AI - PERSONALIZED RECOMMENDATIONS", Colors.BOLD)
            print_color("="*70 + "\n")
            
            if self.system_info:
                print_info(f"GPU: {self.system_info.get('gpu', {}).get('name', 'Unknown')}")
                print_info(f"CPU: {self.system_info.get('cpu', {}).get('model', 'Unknown')}")
                print_info(f"RAM: {self.system_info.get('memory_gb', 0)}GB")
                print_info(f"OS: {self.system_info.get('os', 'Unknown')}")
                
                print("\nBased on your system, here are the recommended applications:")
                print("(Applications with highest compatibility scores)\n")
                
                recommendations = ai.get_all_recommendations()
                sorted_apps = sorted(
                    recommendations.items(),
                    key=lambda x: x[1].compatibility_score,
                    reverse=True
                )
                
                count = 0
                for app_key, rec in sorted_apps:
                    if count >= 15:
                        break
                    score = rec.compatibility_score * 100
                    if score >= 70:
                        print(f"✓ {rec.app_name:25s} ({score:.0f}%) - {rec.estimated_performance}")
                        count += 1
            
            print_color("\n" + "="*70 + "\n", Colors.BOLD)
    
    def cmd_profile(self, args):
        """Configuration profile command handler"""
        
        if not hasattr(args, 'profile_command') or not args.profile_command:
            print_color("\n" + "="*70)
            print_color("WINPATABLE CONFIGURATION PROFILES", Colors.BOLD)
            print_color("="*70 + "\n")
            
            profiles = ConfigurationProfile.list_profiles()
            print("Available profiles:\n")
            
            for name, info in profiles.items():
                print(f"  {name.upper()}")
                print(f"    {info['description']}")
                print(f"    Recommended apps: {info['apps']}\n")
            
            print("Usage: winpatable profile list")
            print("       winpatable profile apply <profile_name>\n")
            print_color("="*70 + "\n", Colors.BOLD)
            return
        
        if args.profile_command == 'list':
            print_color("\n" + "="*70)
            print_color("WINPATABLE CONFIGURATION PROFILES", Colors.BOLD)
            print_color("="*70 + "\n")
            
            profiles = ConfigurationProfile.list_profiles()
            
            for name, info in profiles.items():
                print(f"📋 {name.upper()}")
                print(f"   Description: {info['description']}")
                print(f"   Recommended applications: {info['apps']}\n")
            
            print_color("="*70 + "\n", Colors.BOLD)
        
        elif args.profile_command == 'apply':
            profile_name = args.name
            print_color("\n" + "="*70)
            print_color(f"APPLYING PROFILE: {profile_name.upper()}", Colors.BOLD)
            print_color("="*70)
            
            success = ConfigurationProfile.apply_profile(profile_name)
            
            if success:
                print_success(f"Profile '{profile_name}' configuration loaded")
                print("\nYou can now install recommended applications using:")
                print(f"  winpatable install-app <app_name>\n")
            else:
                print_error(f"Profile '{profile_name}' not found")
            
            print_color("="*70 + "\n", Colors.BOLD)
    
    def cmd_security(self, args):
        """Security audit and malware scanning command"""
        
        if not hasattr(args, 'security_command') or not args.security_command:
            print_color("\n" + "="*70)
            print_color("WINPATABLE SECURITY", Colors.BOLD)
            print_color("="*70 + "\n")
            
            print("Available commands:\n")
            print("  security audit         - Run comprehensive security audit")
            print("  security scan <path>   - Scan directory for malware")
            print("  security install-clamav - Install ClamAV antivirus\n")
            print_color("="*70 + "\n", Colors.BOLD)
            return
        
        if args.security_command == 'audit':
            print_color("\n" + "="*70)
            print_color("SECURITY AUDIT", Colors.BOLD)
            print_color("="*70 + "\n")
            print("Running comprehensive security checks...\n")
            
            auditor = SecurityAuditor()
            checks = auditor.run_all_checks()
            auditor.print_report()
        
        elif args.security_command == 'scan':
            path = args.path
            print_color("\n" + "="*70)
            print_color(f"MALWARE SCAN: {path}", Colors.BOLD)
            print_color("="*70 + "\n")
            
            detector = MalwareDetector()
            
            if not detector.clamav_available:
                print_warning("ClamAV not installed. Install with:")
                print("  winpatable security install-clamav\n")
                return
            
            print(f"Scanning {path}...\n")
            results = detector.scan_directory(path)
            
            if results:
                print_error(f"Found {len(results)} potential threats:\n")
                for filepath, (clean, msg) in results.items():
                    print(f"  ✗ {filepath}")
                    print(f"    {msg}\n")
            else:
                print_success("No threats detected!")
            
            print_color("="*70 + "\n", Colors.BOLD)
        
        elif args.security_command == 'install-clamav':
            print_color("\n" + "="*70)
            print_color("INSTALLING CLAMAV", Colors.BOLD)
            print_color("="*70 + "\n")
            
            detector = MalwareDetector()
            print("Installing ClamAV antivirus...")
            
            if detector.install_clamav():
                print_success("ClamAV installed successfully!")
                print("\nUpdate virus definitions with:")
                print("  sudo freshclam\n")
            else:
                print_error("Failed to install ClamAV")
            
            print_color("="*70 + "\n", Colors.BOLD)

    def cmd_auth(self, args):
        """Authentication helpers (GitHub token storage)"""
        if not hasattr(args, 'auth_command') or args.auth_command != 'github':
            print("Usage: winpatable auth github --set-token [TOKEN]")
            return

        token_arg = args.set_token
        token_path = Path.home() / '.winpatable' / 'github_token'
        os.makedirs(token_path.parent, exist_ok=True)

        if token_arg is True:
            # interactive prompt
            if sys.stdin.isatty():
                token = input('Enter GitHub personal access token (will be stored locally, permission 600): ').strip()
            else:
                print_error('No token provided and not interactive')
                return
        else:
            token = token_arg

        if not token:
            print_error('Token is empty; aborting')
            return

        try:
            with open(token_path, 'w') as fh:
                fh.write(token.strip())
            os.chmod(token_path, stat.S_IRUSR | stat.S_IWUSR)
            print_success(f'GitHub token saved to {token_path} (mode 600)')
        except Exception as e:
            print_error(f'Failed to save token: {e}')

    def cmd_updater(self, args):
        """Manage updater systemd user timer"""
        cmd = getattr(args, 'updater_command', None)
        unit_dir = Path.home() / '.config' / 'systemd' / 'user'
        service_file = unit_dir / 'winpatable-update.service'
        timer_file = unit_dir / 'winpatable-update.timer'
        unit_dir.mkdir(parents=True, exist_ok=True)

        def write_unit():
            service = f"""[Unit]\nDescription=Winpatable Update Service\n\n[Service]\nType=oneshot\nExecStart={sys.executable} -m src.core.updater --check-only\n"""
            timer = f"""[Unit]\nDescription=Daily Winpatable Update Timer\n\n[Timer]\nOnCalendar=daily\nPersistent=true\n\n[Install]\nWantedBy=timers.target\n"""
            try:
                with open(service_file, 'w') as fh:
                    fh.write(service)
                with open(timer_file, 'w') as fh:
                    fh.write(timer)
                print_success(f'Wrote unit files to {unit_dir}')
                return True
            except Exception as e:
                print_error(f'Failed to write unit files: {e}')
                return False

        if cmd == 'enable-timer':
            ok = write_unit()
            if not ok:
                return
            # Try to enable via systemctl --user
            try:
                subprocess.run(['systemctl', '--user', 'daemon-reload'], check=True)
                subprocess.run(['systemctl', '--user', 'enable', '--now', 'winpatable-update.timer'], check=True)
                print_success('Enabled and started winpatable-update.timer (systemd user)')
            except Exception as e:
                print_warning(f'Could not enable systemd timer: {e}')
                print('If your system does not support systemd user services, you can run the updater daily via cron or a scheduler.')

        elif cmd == 'disable-timer':
            try:
                subprocess.run(['systemctl', '--user', 'disable', '--now', 'winpatable-update.timer'], check=True)
                print_success('Disabled winpatable-update.timer')
            except Exception as e:
                print_warning(f'Could not disable systemd timer: {e}')
            # remove unit files
            try:
                if service_file.exists():
                    service_file.unlink()
                if timer_file.exists():
                    timer_file.unlink()
                print_success('Removed unit files')
            except Exception:
                pass

        elif cmd == 'status':
            try:
                subprocess.run(['systemctl', '--user', 'status', 'winpatable-update.timer'])
            except Exception as e:
                print_warning(f'Could not query systemd timer status: {e}')
        else:
            print('Usage: winpatable updater [enable-timer|disable-timer|status]')
    
    def run(self):
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
        quick_parser.add_argument('--simple', action='store_true', help='Run quick-start with sensible defaults for everyday users')
        
        # Performance tuning command
        subparsers.add_parser('performance-tuning', help='Show performance tuning recommendations')
        
        # Update command
        update_parser = subparsers.add_parser('update', help='Check for and install updates')
        update_parser.add_argument('--check-only', action='store_true', help='Only check for updates, do not install')
        update_parser.add_argument('--force', action='store_true', help='Force update without asking for confirmation')
        update_parser.add_argument('--mode', choices=['auto', 'security', 'feature'], default='auto', help='Which update channel to check: weekly security or monthly feature (default: auto)')
        
        # AI Assistant command
        ai_parser = subparsers.add_parser('ai', help='AI assistant for app compatibility')
        ai_subparsers = ai_parser.add_subparsers(dest='ai_command', help='AI commands')
        ai_subparsers.add_parser('list', help='List all supported apps with AI scores')
        ai_analyze = ai_subparsers.add_parser('analyze', help='Analyze compatibility of an app')
        ai_analyze.add_argument('app', help='Application name to analyze')
        ai_subparsers.add_parser('recommend', help='Get AI recommendations for your system')
        
        # Profile command
        profile_parser = subparsers.add_parser('profile', help='Configuration profiles for different use cases')
        profile_subparsers = profile_parser.add_subparsers(dest='profile_command', help='Profile commands')
        profile_subparsers.add_parser('list', help='List available configuration profiles')
        profile_apply = profile_subparsers.add_parser('apply', help='Apply a configuration profile')
        profile_apply.add_argument('name', choices=['gaming', 'creative', 'business', 'development', 'audio'],
                                 help='Profile name to apply')
        
        # Security command
        security_parser = subparsers.add_parser('security', help='Security audit and malware scanning')
        security_subparsers = security_parser.add_subparsers(dest='security_command', help='Security commands')
        security_subparsers.add_parser('audit', help='Run comprehensive security audit')
        security_scan = security_subparsers.add_parser('scan', help='Scan for malware')
        security_scan.add_argument('path', nargs='?', default=str(Path.home() / '.winpatable'),
                                 help='Path to scan (default: ~/.winpatable)')
        security_subparsers.add_parser('install-clamav', help='Install ClamAV antivirus')

        # Report command (bug / feature)
        report_parser = subparsers.add_parser('report', help='Create a bug or feature report')
        report_subparsers = report_parser.add_subparsers(dest='report_command', help='Report commands')
        report_bug = report_subparsers.add_parser('bug', help='Report a bug')
        report_bug.add_argument('--title', help='Short title for the bug')
        report_bug.add_argument('--description', help='Detailed description / steps to reproduce')
        report_feature = report_subparsers.add_parser('feature', help='Request a feature')
        report_feature.add_argument('--title', help='Short title for the feature request')
        report_feature.add_argument('--description', help='Detailed description of the feature request')
        report_subparsers.add_parser('gui', help='Open a simple GUI to report bugs/features')

        # Auth command: store GitHub token securely
        auth_parser = subparsers.add_parser('auth', help='Authentication helpers')
        auth_sub = auth_parser.add_subparsers(dest='auth_command', help='Auth commands')
        gh = auth_sub.add_parser('github', help='GitHub token storage')
        gh.add_argument('--set-token', help='Set GitHub token (saves to ~/.winpatable/github_token)', nargs='?', const=True)

        # Updater service (systemd user timer)
        updater_parser = subparsers.add_parser('updater', help='Updater utilities (system timer)')
        updater_sub = updater_parser.add_subparsers(dest='updater_command', help='Updater commands')
        updater_sub.add_parser('enable-timer', help='Register systemd user timer to run winpatable update daily')
        updater_sub.add_parser('disable-timer', help='Disable the systemd user timer')
        updater_sub.add_parser('status', help='Show updater timer status (systemctl --user)')
        
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
            'performance-tuning': self.cmd_performance_tuning,
            'update': self.cmd_update,
            'report': self.cmd_report,
            'auth': self.cmd_auth,
            'updater': self.cmd_updater,
            'ai': self.cmd_ai,
            'profile': self.cmd_profile,
            'security': self.cmd_security
        }
        
        if args.command in command_map:
            command_map[args.command](args)
        else:
            print(f"Unknown command: {args.command}")
            parser.print_help()

    # GUI route handled by the main CLI; use the full cmd_report implementation below.

    def cmd_report(self, args):
        """Create a bug or feature report saved locally and optionally open GitHub issue URL"""
        rpt_type = getattr(args, 'report_command', None)
        if not rpt_type:
            print("Usage: winpatable report [bug|feature] --title 'Short title' --description 'Details'")
            return

        title = getattr(args, 'title', None)
        description = getattr(args, 'description', None)

        # Interactive prompts if missing
        if not title and sys.stdin.isatty():
            title = input("Enter a short title for the report: ").strip()
        if not description and sys.stdin.isatty():
            print("Enter a detailed description (end with an empty line):")
            lines = []
            while True:
                try:
                    line = input()
                except EOFError:
                    break
                if not line.strip():
                    break
                lines.append(line)
            description = '\n'.join(lines).strip()

        if not title:
            print_error("Report title is required")
            return

        report_dir = Path.home() / '.winpatable' / 'reports'
        report_dir.mkdir(parents=True, exist_ok=True)

        timestamp = int(time.time())
        filename = f"{rpt_type}_{timestamp}.json"
        path = report_dir / filename

        system_summary = {
            'user': getpass.getuser(),
            'platform': platform.platform(),
            'python': platform.python_version()
        }

        report = {
            'type': rpt_type,
            'title': title,
            'description': description or '',
            'system': system_summary,
            'created_at': timestamp
        }

        try:
            with open(path, 'w') as fh:
                json.dump(report, fh, indent=2)
            print_success(f"Report saved: {path}")
        except Exception as e:
            print_error(f"Failed to save report: {e}")
            return

        # Offer to open GitHub new issue page with prefilled title/body
        if sys.stdin.isatty():
            go = input("Open GitHub new issue page to submit this report? (y/n): ").strip().lower()
            if go == 'y':
                repo = 'thomasboy2017/Winpatable-'
                url = f"https://github.com/{repo}/issues/new?title={urllib_request_quote(title)}&body={urllib_request_quote(description or '')}"
                try:
                    webbrowser.open(url)
                    print_info("Opened browser to GitHub issue page")
                except Exception:
                    print_warning("Could not open web browser. You can manually create an issue at: https://github.com/thomasboy2017/Winpatable-/issues/new")


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
