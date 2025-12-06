"""
Ventilairsec VMI Manager
Handles device communication, command parsing, and state management
"""

import asyncio
import logging
from typing import Dict, Optional, List, Any
from dataclasses import dataclass, field
from datetime import datetime
import json

from enocean_packet import RadioPacket
from enocean_constants import (
    RORG, EnOceanDevices, VentilairsecCommands, addr_to_hex, hex_to_addr
)

logger = logging.getLogger(__name__)


@dataclass
class DeviceState:
    """Represents the state of a device"""
    address: str
    name: str
    rorg: int
    last_update: datetime = field(default_factory=datetime.now)
    data: Dict[str, Any] = field(default_factory=dict)

    def __repr__(self) -> str:
        return f"DeviceState({self.name} @ {self.address})"


class VentilairsecManager:
    """Manages Ventilairsec VMI and associated sensors"""

    # Known device addresses
    KNOWN_DEVICES = {
        '0421574F': {
            'name': 'VMI Purevent',
            'type': 'vmi',
            'rorg': 0xD1,
            'func': 0x07,
            'type_byte': 0x9F
        },
        '0422407D': {
            'name': 'Ventilairsec Assistant',
            'type': 'assistant',
            'rorg': 0xD1,
            'func': 0x07,
            'type_byte': 0x9F
        },
        '81003227': {
            'name': 'CO2 Sensor',
            'type': 'co2_sensor',
            'rorg': 0xA5,
            'func': 0x09,
            'type_byte': 0x04
        },
        '810054F5': {
            'name': 'Temperature/Humidity Sensor',
            'type': 'temp_humidity_sensor',
            'rorg': 0xA5,
            'func': 0x04,
            'type_byte': 0x01
        }
    }

    def __init__(self, communicator):
        self.communicator = communicator
        self.devices: Dict[str, DeviceState] = {}
        self.packet_queue: asyncio.Queue = asyncio.Queue()
        self.running = False

        # Register packet callback
        communicator.add_packet_callback(self.on_packet_received)

    async def processing_loop(self):
        """Main processing loop for incoming packets"""
        self.running = True
        logger.info("🔄 Starting Ventilairsec processing loop")

        while self.running:
            try:
                # Get next packet from queue with timeout
                packet = await asyncio.wait_for(self.packet_queue.get(), timeout=1.0)
                await self._process_packet(packet)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"❌ Error in processing loop: {e}")
                await asyncio.sleep(1)

    async def on_packet_received(self, packet: RadioPacket):
        """Callback for received packets"""
        try:
            # Add to processing queue
            await self.packet_queue.put(packet)
        except Exception as e:
            logger.error(f"❌ Error queuing packet: {e}")

    async def _process_packet(self, packet: RadioPacket):
        """Process a received packet"""
        try:
            sender_hex = packet.sender_hex.upper()
            logger.debug(f"📦 Processing packet from {sender_hex}")

            # Check if it's a known device
            if sender_hex not in self.KNOWN_DEVICES:
                logger.debug(f"⚠️  Unknown device: {sender_hex}")
                return

            device_info = self.KNOWN_DEVICES[sender_hex]
            device_name = device_info['name']
            device_type = device_info['type']

            logger.info(f"📡 Packet from {device_name} ({sender_hex})")

            # Parse packet based on type
            if device_type == 'vmi':
                await self._parse_vmi_packet(packet, sender_hex, device_name)
            elif device_type == 'assistant':
                await self._parse_assistant_packet(packet, sender_hex, device_name)
            elif device_type == 'co2_sensor':
                await self._parse_co2_packet(packet, sender_hex, device_name)
            elif device_type == 'temp_humidity_sensor':
                await self._parse_temp_humidity_packet(packet, sender_hex, device_name)

            # Update device state
            self.devices[sender_hex] = DeviceState(
                address=sender_hex,
                name=device_name,
                rorg=packet.rorg,
                data=self._extract_sensor_data(packet)
            )

        except Exception as e:
            logger.error(f"❌ Error processing packet: {e}")

    async def _parse_vmi_packet(self, packet: RadioPacket, address: str, name: str):
        """Parse VMI Purevent D1-07-9F packet"""
        try:
            # Extract data from D1-07-9F packet
            # Data structure: [Status|Speed|Temperature|Errors...]

            data = packet.data
            if len(data) < 4:
                logger.warning(f"⚠️  VMI packet too short: {len(data)} bytes")
                return

            status = data[0]
            speed = data[1] if len(data) > 1 else 0
            temperature = data[2] if len(data) > 2 else 0
            errors = (data[3] if len(data) > 3 else 0,
                     data[4] if len(data) > 4 else 0)

            logger.info(f"🌬️  VMI: Speed={speed}%, Temp={temperature}°C, Errors={errors}")

        except Exception as e:
            logger.error(f"❌ Error parsing VMI packet: {e}")

    async def _parse_assistant_packet(self, packet: RadioPacket, address: str, name: str):
        """Parse Assistant (remote control) packet"""
        try:
            logger.info(f"🎛️  Assistant packet received")
        except Exception as e:
            logger.error(f"❌ Error parsing assistant packet: {e}")

    async def _parse_co2_packet(self, packet: RadioPacket, address: str, name: str):
        """Parse CO2 Sensor A5-09-04 packet"""
        try:
            # 4BS sensor: CO2 in ppm
            # Data format: [DB_3|DB_2|DB_1|DB_0]
            data = packet.data
            if len(data) < 4:
                logger.warning(f"⚠️  CO2 packet too short")
                return

            # Convert 4 bytes to CO2 value (0-2500 ppm)
            raw_value = (data[0] << 24) | (data[1] << 16) | (data[2] << 8) | data[3]
            co2_ppm = (raw_value * 2500) // 0xFFFFFFFF

            logger.info(f"💨 CO2 Sensor: {co2_ppm} ppm")

        except Exception as e:
            logger.error(f"❌ Error parsing CO2 packet: {e}")

    async def _parse_temp_humidity_packet(self, packet: RadioPacket, address: str, name: str):
        """Parse Temperature/Humidity Sensor A5-04-01 packet"""
        try:
            # 4BS sensor: Temperature and Humidity
            # Data format varies based on type
            data = packet.data
            if len(data) < 4:
                logger.warning(f"⚠️  Temp/Humidity packet too short")
                return

            # Extract temperature (0-40°C)
            temp_raw = (data[0] << 8) | data[1]
            temperature = (temp_raw * 40) / 1023  # Normalize to 0-40°C

            # Extract humidity (0-100%)
            humidity_raw = (data[2] << 8) | data[3]
            humidity = (humidity_raw * 100) / 1023  # Normalize to 0-100%

            logger.info(f"🌡️  Temp/Humidity: {temperature:.1f}°C, {humidity:.1f}%")

        except Exception as e:
            logger.error(f"❌ Error parsing temp/humidity packet: {e}")

    def _extract_sensor_data(self, packet: RadioPacket) -> Dict[str, Any]:
        """Extract sensor data from packet"""
        data = {}

        try:
            if packet.rorg == 0xA5:  # 4BS
                # Generic 4-byte sensor
                if len(packet.data) >= 4:
                    data['raw_bytes'] = packet.data.hex()
                    data['byte_0'] = packet.data[0]
                    data['byte_1'] = packet.data[1]
                    data['byte_2'] = packet.data[2]
                    data['byte_3'] = packet.data[3]

            elif packet.rorg == 0xD1:  # MSC (Manufacturer Specific)
                if len(packet.data) >= 1:
                    data['raw_bytes'] = packet.data.hex()

        except Exception as e:
            logger.error(f"❌ Error extracting sensor data: {e}")

        return data

    async def send_command(self, device_address: str, command: int, data: bytes = b'') -> bool:
        """Send a command to a device"""
        try:
            if device_address not in self.KNOWN_DEVICES:
                logger.error(f"❌ Unknown device: {device_address}")
                return False

            device_info = self.KNOWN_DEVICES[device_address]

            # Build command packet
            packet_data = bytes([command]) + data

            # Parse address
            addr_bytes = hex_to_addr(device_address)

            # Create and send packet
            packet = RadioPacket(
                packet_type=1,  # RADIO_ERP1
                rorg=device_info['rorg'],
                func=device_info['func'],
                type_byte=device_info['type_byte'],
                sender_addr=addr_bytes,
                destination_addr=addr_bytes,
                data=packet_data,
                optional_data=b'',
                security_level=0,
                rssi=0,
                repeater_count=0,
                learn=False,
                command=command
            )

            return await self.communicator.send_packet(packet)

        except Exception as e:
            logger.error(f"❌ Error sending command: {e}")
            return False

    async def set_vmi_speed(self, speed: int) -> bool:
        """Set VMI fan speed (0-100%)"""
        try:
            if not 0 <= speed <= 100:
                logger.error(f"❌ Invalid speed: {speed}")
                return False

            logger.info(f"🎚️  Setting VMI speed to {speed}%")

            # Build command data
            command_data = bytes([speed, 0, 0])

            return await self.send_command('0421574F', 0x01, command_data)

        except Exception as e:
            logger.error(f"❌ Error setting VMI speed: {e}")
            return False

    def get_device_states(self) -> Dict[str, Any]:
        """Get all device states"""
        return {
            addr: {
                'name': state.name,
                'address': addr,
                'rorg': f"0x{state.rorg:02X}",
                'last_update': state.last_update.isoformat(),
                'data': state.data
            }
            for addr, state in self.devices.items()
        }

    def stop(self):
        """Stop the manager"""
        logger.info("🛑 Stopping Ventilairsec manager")
        self.running = False
