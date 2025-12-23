"""
Home Assistant Native Entities
Implements native HA entities for Ventilairsec2HA with MQTT Discovery
"""

import asyncio
import logging
import json
from typing import Optional, Dict, Any
from datetime import datetime

try:
    import paho.mqtt.client as mqtt
except ImportError:
    mqtt = None

logger = logging.getLogger(__name__)


class HAEntity:
    """Base class for Home Assistant entities"""

    def __init__(
        self,
        device_id: str,
        entity_id: str,
        name: str,
        entity_type: str,
        mqtt_client: mqtt.Client,
        config: Dict[str, Any],
    ):
        self.device_id = device_id
        self.entity_id = entity_id
        self.name = name
        self.entity_type = entity_type
        self.mqtt_client = mqtt_client
        self.config = config
        self.state = None
        self.attributes = {}

    def get_discovery_topic(self) -> str:
        """Get MQTT Discovery topic for this entity"""
        return f"homeassistant/{self.entity_type}/{self.device_id}/{self.entity_id}/config"

    def get_state_topic(self) -> str:
        """Get MQTT state topic"""
        return f"ventilairsec2ha/{self.device_id}/{self.entity_id}/state"

    def get_command_topic(self) -> str:
        """Get MQTT command topic (for controllable entities)"""
        return f"ventilairsec2ha/{self.device_id}/{self.entity_id}/set"

    def publish_discovery(self):
        """Publish MQTT Discovery message"""
        if not self.mqtt_client:
            return

        discovery_topic = self.get_discovery_topic()
        payload = self.get_discovery_payload()

        try:
            self.mqtt_client.publish(discovery_topic, json.dumps(payload), retain=True)
            logger.info(f"✅ Published discovery for {self.name} to {discovery_topic}")
        except Exception as e:
            logger.error(f"❌ Failed to publish discovery for {self.name}: {e}")

    def get_discovery_payload(self) -> Dict[str, Any]:
        """Override in subclasses to provide specific discovery payload"""
        return {
            "name": self.name,
            "state_topic": self.get_state_topic(),
            "unique_id": f"ventilairsec2ha_{self.device_id}_{self.entity_id}",
            "device": {
                "identifiers": [f"ventilairsec2ha_{self.device_id}"],
                "name": f"Ventilairsec2HA {self.device_id}",
                "manufacturer": "Ventilairsec2HA",
                "model": "Purevent Ventilairsec",
            },
        }

    def publish_state(self, state: Any, attributes: Optional[Dict] = None):
        """Publish entity state"""
        if not self.mqtt_client:
            return

        self.state = state
        if attributes:
            self.attributes.update(attributes)

        state_topic = self.get_state_topic()

        try:
            self.mqtt_client.publish(state_topic, json.dumps({"state": state}), retain=True)
        except Exception as e:
            logger.error(f"❌ Failed to publish state for {self.name}: {e}")


class HAClimate(HAEntity):
    """Home Assistant Climate Entity (VMI Control)"""

    def __init__(self, device_id: str, mqtt_client: mqtt.Client, config: Dict[str, Any]):
        super().__init__(
            device_id=device_id,
            entity_id="vmi_climate",
            name="VMI Ventilation Control",
            entity_type="climate",
            mqtt_client=mqtt_client,
            config=config,
        )

    def get_discovery_payload(self) -> Dict[str, Any]:
        """Climate entity discovery payload"""
        payload = super().get_discovery_payload()
        payload.update(
            {
                "modes": ["off", "low", "medium", "high", "auto"],
                "mode_state_topic": self.get_state_topic(),
                "mode_command_topic": self.get_command_topic(),
                "current_temperature_topic": self.get_state_topic(),
                "temperature_unit": "C",
                "min_temp": 0,
                "max_temp": 4,
                "precision": 1,
            }
        )
        return payload


class HASensor(HAEntity):
    """Home Assistant Sensor Entity"""

    def __init__(
        self,
        device_id: str,
        entity_id: str,
        name: str,
        mqtt_client: mqtt.Client,
        config: Dict[str, Any],
        unit_of_measurement: Optional[str] = None,
        device_class: Optional[str] = None,
    ):
        super().__init__(
            device_id=device_id,
            entity_id=entity_id,
            name=name,
            entity_type="sensor",
            mqtt_client=mqtt_client,
            config=config,
        )
        self.unit_of_measurement = unit_of_measurement
        self.device_class = device_class

    def get_discovery_payload(self) -> Dict[str, Any]:
        """Sensor entity discovery payload"""
        payload = super().get_discovery_payload()
        if self.unit_of_measurement:
            payload["unit_of_measurement"] = self.unit_of_measurement
        if self.device_class:
            payload["device_class"] = self.device_class
        return payload


class HASelect(HAEntity):
    """Home Assistant Select Entity (for discrete options)"""

    def __init__(
        self,
        device_id: str,
        entity_id: str,
        name: str,
        mqtt_client: mqtt.Client,
        config: Dict[str, Any],
        options: list,
    ):
        super().__init__(
            device_id=device_id,
            entity_id=entity_id,
            name=name,
            entity_type="select",
            mqtt_client=mqtt_client,
            config=config,
        )
        self.options = options

    def get_discovery_payload(self) -> Dict[str, Any]:
        """Select entity discovery payload"""
        payload = super().get_discovery_payload()
        payload.update(
            {
                "options": self.options,
                "command_topic": self.get_command_topic(),
            }
        )
        return payload


class HAEntityManager:
    """Manages Home Assistant entities with MQTT Discovery"""

    def __init__(self, mqtt_client: mqtt.Client, config: Dict[str, Any]):
        self.mqtt_client = mqtt_client
        self.config = config
        self.entities: Dict[str, HAEntity] = {}

    def create_vmi_entities(self, device_id: str = "0421574F"):
        """Create entities for VMI Purevent"""
        # Climate entity for VMI control
        climate = HAClimate(device_id, self.mqtt_client, self.config)
        self.entities["vmi_climate"] = climate
        climate.publish_discovery()

        # VMI Status sensor
        vmi_status = HASensor(
            device_id=device_id,
            entity_id="vmi_status",
            name="VMI Status",
            mqtt_client=self.mqtt_client,
            config=self.config,
            device_class="enum",
        )
        self.entities["vmi_status"] = vmi_status
        vmi_status.publish_discovery()

        # VMI Temperature sensor
        vmi_temp = HASensor(
            device_id=device_id,
            entity_id="vmi_temperature",
            name="VMI Temperature",
            mqtt_client=self.mqtt_client,
            config=self.config,
            unit_of_measurement="°C",
            device_class="temperature",
        )
        self.entities["vmi_temperature"] = vmi_temp
        vmi_temp.publish_discovery()

        # VMI Error sensor
        vmi_error = HASensor(
            device_id=device_id,
            entity_id="vmi_error",
            name="VMI Error Code",
            mqtt_client=self.mqtt_client,
            config=self.config,
        )
        self.entities["vmi_error"] = vmi_error
        vmi_error.publish_discovery()

        logger.info(f"✅ Created {len([e for e in self.entities if 'vmi' in e])} VMI entities")

    def create_sensor_entities(self, device_id: str, sensor_type: str):
        """Create entities for CO2 or Temperature/Humidity sensors"""
        if sensor_type == "co2":
            co2 = HASensor(
                device_id=device_id,
                entity_id="co2_level",
                name="CO2 Level",
                mqtt_client=self.mqtt_client,
                config=self.config,
                unit_of_measurement="ppm",
                device_class="carbon_dioxide",
            )
            self.entities[f"co2_{device_id}"] = co2
            co2.publish_discovery()

        elif sensor_type == "temp_humidity":
            temp = HASensor(
                device_id=device_id,
                entity_id="temperature",
                name="Temperature",
                mqtt_client=self.mqtt_client,
                config=self.config,
                unit_of_measurement="°C",
                device_class="temperature",
            )
            self.entities[f"temp_{device_id}"] = temp
            temp.publish_discovery()

            humidity = HASensor(
                device_id=device_id,
                entity_id="humidity",
                name="Humidity",
                mqtt_client=self.mqtt_client,
                config=self.config,
                unit_of_measurement="%",
                device_class="humidity",
            )
            self.entities[f"humidity_{device_id}"] = humidity
            humidity.publish_discovery()

        logger.info(f"✅ Created entities for {sensor_type} sensor {device_id}")

    def publish_state(self, entity_key: str, state: Any, attributes: Optional[Dict] = None):
        """Publish state for an entity"""
        if entity_key in self.entities:
            self.entities[entity_key].publish_state(state, attributes)

    def get_entity(self, entity_key: str) -> Optional[HAEntity]:
        """Get entity by key"""
        return self.entities.get(entity_key)
