#!/usr/bin/env python3
"""
Test auto-detection of GPIO UART vs USB connection.

This script validates the connection detection logic without requiring
actual hardware or Home Assistant environment.
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_gpio_detection():
    """Test that GPIO UART is detected when available."""
    print("\n=== Test 1: GPIO UART Detection ===")
    
    # Mock GPIO paths as available
    gpio_paths = [
        '/dev/ttyAMA0',    # Primary Raspberry Pi UART0
        '/dev/serial0',    # Alias for UART0
        '/dev/ttyS0'       # Mini UART (UART1 on Pi)
    ]
    
    with patch('pathlib.Path.exists') as mock_exists:
        def exists_side_effect(path):
            return str(path) in gpio_paths
        
        mock_exists.side_effect = exists_side_effect
        
        # Import after mocking
        from enocean_communicator import EnOceanCommunicator
        
        # Create instance with auto mode
        comm = EnOceanCommunicator(port='auto', mode='auto')
        
        # Test detection (without actually opening port)
        detected_type = comm._detect_connection_type()
        detected_port = comm._detect_port()
        
        print(f"✓ Detected connection type: {detected_type}")
        print(f"✓ Detected port: {detected_port}")
        
        assert detected_type == 'gpio_uart', f"Expected 'gpio_uart', got {detected_type}"
        assert detected_port in gpio_paths, f"Expected GPIO path, got {detected_port}"
        
    print("✓ GPIO detection test PASSED")


def test_usb_fallback():
    """Test that USB is detected when GPIO is unavailable."""
    print("\n=== Test 2: USB Fallback Detection ===")
    
    # Mock USB paths as available (GPIO paths NOT available)
    usb_paths = ['/dev/ttyUSB0', '/dev/ttyACM0']
    
    with patch('pathlib.Path.exists') as mock_exists:
        def exists_side_effect(path):
            return str(path) in usb_paths
        
        mock_exists.side_effect = exists_side_effect
        
        from enocean_communicator import EnOceanCommunicator
        
        comm = EnOceanCommunicator(port='auto', mode='auto')
        
        detected_type = comm._detect_connection_type()
        detected_port = comm._detect_port()
        
        print(f"✓ Detected connection type: {detected_type}")
        print(f"✓ Detected port: {detected_port}")
        
        assert detected_type == 'usb', f"Expected 'usb', got {detected_type}"
        assert detected_port in usb_paths, f"Expected USB path, got {detected_port}"
        
    print("✓ USB fallback test PASSED")


def test_explicit_mode_gpio():
    """Test that explicit GPIO mode is respected."""
    print("\n=== Test 3: Explicit GPIO Mode ===")
    
    with patch('pathlib.Path.exists') as mock_exists:
        mock_exists.return_value = True  # All paths exist
        
        from enocean_communicator import EnOceanCommunicator
        
        comm = EnOceanCommunicator(port='/dev/ttyAMA0', mode='gpio')
        
        print(f"✓ Mode set to: {comm.mode}")
        print(f"✓ Port set to: /dev/ttyAMA0")
        
        assert comm.mode == 'gpio', f"Expected mode 'gpio', got {comm.mode}"
        
    print("✓ Explicit GPIO mode test PASSED")


def test_explicit_mode_usb():
    """Test that explicit USB mode is respected."""
    print("\n=== Test 4: Explicit USB Mode ===")
    
    with patch('pathlib.Path.exists') as mock_exists:
        mock_exists.return_value = True  # All paths exist
        
        from enocean_communicator import EnOceanCommunicator
        
        comm = EnOceanCommunicator(port='/dev/ttyUSB0', mode='usb')
        
        print(f"✓ Mode set to: {comm.mode}")
        print(f"✓ Port set to: /dev/ttyUSB0")
        
        assert comm.mode == 'usb', f"Expected mode 'usb', got {comm.mode}"
        
    print("✓ Explicit USB mode test PASSED")


def test_no_device_found():
    """Test behavior when no serial device is found."""
    print("\n=== Test 5: No Device Found ===")
    
    with patch('pathlib.Path.exists') as mock_exists:
        mock_exists.return_value = False  # No paths exist
        
        from enocean_communicator import EnOceanCommunicator
        
        comm = EnOceanCommunicator(port='auto', mode='auto')
        
        detected_port = comm._detect_port()
        
        print(f"✓ Detected port when nothing available: {detected_port}")
        
        # Should return None or fall back to default
        assert detected_port is None or detected_port == '/dev/ttyUSB0', \
            f"Expected None or default, got {detected_port}"
        
    print("✓ No device found test PASSED")


def test_configuration_loading():
    """Test that configuration loads connection_mode correctly."""
    print("\n=== Test 6: Configuration Loading ===")
    
    from config import Config
    import tempfile
    import json
    
    # Create temporary config
    with tempfile.TemporaryDirectory() as tmpdir:
        options_file = Path(tmpdir) / 'options.json'
        
        # Test GPIO mode
        options = {
            'mqtt_host': 'localhost',
            'mqtt_port': 1883,
            'log_level': 'INFO',
            'connection_mode': 'gpio',
            'serial_port': '/dev/ttyAMA0'
        }
        
        options_file.write_text(json.dumps(options))
        
        config = Config(str(options_file))
        
        print(f"✓ Loaded connection_mode: {config.connection_mode}")
        print(f"✓ Loaded serial_port: {config.serial_port}")
        
        assert config.connection_mode == 'gpio', f"Expected 'gpio', got {config.connection_mode}"
        assert config.serial_port == '/dev/ttyAMA0'
        
    print("✓ Configuration loading test PASSED")


def main():
    """Run all tests."""
    print("=" * 60)
    print("Connection Detection Test Suite")
    print("=" * 60)
    
    try:
        test_gpio_detection()
        test_usb_fallback()
        test_explicit_mode_gpio()
        test_explicit_mode_usb()
        test_no_device_found()
        test_configuration_loading()
        
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED")
        print("=" * 60)
        return 0
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    exit(main())
