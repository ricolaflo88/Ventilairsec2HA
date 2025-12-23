"""
Home Assistant Integration Module
Publishes device states to Home Assistant via MQTT with Discovery
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

from ha_entities import HAEntityManager

logger = logging.getLogger(__name__)


class HomeAssistantIntegration:
    """Integrates with Home Assistant via MQTT with Discovery"""

    def __init__(self, config, communicator, ventilairsec_manager):
        self.config = config
        self.communicator = communicator
        self.ventilairsec_manager = ventilairsec_manager

        self.client: Optional[mqtt.Client] = None
        self.entity_manager: Optional[HAEntityManager] = None
        self.connected = False
        self.running = False

        if not mqtt:
            logger.warning("⚠️  paho-mqtt not available, MQTT disabled")

    async def initialize(self) -> bool:
        """Initialize MQTT connection and Home Assistant entities"""
        try:
            if not mqtt:
                logger.warning("⚠️  MQTT library not available")
                return False

            logger.info(f"🔗 Connecting to MQTT broker: {self.config.mqtt_broker}:{self.config.mqtt_port}")

            # Create MQTT client with retry
            self.client = mqtt.Client(
                client_id="ventilairsec2ha",
                protocol=mqtt.MQTTv311,
                clean_session=True
            )

            # Set callbacks
            self.client.on_connect = self._on_mqtt_connect
            self.client.on_disconnect = self._on_mqtt_disconnect
            self.client.on_message = self._on_mqtt_message

            # Create entity manager
            self.entity_manager = HAEntityManager(self.client, self.config)

            # Connect with retry logic
            max_retries = 5
            for attempt in range(max_retries):
                try:
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

                            # Create HA entities with MQTT Discovery
                            await self._setup_ha_entities()

                            return True
                        await asyncio.sleep(0.1)

                    # Connection timeout, try again
                    self.client.loop_stop()

                except Exception as e:
                    logger.warning(f"⚠️  Connection attempt {attempt + 1}/{max_retries} failed: {e}")
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff

            logger.error("❌ Failed to connect to MQTT broker after retries")
            return False

        except Exception as e:
            logger.error(f"❌ MQTT initialization error: {e}")
            return False

    async def _setup_ha_entities(self):
        """Setup Home Assistant entities with MQTT Discovery"""
        try:
            # Create VMI entity
            self.entity_manager.create_vmi_entities()

            # Create sensor entities for known devices
            sensor_devices = {
                '81003227': 'co2',
                '810054F5': 'temp_humidity'
            }

            for device_id, sensor_type in sensor_devices.items():
                self.entity_manager.create_sensor_entities(device_id, sensor_type)

            logger.info("✅ Home Assistant entities configured with MQTT Discovery")

        except Exception as e:
            logger.error(f"❌ Error setting up HA entities: {e}")

    def _on_mqtt_connect(self, client, userdata, flags, rc):
        """MQTT connect callback"""
        if rc == 0:
            logger.info("✅ MQTT Connected")
            self.connected = True

            # Subscribe to command topics
            self.client.subscribe("ventilairsec2ha/+/+/set")
            self.client.subscribe("homeassistant/ventilairsec2ha/command/#")
        else:
            logger.error(f"❌ MQTT Connection failed with code: {rc}")
            self.connected = False

    def _on_mqtt_disconnect(self, client, userdata, rc):
        """MQTT disconnect callback"""
        self.connected = False
        if rc != 0:
            logger.warning(f"⚠️  Unexpected MQTT disconnect: {rc}")

    def _on_mqtt_message(self, client, userdata, msg):
        """MQTT message callback for commands"""
        try:
            logger.debug(f"📥 MQTT message: {msg.topic} = {msg.payload}")

            # Parse command topic: ventilairsec2ha/{device_id}/{entity_id}/set
            parts = msg.topic.split('/')
            if len(parts) >= 4 and parts[-1] == 'set':
                device_id = parts[1]
                entity_id = parts[2]
                payload = msg.payload.decode('utf-8').strip()

                # Handle VMI speed control
                if entity_id == 'vmi_climate' and device_id == '0421574F':
                    try:
                        # Parse speed from payload (0-4)
                        speed_map = {
                            'off': 0,
                            'low': 1,
                            'medium': 2,
                            'high': 3,
                            'auto': 4
                        }
                        speed = speed_map.get(payload.lower(), int(payload))
                        asyncio.create_task(
                            self.ventilairsec_manager.set_vmi_speed(speed)
                        )
                        logger.info(f"✅ Set VMI speed to {speed}")
                    except ValueError:
                        logger.error(f"❌ Invalid speed value: {payload}")

        except Exception as e:
            logger.error(f"❌ Error handling MQTT message: {e}")

    async def publish_loop(self):
        """Main publish loop - continuously publishes device states to MQTT"""
        self.running = True
        logger.info("📤 Starting MQTT publish loop")

        while self.running:
            try:
                if self.connected and self.entity_manager:
                    # Get current device states from manager
                    devices = self.ventilairsec_manager.devices

                    for device_addr, device_state in devices.items():
                        try:
                            # Publish VMI state
                            if device_addr.upper() == '0421574F':
                                # Climate state
                                speed = device_state.data.get('speed', 0)
                                self.entity_manager.publish_state(
                                    'vmi_climate',
                                    speed,
                                    {'last_update': datetime.now().isoformat()}
                                )

                                # Temperature
                                if 'temperature' in device_state.data:
                                    self.entity_manager.publish_state(
                                        'vmi_temperature',
                                        device_state.data['temperature']
                                    )

                                # Status
                                if 'status' in device_state.data:
                                    self.entity_manager.publish_state(
                                        'vmi_status',
                                        device_state.data['status']
                                    )

                            # Publish CO2 sensor state
                            elif device_addr.upper() == '81003227':
                                if 'co2' in device_state.data:
                                    self.entity_manager.publish_state(
                                        f"co2_{device_addr}",
                                        device_state.data['co2']
                                    )

                            # Publish Temperature/Humidity sensor state
                            elif device_addr.upper() == '810054F5':
                                if 'temperature' in device_state.data:
                                    self.entity_manager.publish_state(
                                        f"temp_{device_addr}",
                                        device_state.data['temperature']
                                    )
                                if 'humidity' in device_state.data:
                                    self.entity_manager.publish_state(
                                        f"humidity_{device_addr}",
                                        device_state.data['humidity']
                                    )

                        except Exception as e:
                            logger.error(f"❌ Error publishing state for {device_addr}: {e}")

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
