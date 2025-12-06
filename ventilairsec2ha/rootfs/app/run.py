"""
Ventilairsec2HA - Home Assistant Addon for Purevent Ventilairsec VMI via EnOcean
Main application entry point
"""

import logging
import sys
import json
import os
import signal
import asyncio
from pathlib import Path
from typing import Optional, Dict, Any

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import addon modules
from config import Config
from enocean_communicator import EnOceanCommunicator
from ventilairsec_manager import VentilairsecManager
from home_assistant_integration import HomeAssistantIntegration
from webui_server import WebUIServer


class VentilairsecHA:
    """Main application class for Ventilairsec2HA addon"""
    
    def __init__(self):
        self.config: Optional[Config] = None
        self.communicator: Optional[EnOceanCommunicator] = None
        self.ventilairsec_manager: Optional[VentilairsecManager] = None
        self.ha_integration: Optional[HomeAssistantIntegration] = None
        self.webui_server: Optional[WebUIServer] = None
        self.running = False
        
    async def initialize(self) -> bool:
        """Initialize all components"""
        try:
            logger.info("🚀 Initializing Ventilairsec2HA addon...")
            
            # Load configuration
            self.config = Config()
            if not self.config.load():
                logger.error("❌ Failed to load configuration")
                return False
            logger.info(f"✅ Configuration loaded: serial_port={self.config.serial_port}")
            
            # Initialize EnOcean communicator
            self.communicator = EnOceanCommunicator(
                port=self.config.serial_port,
                mode=self.config.connection_mode
            )
            if not await self.communicator.initialize():
                logger.error("❌ Failed to initialize EnOcean communicator")
                return False
            logger.info(f"✅ EnOcean communicator initialized ({self.communicator.connection_type})")
            
            # Initialize Ventilairsec manager
            self.ventilairsec_manager = VentilairsecManager(self.communicator)
            logger.info("✅ Ventilairsec manager initialized")
            
            # Initialize Home Assistant integration
            if self.config.enable_mqtt:
                self.ha_integration = HomeAssistantIntegration(
                    self.config,
                    self.communicator,
                    self.ventilairsec_manager
                )
                if not await self.ha_integration.initialize():
                    logger.warning("⚠️  Failed to initialize Home Assistant integration")
            
            # Initialize WebUI server
            self.webui_server = WebUIServer(
                self.config,
                self.communicator,
                self.ventilairsec_manager
            )
            if not await self.webui_server.start():
                logger.warning("⚠️  Failed to start WebUI server")
            
            logger.info("✅ All components initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Initialization error: {e}", exc_info=True)
            return False
    
    async def run(self):
        """Main run loop"""
        self.running = True
        logger.info("📡 Starting main loop...")
        
        try:
            # Register signal handlers
            loop = asyncio.get_event_loop()
            loop.add_signal_handler(signal.SIGTERM, self.shutdown)
            loop.add_signal_handler(signal.SIGINT, self.shutdown)
            
            # Start receivers
            tasks = [
                self.communicator.receive_loop(),
                self.ventilairsec_manager.processing_loop()
            ]
            
            if self.ha_integration:
                tasks.append(self.ha_integration.publish_loop())
            
            if self.webui_server:
                tasks.append(self.webui_server.server_loop())
            
            # Run all tasks concurrently
            await asyncio.gather(*tasks)
            
        except Exception as e:
            logger.error(f"❌ Runtime error: {e}", exc_info=True)
        finally:
            await self.shutdown()
    
    def shutdown(self):
        """Shutdown handler"""
        logger.info("🛑 Shutting down...")
        self.running = False
        
        if self.communicator:
            self.communicator.stop()
        if self.ha_integration:
            asyncio.create_task(self.ha_integration.close())
        if self.webui_server:
            asyncio.create_task(self.webui_server.stop())
        
        logger.info("✅ Shutdown complete")


async def main():
    """Application entry point"""
    app = VentilairsecHA()
    
    if not await app.initialize():
        logger.error("Initialization failed, exiting")
        sys.exit(1)
    
    await app.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
