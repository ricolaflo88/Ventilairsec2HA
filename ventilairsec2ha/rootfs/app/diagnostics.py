#!/usr/bin/env python3
"""
Troubleshooting tool for GPIO/USB EnOcean connection issues.

This script helps diagnose connection problems with the EnOcean module,
checking GPIO availability, USB devices, serial port permissions, etc.
"""

import os
import subprocess
import sys
from pathlib import Path


class ConnectionDiagnostics:
    """Diagnostic tool for EnOcean connection issues."""
    
    def __init__(self):
        """Initialize diagnostics."""
        self.issues = []
        self.warnings = []
        self.info = []
    
    def check_gpio_uart_paths(self):
        """Check if GPIO UART paths exist."""
        print("\n" + "="*60)
        print("🔍 Checking GPIO UART Paths")
        print("="*60)
        
        gpio_paths = [
            ('/dev/ttyAMA0', 'Primary Raspberry Pi UART0'),
            ('/dev/serial0', 'Alias for UART0'),
            ('/dev/ttyS0', 'Mini UART (UART1)')
        ]
        
        found_gpio = False
        for path, description in gpio_paths:
            if Path(path).exists():
                self._check_permissions(path, "GPIO UART")
                found_gpio = True
                self.info.append(f"✓ Found {description}: {path}")
                print(f"✓ Found {description}: {path}")
            else:
                print(f"✗ Not found: {path} ({description})")
        
        if not found_gpio:
            self.warnings.append("No GPIO UART ports found. GPIO UART may not be enabled on this device.")
    
    def check_usb_devices(self):
        """Check for USB serial devices."""
        print("\n" + "="*60)
        print("🔍 Checking USB Serial Devices")
        print("="*60)
        
        usb_patterns = ['/dev/ttyUSB*', '/dev/ttyACM*']
        
        found_usb = False
        for pattern in usb_patterns:
            paths = list(Path('/dev').glob(pattern.replace('/dev/', '')))
            if paths:
                found_usb = True
                for path in paths:
                    self._check_permissions(str(path), "USB Serial")
                    self.info.append(f"✓ Found USB device: {path}")
                    print(f"✓ Found USB device: {path}")
        
        if not found_usb:
            print("✗ No USB serial devices found")
    
    def _check_permissions(self, path, device_type):
        """Check read/write permissions on serial port."""
        p = Path(path)
        
        try:
            if os.access(path, os.R_OK):
                print(f"  ✓ Readable: {path}")
            else:
                msg = f"✗ Not readable (permission denied): {path}"
                print(msg)
                self.issues.append(msg)
            
            if os.access(path, os.W_OK):
                print(f"  ✓ Writable: {path}")
            else:
                msg = f"✗ Not writable (permission denied): {path}"
                print(msg)
                self.issues.append(msg)
            
            # Show actual permissions
            stat = p.stat()
            perms = oct(stat.st_mode)[-3:]
            print(f"  📊 Permissions: {perms}")
            
        except Exception as e:
            self.issues.append(f"Could not check permissions for {path}: {e}")
    
    def check_uart_enabled(self):
        """Check if UART is enabled on Raspberry Pi."""
        print("\n" + "="*60)
        print("🔍 Checking UART Configuration (Raspberry Pi)")
        print("="*60)
        
        config_paths = [
            '/boot/firmware/config.txt',
            '/boot/config.txt'
        ]
        
        uart_enabled = False
        for config_path in config_paths:
            if Path(config_path).exists():
                try:
                    with open(config_path) as f:
                        content = f.read()
                        if 'enable_uart=1' in content:
                            uart_enabled = True
                            self.info.append(f"✓ UART enabled in {config_path}")
                            print(f"✓ UART enabled in {config_path}")
                        elif '[all]' in content or 'dtoverlay' in content:
                            self.warnings.append(f"Could not determine UART status from {config_path}")
                            print(f"⚠ UART configuration unclear in {config_path}")
                except Exception as e:
                    self.warnings.append(f"Could not read {config_path}: {e}")
                    print(f"⚠ Could not read {config_path}: {e}")
        
        if not uart_enabled:
            self.warnings.append("UART may not be enabled. See GPIO_USB_GUIDE.md for activation steps.")
    
    def check_pyserial_installation(self):
        """Check if pyserial is installed."""
        print("\n" + "="*60)
        print("🔍 Checking Python Serial Module")
        print("="*60)
        
        try:
            import serial
            self.info.append(f"✓ pyserial installed: version {serial.VERSION}")
            print(f"✓ pyserial installed: version {serial.VERSION}")
        except ImportError:
            msg = "✗ pyserial not installed"
            self.issues.append(msg)
            print(msg)
    
    def check_addon_user_groups(self):
        """Check if current user is in necessary groups."""
        print("\n" + "="*60)
        print("🔍 Checking User Groups")
        print("="*60)
        
        try:
            # Get current user's groups
            result = subprocess.run(['id'], capture_output=True, text=True)
            print(f"User info: {result.stdout.strip()}")
            
            # Check for dialout group (often needed for serial)
            if 'dialout' in result.stdout:
                self.info.append("✓ User in 'dialout' group (can access serial ports)")
                print("✓ User in 'dialout' group")
            else:
                self.warnings.append("User not in 'dialout' group. May need to add user to dialout group.")
                print("⚠ User not in 'dialout' group (may need sudo)")
            
            # Check for gpio group (for direct GPIO access)
            if 'gpio' in result.stdout:
                self.info.append("✓ User in 'gpio' group")
                print("✓ User in 'gpio' group")
            else:
                print("ℹ User not in 'gpio' group (not critical for UART)")
                
        except Exception as e:
            self.warnings.append(f"Could not check user groups: {e}")
    
    def check_dmesg_errors(self):
        """Check dmesg for recent serial/USB errors."""
        print("\n" + "="*60)
        print("🔍 Checking Recent System Errors (dmesg)")
        print("="*60)
        
        try:
            # Get last 30 lines of dmesg, filter for serial/usb errors
            result = subprocess.run(
                ['dmesg', '-T'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            lines = result.stdout.split('\n')[-30:]
            serial_lines = [l for l in lines if any(x in l.lower() for x in 
                           ['serial', 'usb', 'tty', 'uart', 'error', 'failed'])]
            
            if serial_lines:
                print("Recent relevant dmesg messages:")
                for line in serial_lines[-10:]:
                    if 'error' in line.lower() or 'failed' in line.lower():
                        self.warnings.append(f"dmesg: {line}")
                        print(f"  ⚠ {line}")
                    else:
                        print(f"  ℹ {line}")
            else:
                self.info.append("✓ No serial/USB errors in recent dmesg")
                print("✓ No recent serial/USB errors found")
                
        except Exception as e:
            print(f"ℹ Could not read dmesg (may require sudo): {e}")
    
    def check_home_assistant_environment(self):
        """Check if running in Home Assistant environment."""
        print("\n" + "="*60)
        print("🔍 Checking Home Assistant Environment")
        print("="*60)
        
        ha_indicators = {
            '/usr/bin/ha': 'Home Assistant CLI',
            '/data': 'Home Assistant Data Directory',
            '/data/options.json': 'Home Assistant Addon Options',
            '/run/supervisor': 'Home Assistant Supervisor'
        }
        
        found_ha = False
        for path, description in ha_indicators.items():
            if Path(path).exists():
                found_ha = True
                self.info.append(f"✓ Found {description}: {path}")
                print(f"✓ Found {description}: {path}")
        
        if not found_ha:
            self.warnings.append("Not running in Home Assistant environment (testing outside HA?)")
            print("⚠ Not in Home Assistant environment")
        else:
            print("✓ Running in Home Assistant environment")
    
    def generate_report(self):
        """Generate and print diagnostic report."""
        print("\n" + "="*60)
        print("📋 Diagnostic Report")
        print("="*60)
        
        if self.info:
            print("\n✓ Information:")
            for item in self.info:
                print(f"  {item}")
        
        if self.warnings:
            print("\n⚠ Warnings:")
            for item in self.warnings:
                print(f"  {item}")
        
        if self.issues:
            print("\n✗ Issues:")
            for item in self.issues:
                print(f"  {item}")
        
        # Final recommendation
        print("\n" + "="*60)
        print("🎯 Recommendation")
        print("="*60)
        
        if not self.issues:
            print("✓ Connection appears to be properly configured!")
            print("  Try restarting the addon to complete the connection.")
            return 0
        else:
            print("✗ Issues found that may prevent connection:")
            print("\nRecommendations:")
            print("  1. Check permissions on /dev/ttyAMA0 or /dev/ttyUSB0")
            print("  2. Enable UART: see GPIO_USB_GUIDE.md")
            print("  3. Check User/group membership")
            print("  4. Try explicit serial_port in addon settings")
            print("  5. Check for physical connection issues")
            return 1
    
    def run_all_checks(self):
        """Run all diagnostic checks."""
        print("\n" + "="*70)
        print("  EnOcean Connection Diagnostics - Ventilairsec2HA")
        print("="*70)
        
        self.check_home_assistant_environment()
        self.check_gpio_uart_paths()
        self.check_usb_devices()
        self.check_uart_enabled()
        self.check_pyserial_installation()
        self.check_addon_user_groups()
        self.check_dmesg_errors()
        
        return self.generate_report()


def main():
    """Run diagnostics."""
    diagnostics = ConnectionDiagnostics()
    return diagnostics.run_all_checks()


if __name__ == '__main__':
    sys.exit(main())
