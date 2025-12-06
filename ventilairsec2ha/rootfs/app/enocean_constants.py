"""
EnOcean protocol constants and utilities
Based on EnOcean radio specification
"""

from enum import IntEnum
from typing import Dict, Tuple

# RORG (Radio Telegram Type) definitions
class RORG(IntEnum):
    """EnOcean Radio Telegram types"""
    RPS = 0xF6  # Repeated Switch Communication
    BS1 = 0xD5  # Single Data
    BS4 = 0xA5  # Variable Length Data
    BS4_VAR = 0xA6  # 4BS variable length telegram
    VLD = 0xB0  # Variable Length Data
    MSC = 0xD1  # Manufacturer Specific Command
    UTE = 0xC6  # Universal Teach-In
    CHAINED = 0xF0  # Chained data (4BS data blocks)
    RESPONSE = 0x02  # Response


# Function codes for common RORGs
FUNC_TYPES: Dict[str, Dict[int, str]] = {
    'A5': {  # 4BS - Temperature, humidity, light
        0x04: 'Temperature/Humidity Sensor',
        0x09: 'CO2 Sensor',
        0x12: 'Illumination Sensor'
    },
    'D1': {  # MSC - Manufacturer Specific
        0x07: 'Ventilairsec VMI'
    }
}


# Device definitions with EnOcean chip ID format: RORG-FUNC-TYPE
class EnOceanDevices:
    """Known EnOcean device types"""
    
    # VMI Purevent Ventilairsec
    VMI_PUREVENT = {
        'rorg': 0xD1,
        'func': 0x07,
        'type': 0x9F,
        'name': 'VMI Purevent Ventilairsec',
        'variants': {
            '01': 'VMI (Device)',  # 0x0421574F
            '00': 'Assistant (Remote Control)'  # 0x0422407D
        }
    }
    
    # Environmental sensors
    CO2_SENSOR = {
        'rorg': 0xA5,
        'func': 0x09,
        'type': 0x04,
        'name': 'CO2 Sensor'
    }
    
    TEMP_HUMIDITY_SENSOR = {
        'rorg': 0xA5,
        'func': 0x04,
        'type': 0x01,
        'name': 'Temperature/Humidity Sensor'
    }


# EnOcean frame structure constants
FRAME_HEADER = 0xAA  # Start byte
FRAME_SYNC = [0xAA, 0xAA, 0xAA]  # Sync pattern
FRAME_LENGTH_MIN = 7  # Minimum frame length (header + type + data)


# Packet type definitions (from ESP3 protocol)
class PacketType(IntEnum):
    """ESP3 Protocol Packet Types"""
    RESERVED = 0x00
    RADIO_ERP1 = 0x01
    RESPONSE = 0x02
    RADIO_SUB_TEL = 0x03
    EVENT = 0x04
    COMMON_COMMAND = 0x05
    SMART_ACK_COMMAND = 0x06
    REMOTE_MAN_COMMAND = 0x07
    RADIO_MESSAGE = 0x08
    RADIO_ADVANCED = 0x09


# Status bit definitions for Radio packets
class PacketStatus:
    """Status bytes for radio packets"""
    REPEATER_COUNT_MASK = 0x0F
    REPEATER_ERROR_MASK = 0x10
    CRC_OK = 0x00
    CRC_ERROR = 0xFF


# Ventilairsec D1-07-9F specific commands
class VentilairsecCommands(IntEnum):
    """Ventilairsec command types for D1-07-9F"""
    SPEED_LOW = 0x10
    SPEED_MEDIUM = 0x20
    SPEED_HIGH = 0x30
    SPEED_MAX = 0x40
    MODE_AUTO = 0x01
    MODE_MANUAL = 0x02
    MODE_BYPASS = 0x03
    MODE_OFF = 0x00
    TEACH_IN = 0x80
    TEACH_OUT = 0x81


# Data field structure for Ventilairsec
VENTILAIRSEC_D1_07_9F_FIELDS = {
    'status': {
        'offset': 0,
        'length': 1,
        'description': 'Status and control byte'
    },
    'speed': {
        'offset': 0,
        'length': 2,
        'description': 'Fan speed (0-100%)'
    },
    'temperature': {
        'offset': 1,
        'length': 1,
        'description': 'Temperature (°C)'
    },
    'errors': {
        'offset': 2,
        'length': 2,
        'description': 'Error codes'
    }
}


# Utility functions
def rorg_to_hex(rorg: int) -> str:
    """Convert RORG value to hex string"""
    return f"{rorg:02X}"


def addr_to_hex(addr: bytes) -> str:
    """Convert 4-byte address to hex string"""
    if isinstance(addr, (list, tuple)):
        return "".join(f"{b:02X}" for b in addr)
    return addr.hex() if hasattr(addr, 'hex') else str(addr)


def hex_to_addr(hex_str: str) -> bytes:
    """Convert hex string to 4-byte address"""
    return bytes.fromhex(hex_str.replace(':', '').replace('-', ''))
