"""
EnOcean Serial Communicator
Handles low-level serial communication with EnOcean stick (USB or GPIO UART)
"""

import asyncio
import logging
import serial
from typing import Optional, Callable, List, Union
from pathlib import Path

from enocean_packet import EnOceanPacket, RadioPacket, RawPacketBuffer
from enocean_constants import PacketType

logger = logging.getLogger(__name__)


class EnOceanCommunicator:
    """
    Manages serial communication with EnOcean stick
    Supports both USB (/dev/ttyUSB*) and GPIO UART (/dev/ttyAMA0, /dev/serial0)
    """

    # Serial communication parameters
    BAUDRATE = 57600
    TIMEOUT = 1

    # Connection modes
    MODE_USB = 'usb'
    MODE_GPIO_UART = 'gpio'
    MODE_AUTO = 'auto'

    def __init__(self, port: str = 'auto', mode: str = 'auto'):
        """
        Initialize EnOcean communicator

        Args:
            port: Serial port (/dev/ttyUSB0, /dev/ttyAMA0, or 'auto')
            mode: Connection mode ('usb', 'gpio', 'auto')
        """
        self.port = port
        self.mode = mode
        self.serial: Optional[serial.Serial] = None
        self.base_id: Optional[bytes] = None
        self.packet_buffer = RawPacketBuffer()
        self.running = False
        self.packet_callbacks: List[Callable] = []
        self.connection_type = None  # Will be set during init
        self.retry_count = 0
        self.max_retries = 5
        self.retry_delay = 2  # seconds

    async def initialize(self) -> bool:
        """Initialize serial connection with retry logic"""
        try:
            logger.info(f"🔌 Initializing EnOcean communicator (mode: {self.mode})")

            # Determine connection type
            if self.mode == 'auto':
                self.connection_type = self._detect_connection_type()
            else:
                self.connection_type = self.mode

            logger.info(f"📡 Connection type: {self.connection_type}")

            # Detect port if auto
            if self.port == 'auto':
                self.port = self._detect_port()

            # Try to connect with retry logic
            for attempt in range(self.max_retries):
                try:
                    # Check if port exists
                    if not Path(self.port).exists():
                        logger.error(f"❌ Serial port {self.port} not found")
                        logger.info("ℹ️  Available options:")
                        logger.info("   USB: /dev/ttyUSB*")
                        logger.info("   GPIO UART: /dev/ttyAMA0, /dev/serial0")
                        
                        if attempt < self.max_retries - 1:
                            logger.info(f"⏳ Retrying in {self.retry_delay}s...")
                            await asyncio.sleep(self.retry_delay)
                            continue
                        return False

                    # Open serial port
                    self.serial = serial.Serial(
                        port=self.port,
                        baudrate=self.BAUDRATE,
                        timeout=self.TIMEOUT,
                        write_timeout=self.TIMEOUT
                    )

                    conn_desc = f"GPIO UART" if self.connection_type == self.MODE_GPIO_UART else "USB"
                    logger.info(f"✅ Serial port opened: {self.port} ({conn_desc}) @ {self.BAUDRATE} baud")

                    # Get base ID and other controller info
                    if not await self.get_base_id():
                        logger.warning(f"⚠️  Failed to get base ID (attempt {attempt + 1}/{self.max_retries})")
                        
                        if self.serial:
                            self.serial.close()
                            self.serial = None
                        
                        if attempt < self.max_retries - 1:
                            await asyncio.sleep(self.retry_delay)
                            continue
                        
                        logger.error("❌ Failed to get base ID after retries")
                        return False

                    logger.info(f"✅ Controller Base ID: {self.base_id.hex().upper()}")
                    self.running = True
                    self.retry_count = 0
                    return True

                except serial.SerialException as e:
                    logger.warning(f"⚠️  Serial error (attempt {attempt + 1}/{self.max_retries}): {e}")
                    
                    if self.serial:
                        try:
                            self.serial.close()
                        except:
                            pass
                        self.serial = None
                    
                    if attempt < self.max_retries - 1:
                        await asyncio.sleep(self.retry_delay)
                        continue
                    
                    logger.error("❌ Serial connection failed after retries")
                    return False

            return False

        except Exception as e:
            logger.error(f"❌ Initialization error: {e}")
            return False

    def _detect_connection_type(self) -> str:
        """Auto-detect connection type (USB or GPIO)"""
        # Check GPIO UART first
        gpio_paths = ['/dev/ttyAMA0', '/dev/serial0', '/dev/ttyS0']
        for path in gpio_paths:
            if Path(path).exists():
                logger.info(f"✅ Detected GPIO UART: {path}")
                self.port = path
                return self.MODE_GPIO_UART

        # Check USB
        try:
            import glob
            usb_ports = glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*')
            if usb_ports:
                logger.info(f"✅ Detected USB: {usb_ports[0]}")
                self.port = usb_ports[0]
                return self.MODE_USB
        except:
            pass

        logger.warning("⚠️  No EnOcean stick detected, assuming USB")
        return self.MODE_USB

    def _detect_port(self) -> str:
        """Auto-detect available serial port"""
        # Check GPIO UART
        gpio_paths = ['/dev/ttyAMA0', '/dev/serial0', '/dev/ttyS0']
        for path in gpio_paths:
            if Path(path).exists():
                return path

        # Check USB
        try:
            import glob
            usb_ports = glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*')
            if usb_ports:
                return usb_ports[0]
        except:
            pass

        # Default
        return '/dev/ttyUSB0'

    async def get_base_id(self) -> bool:
        """Request base ID from controller"""
        try:
            # Request version info
            version_request = bytes([0xAA, 0x00, 0x05, 0x05, 0x70, 0x01, 0x80])

            self.serial.write(version_request)
            await asyncio.sleep(0.1)

            # Read response
            response = self.serial.read(30)
            if len(response) >= 13:
                # Base ID is typically at offset 6-9
                self.base_id = response[7:11]
                return True

            logger.warning("⚠️  Could not parse base ID from response")
            return False

        except Exception as e:
            logger.error(f"❌ Error getting base ID: {e}")
            return False

    async def receive_loop(self):
        """Main receive loop - continuously reads from serial port"""
        logger.info("📥 Starting receive loop")

        while self.running:
            try:
                if self.serial and self.serial.in_waiting > 0:
                    # Read available data
                    data = self.serial.read(self.serial.in_waiting)
                    self.packet_buffer.add_data(data)

                    # Try to extract complete packets
                    while True:
                        packet_data = self.packet_buffer.extract_packet()
                        if not packet_data:
                            break

                        # Parse packet
                        packet = EnOceanPacket.parse_packet(packet_data)
                        if packet:
                            logger.debug(f"📦 Received packet: {packet}")
                            await self._dispatch_packet(packet)
                        else:
                            logger.debug("⚠️  Failed to parse packet")

                await asyncio.sleep(0.01)  # Prevent busy waiting

            except Exception as e:
                logger.error(f"❌ Error in receive loop: {e}")
                await asyncio.sleep(1)

    async def send_packet(self, packet: RadioPacket) -> bool:
        """Send a radio packet"""
        try:
            if not self.serial:
                logger.error("❌ Serial port not open")
                return False

            # Build ESP3 packet
            esp3_packet = EnOceanPacket.create_radio_packet(
                rorg=packet.rorg,
                data=packet.data,
                sender_addr=packet.sender_addr,
                destination_addr=packet.destination_addr,
                repeater_count=packet.repeater_count,
                learn=packet.learn,
                command=packet.command
            )

            logger.debug(f"📤 Sending packet: {esp3_packet.hex()}")
            self.serial.write(esp3_packet)

            # Wait for response
            await asyncio.sleep(0.1)

            logger.info(f"✅ Packet sent successfully")
            return True

        except Exception as e:
            logger.error(f"❌ Error sending packet: {e}")
            return False

    def add_packet_callback(self, callback: Callable):
        """Register a callback for received packets"""
        self.packet_callbacks.append(callback)

    async def _dispatch_packet(self, packet: RadioPacket):
        """Dispatch received packet to all registered callbacks"""
        for callback in self.packet_callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(packet)
                else:
                    callback(packet)
            except Exception as e:
                logger.error(f"❌ Error in packet callback: {e}")

    def stop(self):
        """Stop the communicator"""
        logger.info("🛑 Stopping EnOcean communicator")
        self.running = False

        if self.serial:
            try:
                self.serial.close()
                logger.info("✅ Serial port closed")
            except Exception as e:
                logger.error(f"❌ Error closing serial port: {e}")
