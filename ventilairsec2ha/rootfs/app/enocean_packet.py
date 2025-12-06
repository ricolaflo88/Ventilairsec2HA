"""
EnOcean Radio Telegram Packet handling
Implements ESP3 protocol and packet parsing
"""

import logging
from typing import Optional, Dict, Any, List, Tuple
from dataclasses import dataclass
from enum import IntEnum
import struct

from enocean_constants import (
    RORG, PacketType, FRAME_HEADER, FRAME_SYNC,
    rorg_to_hex, addr_to_hex, hex_to_addr
)

logger = logging.getLogger(__name__)


@dataclass
class RadioPacket:
    """Represents an EnOcean radio telegram"""
    
    # Packet structure
    packet_type: PacketType
    rorg: int  # Radio Telegram Type
    func: int  # Functional definition
    type_byte: int  # Type definition
    
    # Device information
    sender_addr: bytes  # 4-byte sender address
    destination_addr: bytes  # 4-byte destination (usually 0xFFFFFFFF for broadcast)
    
    # Data payload
    data: bytes  # Variable length data (1-14 bytes)
    optional_data: bytes  # Optional sub-telegram information
    
    # Signal information
    security_level: int
    rssi: int  # RSSI in dBm (typically -80 to -40)
    repeater_count: int
    learn: bool  # Learn telegram flag
    command: int  # Command type
    
    def __post_init__(self):
        """Validate packet after initialization"""
        if len(self.sender_addr) != 4:
            raise ValueError("Sender address must be 4 bytes")
        if len(self.destination_addr) != 4:
            raise ValueError("Destination address must be 4 bytes")
    
    @property
    def sender_hex(self) -> str:
        """Get sender address as hex string"""
        return addr_to_hex(self.sender_addr)
    
    @property
    def destination_hex(self) -> str:
        """Get destination address as hex string"""
        return addr_to_hex(self.destination_addr)
    
    @property
    def data_hex(self) -> str:
        """Get data as hex string"""
        return self.data.hex() if self.data else ""
    
    def __repr__(self) -> str:
        return (f"RadioPacket(type={self.rorg:02X}, "
                f"from={self.sender_hex}, "
                f"data={self.data_hex})")


class EnOceanPacket:
    """Low-level ESP3 protocol packet handling"""
    
    @staticmethod
    def create_radio_packet(
        rorg: int,
        data: bytes,
        sender_addr: bytes,
        destination_addr: bytes = b'\xFF\xFF\xFF\xFF',
        repeater_count: int = 0,
        learn: bool = False,
        command: int = 0
    ) -> bytes:
        """
        Create an ESP3 radio packet (transmission)
        
        Args:
            rorg: Radio telegram type (e.g., 0xA5, 0xD1)
            data: Payload data (1-14 bytes)
            sender_addr: 4-byte sender address
            destination_addr: 4-byte destination (default broadcast)
            repeater_count: Number of repeaters
            learn: Learn telegram flag
            command: Command type
        
        Returns:
            Complete ESP3 packet ready for transmission
        """
        
        if not data or len(data) > 14:
            raise ValueError("Data must be 1-14 bytes")
        if len(sender_addr) != 4 or len(destination_addr) != 4:
            raise ValueError("Addresses must be 4 bytes each")
        
        # Build packet structure
        # Packet format: HEADER | LENGTH(2) | PACKET_TYPE | DATA | CRC | CRC
        
        packet_type = PacketType.RADIO_ERP1
        
        # Calculate optional data length (typically 7 bytes for standard radio)
        optional_data_len = 7
        data_len = len(data) + 1  # +1 for status byte
        
        # Build header
        header = bytes([FRAME_HEADER])
        
        # Payload: RORG | DATA | SENDER_ADDR | REPEATER_COUNT | CRC8
        payload = bytes([rorg]) + data + sender_addr + destination_addr + \
                 bytes([repeater_count]) + bytes([command])
        
        # Length of data + optional data
        length = len(payload) + optional_data_len + 1  # +1 for status
        
        # CRC calculation
        crc = EnOceanPacket._calculate_crc(bytes([packet_type]) + payload)
        
        # Build final packet: SYNC | LENGTH_H | LENGTH_L | LENGTH_CRC | PACKET
        packet = (
            header + 
            bytes([(length >> 8) & 0xFF, length & 0xFF]) +
            bytes([EnOceanPacket._calculate_crc(bytes([length >> 8, length & 0xFF]))]) +
            bytes([packet_type]) +
            payload +
            bytes([crc])
        )
        
        return packet
    
    @staticmethod
    def parse_packet(data: bytes) -> Optional[RadioPacket]:
        """
        Parse an ESP3 protocol packet
        
        Args:
            data: Raw packet data
            
        Returns:
            Parsed RadioPacket or None if invalid
        """
        
        try:
            if not data or len(data) < 14:
                logger.debug(f"Packet too short: {len(data)} bytes")
                return None
            
            # Check frame header
            if data[0] != FRAME_HEADER:
                logger.debug(f"Invalid frame header: 0x{data[0]:02X}")
                return None
            
            # Extract length
            data_len_h = data[1]
            data_len_l = data[2]
            data_len = (data_len_h << 8) | data_len_l
            
            # Verify packet length
            if len(data) < data_len + 7:  # +7 for header + length fields + CRC
                logger.debug(f"Incomplete packet: expected {data_len + 7}, got {len(data)}")
                return None
            
            # Extract packet type
            packet_type = data[4]
            
            # For radio packets
            if packet_type == PacketType.RADIO_ERP1:
                # Parse radio telegram
                rorg = data[5]
                
                # Data starts at offset 6
                data_payload = data[6:6 + data_len - 1]
                
                if len(data_payload) < 6:
                    logger.debug(f"Radio packet payload too short: {len(data_payload)}")
                    return None
                
                # Extract fields
                payload_data = data_payload[:-5]  # All except last 5 bytes
                sender_addr = bytes(data_payload[-5:-1])
                status_byte = data_payload[-1]
                
                # Parse status byte
                repeater_count = status_byte & 0x0F
                learn = bool(status_byte & 0x80)
                
                # Signal information
                rssi = 0  # Would be in optional data for real packets
                
                return RadioPacket(
                    packet_type=PacketType.RADIO_ERP1,
                    rorg=rorg,
                    func=0,  # Will be parsed based on RORG/data
                    type_byte=0,  # Will be parsed based on RORG/data
                    sender_addr=sender_addr,
                    destination_addr=b'\xFF\xFF\xFF\xFF',
                    data=payload_data,
                    optional_data=b'',
                    security_level=0,
                    rssi=rssi,
                    repeater_count=repeater_count,
                    learn=learn,
                    command=0
                )
            
            logger.debug(f"Unhandled packet type: 0x{packet_type:02X}")
            return None
            
        except Exception as e:
            logger.error(f"Error parsing packet: {e}")
            return None
    
    @staticmethod
    def _calculate_crc(data: bytes) -> int:
        """Calculate CRC8 checksum (CRC-8-CCITT)"""
        crc = 0
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x80:
                    crc = ((crc << 1) ^ 0x07) & 0xFF
                else:
                    crc = (crc << 1) & 0xFF
        return crc
    
    @staticmethod
    def _calculate_4bs_crc(data: bytes) -> int:
        """Calculate CRC for 4BS data"""
        return EnOceanPacket._calculate_crc(data)


class RawPacketBuffer:
    """Buffer for handling incoming serial data"""
    
    def __init__(self, max_size: int = 65536):
        self.buffer: bytearray = bytearray()
        self.max_size = max_size
        self.sync_count = 0
    
    def add_data(self, data: bytes):
        """Add data to buffer"""
        self.buffer.extend(data)
        
        # Keep buffer size under control
        if len(self.buffer) > self.max_size:
            # Find next frame header
            idx = self.buffer.find(FRAME_HEADER, 1)
            if idx > 0:
                self.buffer = self.buffer[idx:]
            else:
                self.buffer = bytearray()
    
    def extract_packet(self) -> Optional[bytes]:
        """Extract next complete packet from buffer"""
        
        if len(self.buffer) < 7:  # Minimum frame size
            return None
        
        # Find frame header
        while len(self.buffer) > 0 and self.buffer[0] != FRAME_HEADER:
            self.buffer.pop(0)
        
        if len(self.buffer) < 7:
            return None
        
        # Get packet length
        data_len = (self.buffer[1] << 8) | self.buffer[2]
        total_len = data_len + 7  # +7 for header + length fields + CRC
        
        # Check if we have complete packet
        if len(self.buffer) < total_len:
            return None
        
        # Extract packet
        packet = bytes(self.buffer[:total_len])
        del self.buffer[:total_len]
        
        return packet
