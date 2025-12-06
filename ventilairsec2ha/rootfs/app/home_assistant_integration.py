"""
Home Assistant Integration Module
Publishes device states to Home Assistant via MQTT
"""

import asyncio
import logging
import json
from typing import Optional
from datetime import datetime

try:
    import paho.mqtt.client as mqtt
except ImportError:
    mqtt = None

logger = logging.getLogger(__name__)


class HomeAssistantIntegration:
    """Integrates with Home Assistant via MQTT"""
    
    def __init__(self, config, communicator, ventilairsec_manager):
        self.config = config
        self.communicator = communicator
        self.ventilairsec_manager = ventilairsec_manager
        
        self.client: Optional[mqtt.Client] = None
        self.connected = False
        self.running = False
        
        if not mqtt:
            logger.warning("⚠️  paho-mqtt not available, MQTT disabled")
    
    async def initialize(self) -> bool:
        """Initialize MQTT connection"""
        try:
            if not mqtt:
                logger.warning("⚠️  MQTT library not available")
                return False
            
            logger.info(f"🔗 Connecting to MQTT broker: {self.config.mqtt_broker}:{self.config.mqtt_port}")
            
            # Create MQTT client
            self.client = mqtt.Client(
                client_id="ventilairsec2ha",
                protocol=mqtt.MQTTv31
            )
            
            # Set callbacks
            self.client.on_connect = self._on_mqtt_connect
            self.client.on_disconnect = self._on_mqtt_disconnect
            self.client.on_message = self._on_mqtt_message
            
            # Connect
            self.client.connect(
                self.config.mqtt_broker,
                self.config.mqtt_port,
                keepalive=60
            )
            
            self.client.loop_start()
            
            # Wait for connection
            for _ in range(30):
                if self.connected:
                    logger.info("✅ Connected to MQTT broker")
                    return True
                await asyncio.sleep(0.1)
            
            logger.error("❌ Failed to connect to MQTT broker")
            return False
            
        except Exception as e:
            logger.error(f"❌ MQTT initialization error: {e}")
            return False
    
    def _on_mqtt_connect(self, client, userdata, flags, rc):
        """MQTT connect callback"""
        if rc == 0:
            logger.info("✅ MQTT Connected")
            self.connected = True
            
            # Subscribe to command topics
            self.client.subscribe("homeassistant/ventilairsec2ha/command/#")
        else:
            logger.error(f"❌ MQTT Connection failed: {rc}")
            self.connected = False
    
    def _on_mqtt_disconnect(self, client, userdata, rc):
        """MQTT disconnect callback"""
        self.connected = False
        if rc != 0:
            logger.warning(f"⚠️  Unexpected MQTT disconnect: {rc}")
    
    def _on_mqtt_message(self, client, userdata, msg):
        """MQTT message callback"""
        try:
            logger.debug(f"📥 MQTT message: {msg.topic} = {msg.payload}")
            
            # Parse command topic
            parts = msg.topic.split('/')
            if len(parts) >= 4:
                command = parts[-1]
                payload = msg.payload.decode('utf-8')
                
                # Handle commands
                if command == 'set_speed':
                    speed = int(payload)
                    asyncio.create_task(self.ventilairsec_manager.set_vmi_speed(speed))
        
        except Exception as e:
            logger.error(f"❌ Error handling MQTT message: {e}")
    
    async def publish_loop(self):
        """Main publish loop - continuously publishes device states"""
        self.running = True
        logger.info("📤 Starting MQTT publish loop")
        
        while self.running:
            try:
                if self.connected:
                    # Get current device states
                    states = self.ventilairsec_manager.get_device_states()
                    
                    # Publish each device state
                    for device_addr, state in states.items():
                        topic = f"homeassistant/ventilairsec2ha/state/{device_addr}"
                        payload = json.dumps(state)
                        
                        self.client.publish(topic, payload, qos=1)
                        logger.debug(f"📤 Published: {topic}")
                
                # Publish every 10 seconds
                await asyncio.sleep(10)
                
            except Exception as e:
                logger.error(f"❌ Error in publish loop: {e}")
                await asyncio.sleep(5)
    
    async def close(self):
        """Close MQTT connection"""
        logger.info("🛑 Closing MQTT connection")
        self.running = False
        
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()
