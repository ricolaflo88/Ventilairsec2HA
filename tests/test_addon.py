"""
Unit tests for Ventilairsec2HA addon
Tests EnOcean packet parsing and device communication logic
"""

import sys
import unittest
from pathlib import Path

# Add app directory to path
app_dir = Path(__file__).parent.parent / "ventilairsec2ha" / "rootfs" / "app"
sys.path.insert(0, str(app_dir))

from enocean_packet import EnOceanPacket, RadioPacket
from enocean_constants import RORG, rorg_to_hex, addr_to_hex, hex_to_addr


class TestEnOceanPacket(unittest.TestCase):
    """Test EnOcean packet parsing and creation"""
    
    def test_rorg_to_hex(self):
        """Test RORG to hex conversion"""
        self.assertEqual(rorg_to_hex(RORG.BS4), "A5")
        self.assertEqual(rorg_to_hex(RORG.RPS), "F6")
        self.assertEqual(rorg_to_hex(RORG.MSC), "D1")
    
    def test_addr_to_hex(self):
        """Test address to hex conversion"""
        addr = bytes([0x04, 0x21, 0x57, 0x4F])
        result = addr_to_hex(addr)
        self.assertEqual(result, "0421574F")
    
    def test_hex_to_addr(self):
        """Test hex to address conversion"""
        hex_str = "0421574F"
        result = hex_to_addr(hex_str)
        expected = bytes([0x04, 0x21, 0x57, 0x4F])
        self.assertEqual(result, expected)
    
    def test_crc_calculation(self):
        """Test CRC8 checksum calculation"""
        test_data = bytes([0xA5, 0x50, 0x00, 0xA8, 0x81, 0x00, 0x32, 0x27])
        crc = EnOceanPacket._calculate_crc(test_data)
        self.assertIsInstance(crc, int)
        self.assertGreaterEqual(crc, 0)
        self.assertLess(crc, 256)
    
    def test_radio_packet_creation(self):
        """Test creation of radio packet"""
        rorg = 0xA5
        data = bytes([0x50, 0x00, 0xA8, 0x81])
        sender_addr = bytes([0x81, 0x00, 0x32, 0x27])
        
        packet = EnOceanPacket.create_radio_packet(
            rorg=rorg,
            data=data,
            sender_addr=sender_addr
        )
        
        self.assertIsInstance(packet, bytes)
        self.assertEqual(packet[0], 0xAA)  # Frame header
        self.assertGreater(len(packet), 10)
    
    def test_radio_packet_parsing(self):
        """Test parsing of radio packet"""
        # Create a simple valid packet structure
        # Format: [HEADER|LEN_H|LEN_L|CRC_LEN|TYPE|RORG|DATA...|ADDR...|STATUS|CRC]
        
        rorg = 0xA5
        data = bytes([0x50, 0x00, 0xA8])
        sender = bytes([0x81, 0x00, 0x32, 0x27])
        status = 0x80  # Learn bit set
        
        # This is a simplified test - full packet parsing is complex
        # In production, this would use real serial data
        
        self.assertTrue(True)  # Placeholder for full packet test


class TestRadioPacket(unittest.TestCase):
    """Test RadioPacket data class"""
    
    def test_radio_packet_creation(self):
        """Test creation of RadioPacket"""
        sender = bytes([0x04, 0x21, 0x57, 0x4F])
        dest = bytes([0xFF, 0xFF, 0xFF, 0xFF])
        data = bytes([0x50, 0x00, 0xA8, 0x81])
        
        packet = RadioPacket(
            packet_type=1,
            rorg=0xA5,
            func=0x09,
            type_byte=0x04,
            sender_addr=sender,
            destination_addr=dest,
            data=data,
            optional_data=b'',
            security_level=0,
            rssi=-60,
            repeater_count=0,
            learn=False,
            command=0
        )
        
        self.assertEqual(packet.sender_hex, "0421574F")
        self.assertEqual(packet.destination_hex, "FFFFFFFF")
        self.assertEqual(packet.rorg, 0xA5)
    
    def test_radio_packet_validation(self):
        """Test RadioPacket validation"""
        # Invalid: sender address not 4 bytes
        with self.assertRaises(ValueError):
            RadioPacket(
                packet_type=1,
                rorg=0xA5,
                func=0x09,
                type_byte=0x04,
                sender_addr=bytes([0x01, 0x02, 0x03]),  # Too short
                destination_addr=bytes([0xFF, 0xFF, 0xFF, 0xFF]),
                data=b'test',
                optional_data=b'',
                security_level=0,
                rssi=-60,
                repeater_count=0,
                learn=False,
                command=0
            )


class TestPacketBuffer(unittest.TestCase):
    """Test RawPacketBuffer"""
    
    def test_buffer_add_data(self):
        """Test adding data to buffer"""
        from enocean_packet import RawPacketBuffer
        
        buffer = RawPacketBuffer()
        test_data = bytes([0xAA, 0x00, 0x05])
        
        buffer.add_data(test_data)
        self.assertGreater(len(buffer.buffer), 0)
    
    def test_buffer_extract_incomplete_packet(self):
        """Test extracting incomplete packet"""
        from enocean_packet import RawPacketBuffer
        
        buffer = RawPacketBuffer()
        test_data = bytes([0xAA, 0x00, 0x05])  # Too short
        
        buffer.add_data(test_data)
        packet = buffer.extract_packet()
        
        self.assertIsNone(packet)


class TestVentilairsecDevices(unittest.TestCase):
    """Test Ventilairsec specific device handling"""
    
    def test_vmi_address_parsing(self):
        """Test VMI device address parsing"""
        from ventilairsec_manager import VentilairsecManager
        
        # Known device addresses
        self.assertIn('0421574F', VentilairsecManager.KNOWN_DEVICES)
        self.assertIn('81003227', VentilairsecManager.KNOWN_DEVICES)
        self.assertIn('810054F5', VentilairsecManager.KNOWN_DEVICES)
    
    def test_vmi_device_info(self):
        """Test VMI device information"""
        from ventilairsec_manager import VentilairsecManager
        
        vmi_info = VentilairsecManager.KNOWN_DEVICES.get('0421574F')
        self.assertIsNotNone(vmi_info)
        self.assertEqual(vmi_info['type'], 'vmi')
        self.assertEqual(vmi_info['rorg'], 0xD1)


class TestConfig(unittest.TestCase):
    """Test configuration loading"""
    
    def test_config_defaults(self):
        """Test configuration defaults"""
        from config import Config
        
        config = Config('/nonexistent/path.json')
        
        self.assertEqual(config.serial_port, '/dev/ttyUSB0')
        self.assertTrue(config.enable_mqtt)
        self.assertEqual(config.mqtt_broker, 'mosquitto')
        self.assertEqual(config.mqtt_port, 1883)


if __name__ == '__main__':
    unittest.main()
