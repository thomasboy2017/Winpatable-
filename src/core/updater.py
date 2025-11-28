#!/usr/bin/env python3
"""
Automatic update client for Winpatable
Checks for new releases on GitHub and updates the application
"""

import os
import sys
import json
import urllib.request
import urllib.error
import tempfile
import tarfile
import shutil
import subprocess
from pathlib import Path
from typing import Optional, Dict, Tuple
import time
import hashlib
import re

__version__ = "0.1.0"

GITHUB_REPO = "thomasboy2017/Winpatable-"
GITHUB_API = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
UPDATER_CONFIG = os.path.expanduser("~/.winpatable/updater.json")

# Default intervals (days)
DEFAULT_SECURITY_INTERVAL_DAYS = 7
DEFAULT_FEATURE_INTERVAL_DAYS = 30
RELEASE_DOWNLOAD_URL = f"https://github.com/{GITHUB_REPO}/releases/download"


class UpdateChecker:
    """Handles checking and downloading updates from GitHub"""
    
    def __init__(self, current_version: str = __version__, timeout: int = 10):
        self.current_version = current_version
        self.timeout = timeout
        self.latest_release = None

    @staticmethod
    def load_updater_config() -> Dict:
        try:
            if os.path.exists(UPDATER_CONFIG):
                with open(UPDATER_CONFIG, 'r') as fh:
                    return json.load(fh)
        except Exception:
            pass

        # Default config
        return {
            'last_check_security': 0,
            'last_check_feature': 0,
            'security_interval_days': DEFAULT_SECURITY_INTERVAL_DAYS,
            'feature_interval_days': DEFAULT_FEATURE_INTERVAL_DAYS
        }

    @staticmethod
    def save_updater_config(cfg: Dict):
        try:
            os.makedirs(os.path.dirname(UPDATER_CONFIG), exist_ok=True)
            with open(UPDATER_CONFIG, 'w') as fh:
                json.dump(cfg, fh)
        except Exception:
            pass
    
    def parse_version(self, version_str: str) -> Tuple[int, int, int]:
        """Parse semantic version string (e.g., '0.1.0') into tuple of ints"""
        try:
            # Remove 'v' prefix if present
            version_str = version_str.lstrip('v')
            parts = version_str.split('.')
            return tuple(int(p) for p in parts[:3]) + (0,) * (3 - len(parts))
        except (ValueError, AttributeError):
            return (0, 0, 0)
    
    def check_for_updates(self) -> bool:
        """Check GitHub for a new release. Returns True if update available."""
        try:
            with urllib.request.urlopen(GITHUB_API, timeout=self.timeout) as response:
                data = json.loads(response.read().decode('utf-8'))
                self.latest_release = data
                
                latest_version = data.get('tag_name', 'v0.0.0')
                current = self.parse_version(self.current_version)
                latest = self.parse_version(latest_version)
                
                if latest > current:
                    return True
        except (urllib.error.URLError, json.JSONDecodeError, Exception) as e:
            print(f"⚠ Could not check for updates: {e}")
            return False
        
        return False
    
    def get_release_info(self) -> Optional[Dict]:
        """Get information about the latest release"""
        return self.latest_release

    def is_security_release(self) -> bool:
        """Heuristic: determine whether the latest release is a security/patch release.

        This looks for keywords in the tag, name or body such as 'security', 'patch', 'hotfix', 'fix', 'sec'.
        """
        if not self.latest_release:
            return False

        text = ' '.join([
            str(self.latest_release.get('tag_name', '')),
            str(self.latest_release.get('name', '')),
            str(self.latest_release.get('body', ''))
        ]).lower()

        keywords = ['security', 'sec', 'patch', 'hotfix', 'fix']
        return any(k in text for k in keywords)
    
    def download_and_extract_update(self, asset_filename: str = "Winpatable-complete.tar.gz") -> bool:
        """Download and extract the latest release archive"""
        if not self.latest_release:
            print("✗ No release information available. Run check_for_updates() first.")
            return False
        
        tag = self.latest_release.get('tag_name', 'v0.1.0')
        download_url = f"{RELEASE_DOWNLOAD_URL}/{tag}/{asset_filename}"
        
        try:
            print(f"📥 Downloading {asset_filename} from {tag}...")
            
            with tempfile.TemporaryDirectory() as tmpdir:
                archive_path = os.path.join(tmpdir, asset_filename)
                
                # Download the archive
                with urllib.request.urlopen(download_url, timeout=self.timeout) as response:
                    with open(archive_path, 'wb') as f:
                        f.write(response.read())
                
                print(f"✓ Downloaded {asset_filename}")
                
                # Extract to a temporary location first
                extract_dir = os.path.join(tmpdir, "extracted")
                os.makedirs(extract_dir, exist_ok=True)
                
                with tarfile.open(archive_path, 'r:gz') as tar:
                    tar.extractall(extract_dir)
                
                print(f"✓ Extracted to {extract_dir}")
                
                # Find the Winpatable- directory inside
                extracted_items = os.listdir(extract_dir)
                if extracted_items:
                    src_dir = os.path.join(extract_dir, extracted_items[0])
                    
                    # Get installation directory (user-local)
                    install_dir = self.get_install_dir()
                    
                    # Backup current installation
                    backup_dir = install_dir + ".backup"
                    if os.path.exists(install_dir):
                        if os.path.exists(backup_dir):
                            shutil.rmtree(backup_dir)
                        shutil.copytree(install_dir, backup_dir)
                        print(f"✓ Backed up current installation to {backup_dir}")
                    
                    # Copy new files over
                    if os.path.exists(install_dir):
                        shutil.rmtree(install_dir)
                    shutil.copytree(src_dir, install_dir)
                    
                    print(f"✓ Updated installation in {install_dir}")
                    return True
        except Exception as e:
            print(f"✗ Update failed: {e}")
            return False
        
        return False
    
    def get_install_dir(self) -> str:
        """Get the installation directory (user home or system)"""
        # Check if running from Flatpak
        if os.path.exists("/.flatpak-info"):
            return os.path.expanduser("~/.local/share/winpatable")
        
        # Check if installed in /opt
        if os.path.exists("/opt/winpatable"):
            return "/opt/winpatable"
        
        # Default to user home
        return os.path.expanduser("~/.local/share/winpatable")
    
    def display_update_info(self):
        """Display information about the available update"""
        if not self.latest_release:
            print("✗ No release information available.")
            return
        
        tag = self.latest_release.get('tag_name', 'unknown')
        name = self.latest_release.get('name', tag)
        body = self.latest_release.get('body', 'No description available.')
        
        print("\n" + "="*60)
        print(f"📦 New version available: {name}")
        print("="*60)
        print(body)
        print("="*60 + "\n")


def _seconds_days(days: int) -> int:
    return int(days * 24 * 60 * 60)


def auto_update(check_only: bool = False, verbose: bool = False, mode: str = 'auto', force: bool = False) -> bool:
    """
    Automatically check and update Winpatable
    
    Args:
        check_only: If True, only check for updates without installing
        verbose: If True, print more information
    
    Returns:
        True if update succeeded or no update needed, False if update failed
    """
    checker = UpdateChecker()

    cfg = UpdateChecker.load_updater_config()
    now = int(time.time())

    # Determine whether to perform security/feature checks based on mode and last timestamps
    perform_security = False
    perform_feature = False

    if mode == 'security':
        perform_security = True
    elif mode == 'feature':
        perform_feature = True
    else:  # auto
        last_sec = int(cfg.get('last_check_security', 0))
        last_feat = int(cfg.get('last_check_feature', 0))
        sec_interval = int(cfg.get('security_interval_days', DEFAULT_SECURITY_INTERVAL_DAYS))
        feat_interval = int(cfg.get('feature_interval_days', DEFAULT_FEATURE_INTERVAL_DAYS))

        if now - last_sec >= _seconds_days(sec_interval):
            perform_security = True
        if now - last_feat >= _seconds_days(feat_interval):
            perform_feature = True

    if verbose:
        print(f"🔍 Update check mode='{mode}' (security={perform_security}, feature={perform_feature})")

    # If neither is scheduled, skip
    if not (perform_security or perform_feature):
        if verbose:
            print("✓ No scheduled update checks at this time.")
        return True

    # Perform a single check for latest release and classify it
    if verbose:
        print("🔍 Checking GitHub for the latest release...")

    try:
        if checker.check_for_updates():
            checker.display_update_info()
            is_sec = checker.is_security_release()

            # Decide whether to apply based on classification
            if (is_sec and perform_security) or (not is_sec and perform_feature):
                if check_only:
                    # Update last_check times and exit (don't install)
                    if is_sec:
                        cfg['last_check_security'] = now
                    else:
                        cfg['last_check_feature'] = now
                    UpdateChecker.save_updater_config(cfg)
                    return True

                # Ask user unless forced/CI
                if not force and sys.stdin.isatty():
                    response = input("Do you want to install the update? (y/n): ").strip().lower()
                    if response != 'y':
                        print("Update cancelled by user.")
                        # still update last_check timestamp
                        if is_sec:
                            cfg['last_check_security'] = now
                        else:
                            cfg['last_check_feature'] = now
                        UpdateChecker.save_updater_config(cfg)
                        return True

                # Perform the update
                if checker.download_and_extract_update():
                    print("\n✓ Update completed successfully!")
                    print("Please restart Winpatable to use the new version.")
                    # update last check timestamps
                    if is_sec:
                        cfg['last_check_security'] = now
                    else:
                        cfg['last_check_feature'] = now
                    UpdateChecker.save_updater_config(cfg)
                    return True
                else:
                    print("\n✗ Update failed. Please try again or check GitHub releases manually.")
                    return False
            else:
                # Release available but doesn't match scheduled type
                if verbose:
                    t = 'security' if is_sec else 'feature'
                    print(f"✓ Latest release is a {t} release; not scheduled right now.")
                # Update last_check timestamps for the checked category(s)
                if perform_security:
                    cfg['last_check_security'] = now
                if perform_feature:
                    cfg['last_check_feature'] = now
                UpdateChecker.save_updater_config(cfg)
                return True
        else:
            if verbose:
                print("✓ You are running the latest version of Winpatable.")
            # update last_check timestamps even if no new release found
            if perform_security:
                cfg['last_check_security'] = now
            if perform_feature:
                cfg['last_check_feature'] = now
            UpdateChecker.save_updater_config(cfg)
            return True
    except Exception as e:
        print(f"⚠ Could not check for updates: {e}")
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Winpatable Update Client")
    parser.add_argument("--check-only", action="store_true", help="Only check for updates, don't install")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--force", action="store_true", help="Force update without asking")
    
    args = parser.parse_args()
    
    success = auto_update(check_only=args.check_only, verbose=args.verbose)
    sys.exit(0 if success else 1)
