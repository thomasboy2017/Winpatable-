#!/usr/bin/env python3
"""
Test suite for Winpatable
"""

import unittest
import tempfile
import os
from pathlib import Path
from src.core.system_info import SystemDetector, SystemInfo
from src.wine.wine_manager import WineManager
from src.installers.app_installers import ApplicationManager

class TestSystemDetection(unittest.TestCase):
    """Test system detection functionality"""
    
    def setUp(self):
        self.detector = SystemDetector()
    
    def test_os_detection(self):
        """Test OS detection"""
        os_type, version = self.detector.detect_os()
        self.assertIsNotNone(os_type)
        self.assertIsNotNone(version)
    
    def test_cpu_detection(self):
        """Test CPU detection"""
        cpu = self.detector.detect_cpu()
        self.assertIsNotNone(cpu)
        self.assertGreater(cpu.cores, 0)
    
    def test_memory_detection(self):
        """Test memory detection"""
        memory = self.detector.detect_memory()
        self.assertGreater(memory, 0)
    
    def test_kernel_version(self):
        """Test kernel version detection"""
        kernel = self.detector.get_kernel_version()
        self.assertIsNotNone(kernel)
    
    def test_full_system_info(self):
        """Test complete system information detection"""
        info = self.detector.detect_all()
        self.assertIsInstance(info, SystemInfo)
        self.assertGreater(len(info.gpus), 0)

class TestWineManager(unittest.TestCase):
    """Test Wine manager functionality"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.manager = WineManager(self.temp_dir)
    
    def test_prefix_creation(self):
        """Test Wine prefix directory creation"""
        result = self.manager.ensure_prefix_directory()
        self.assertTrue(result)
        self.assertTrue(self.manager.prefix_path.exists())
    
    def test_config_save_load(self):
        """Test configuration save and load"""
        test_config = {'test_key': 'test_value'}
        self.manager.ensure_prefix_directory()
        self.manager._save_config(test_config)
        
        loaded = self.manager.load_config()
        self.assertEqual(loaded, test_config)
    
    def test_environment_variables(self):
        """Test environment variable generation"""
        env_vars = self.manager.set_environment_variables()
        self.assertIn('WINEPREFIX', env_vars)
        self.assertIn('DXVK_HUD', env_vars)

class TestApplicationManager(unittest.TestCase):
    """Test application manager functionality"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.manager = ApplicationManager(self.temp_dir)
    
    def test_list_applications(self):
        """Test listing supported applications"""
        apps = self.manager.list_applications()
        # Original apps
        self.assertIn('premiere', apps)
        self.assertIn('vegas', apps)
        self.assertIn('3dsmax', apps)
        self.assertIn('office', apps)
        # New Adobe apps
        self.assertIn('photoshop', apps)
        self.assertIn('lightroom', apps)
        self.assertIn('illustrator', apps)
        self.assertIn('aftereffects', apps)
        # New Autodesk apps
        self.assertIn('revit', apps)
        self.assertIn('sketchbook', apps)
        # New Corel apps
        self.assertIn('coreldraw', apps)
        self.assertIn('corelpainter', apps)
        # New Microsoft productivity apps
        self.assertIn('teams', apps)
        self.assertIn('copilot', apps)
        self.assertIn('access', apps)
    
    def test_total_apps_count(self):
        """Test that all expected apps are available"""
        apps = self.manager.list_applications()
        # original + added apps = 25 total
        self.assertEqual(len(apps), 25)
    
    def test_get_installer(self):
        """Test getting application installer"""
        installer = self.manager.get_installer('office')
        self.assertIsNotNone(installer)
    
    def test_invalid_app(self):
        """Test getting installer for invalid app"""
        installer = self.manager.get_installer('invalid')
        self.assertIsNone(installer)
    
    def test_adobe_photoshop_installer(self):
        """Test Adobe Photoshop installer availability"""
        installer = self.manager.get_installer('photoshop')
        self.assertIsNotNone(installer)
        self.assertEqual(installer.CONFIG.name, 'Adobe Photoshop')
        self.assertEqual(installer.CONFIG.minimum_ram_gb, 4)
    
    def test_adobe_lightroom_installer(self):
        """Test Adobe Lightroom installer availability"""
        installer = self.manager.get_installer('lightroom')
        self.assertIsNotNone(installer)
        self.assertEqual(installer.CONFIG.name, 'Adobe Lightroom')
        self.assertEqual(installer.CONFIG.minimum_ram_gb, 4)
    
    def test_adobe_illustrator_installer(self):
        """Test Adobe Illustrator installer availability"""
        installer = self.manager.get_installer('illustrator')
        self.assertIsNotNone(installer)
        self.assertEqual(installer.CONFIG.name, 'Adobe Illustrator')
        self.assertEqual(installer.CONFIG.minimum_ram_gb, 4)
    
    def test_adobe_aftereffects_installer(self):
        """Test Adobe After Effects installer availability"""
        installer = self.manager.get_installer('aftereffects')
        self.assertIsNotNone(installer)
        self.assertEqual(installer.CONFIG.name, 'Adobe After Effects')
        self.assertEqual(installer.CONFIG.minimum_ram_gb, 4)
    
    def test_autodesk_revit_installer(self):
        """Test Autodesk Revit installer availability"""
        installer = self.manager.get_installer('revit')
        self.assertIsNotNone(installer)
        self.assertEqual(installer.CONFIG.name, 'Autodesk Revit')
        self.assertEqual(installer.CONFIG.minimum_ram_gb, 4)
    
    def test_autodesk_sketchbook_installer(self):
        """Test Autodesk Sketchbook installer availability"""
        installer = self.manager.get_installer('sketchbook')
        self.assertIsNotNone(installer)
        self.assertEqual(installer.CONFIG.name, 'Autodesk Sketchbook')
        self.assertEqual(installer.CONFIG.minimum_ram_gb, 4)
    
    def test_coreldraw_installer(self):
        """Test CorelDRAW installer availability"""
        installer = self.manager.get_installer('coreldraw')
        self.assertIsNotNone(installer)
        self.assertEqual(installer.CONFIG.name, 'CorelDRAW')
        self.assertEqual(installer.CONFIG.minimum_ram_gb, 4)
    
    def test_corelpainter_installer(self):
        """Test Corel Painter installer availability"""
        installer = self.manager.get_installer('corelpainter')
        self.assertIsNotNone(installer)
        self.assertEqual(installer.CONFIG.name, 'Corel Painter')
        self.assertEqual(installer.CONFIG.minimum_ram_gb, 4)

    def test_microsoft_teams_installer(self):
        """Test Microsoft Teams installer availability"""
        installer = self.manager.get_installer('teams')
        self.assertIsNotNone(installer)
        self.assertEqual(installer.CONFIG.name, 'Microsoft Teams')
        self.assertEqual(installer.CONFIG.minimum_ram_gb, 4)

    def test_microsoft_copilot_installer(self):
        """Test Microsoft Copilot installer availability"""
        installer = self.manager.get_installer('copilot')
        self.assertIsNotNone(installer)
        self.assertEqual(installer.CONFIG.name, 'Microsoft Copilot')
        self.assertEqual(installer.CONFIG.minimum_ram_gb, 4)

    def test_microsoft_access_installer(self):
        """Test Microsoft Access installer availability"""
        installer = self.manager.get_installer('access')
        self.assertIsNotNone(installer)
        self.assertEqual(installer.CONFIG.name, 'Microsoft Access')
        self.assertEqual(installer.CONFIG.minimum_ram_gb, 4)

class TestCompatibility(unittest.TestCase):
    """Test system compatibility checks"""
    
    def test_x64_detection(self):
        """Test x64 architecture detection"""
        machine = os.uname().machine
        self.assertEqual(machine, 'x86_64')
    
    def test_supported_os(self):
        """Test supported OS detection"""
        detector = SystemDetector()
        os_type, version = detector.detect_os()
        supported = ['ubuntu', 'linux-mint']
        self.assertIn(os_type.value, supported)

def run_tests():
    """Run all tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestSystemDetection))
    suite.addTests(loader.loadTestsFromTestCase(TestWineManager))
    suite.addTests(loader.loadTestsFromTestCase(TestApplicationManager))
    suite.addTests(loader.loadTestsFromTestCase(TestCompatibility))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    import sys
    sys.exit(run_tests())
