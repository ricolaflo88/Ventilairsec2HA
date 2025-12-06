"""
GPIO Serial Communication for Raspberry Pi
Handles UART communication over GPIO pins (RXD/TXD)
"""

import logging
import asyncio
import serial
from typing import Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class GPIOSerialCommunicator:
    """
    Manages UART communication over GPIO pins
    Typically RXD on GPIO 15 (pin 10) and TXD on GPIO 14 (pin 8)
    """

    # GPIO UART device paths (for Raspberry Pi)
    GPIO_UART_PATHS = [
        '/dev/ttyAMA0',    # Primary UART (GPIO 14/15)
        '/dev/serial0',    # Alias for primary UART
        '/dev/ttyS0',      # Mini UART (GPIO 32/33, Pi 5 only)
    ]

    BAUDRATE = 57600
    TIMEOUT = 1

    def __init__(self, port: Optional[str] = None):
        """
        Initialize GPIO UART communicator

        Args:
            port: Specific port (e.g., /dev/ttyAMA0) or auto-detect
        """
        self.port = port or self._detect_gpio_uart()
        self.serial: Optional[serial.Serial] = None
        self.running = False

    @staticmethod
    def _detect_gpio_uart() -> str:
        """Auto-detect available GPIO UART port"""
        for path in GPIOSerialCommunicator.GPIO_UART_PATHS:
            if Path(path).exists():
                logger.info(f"✅ Detected GPIO UART at {path}")
                return path

        logger.warning("⚠️  No GPIO UART detected, trying default")
        return GPIOSerialCommunicator.GPIO_UART_PATHS[0]

    async def initialize(self) -> bool:
        """Initialize GPIO UART connection"""
        try:
            logger.info(f"🔌 Initializing GPIO UART on {self.port}")

            # Check if port exists
            if not Path(self.port).exists():
                logger.error(f"❌ GPIO UART port {self.port} not found")
                logger.info("ℹ️  Available ports:")
                for path in self.GPIO_UART_PATHS:
                    status = "✅" if Path(path).exists() else "❌"
                    logger.info(f"   {status} {path}")
                return False

            # Open serial port
            self.serial = serial.Serial(
                port=self.port,
                baudrate=self.BAUDRATE,
                timeout=self.TIMEOUT,
                write_timeout=self.TIMEOUT
            )

            logger.info(f"✅ GPIO UART opened: {self.port} @ {self.BAUDRATE} baud")
            self.running = True
            return True

        except serial.SerialException as e:
            logger.error(f"❌ Serial port error: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Initialization error: {e}")
            return False

    def is_connected(self) -> bool:
        """Check if GPIO UART is connected"""
        return self.serial is not None and self.serial.is_open

    def write(self, data: bytes) -> bool:
        """Write data to GPIO UART"""
        try:
            if not self.is_connected():
                logger.error("❌ GPIO UART not connected")
                return False

            self.serial.write(data)
            return True
        except Exception as e:
            logger.error(f"❌ Error writing to GPIO UART: {e}")
            return False

    def read(self, size: int = 1024) -> bytes:
        """Read data from GPIO UART"""
        try:
            if not self.is_connected():
                return b''

            data = self.serial.read(size)
            return data
        except Exception as e:
            logger.error(f"❌ Error reading from GPIO UART: {e}")
            return b''

    @property
    def in_waiting(self) -> int:
        """Get number of bytes waiting to be read"""
        try:
            if not self.is_connected():
                return 0
            return self.serial.in_waiting
        except:
            return 0

    def close(self):
        """Close GPIO UART connection"""
        logger.info("🛑 Closing GPIO UART")
        self.running = False

        if self.serial:
            try:
                self.serial.close()
                logger.info("✅ GPIO UART closed")
            except Exception as e:
                logger.error(f"❌ Error closing GPIO UART: {e}")

    def __repr__(self) -> str:
        status = "🟢 Connected" if self.is_connected() else "🔴 Disconnected"
        return f"GPIOSerialCommunicator({self.port}, {status})"
