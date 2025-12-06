"""
Configuration management for Ventilairsec2HA addon
Loads options from Home Assistant add-on configuration
"""

import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class Config:
    """Configuration handler for the addon"""

    DEFAULT_CONFIG = {
        'connection_mode': 'auto',
        'serial_port': 'auto',
        'log_level': 'info',
        'enable_mqtt': True,
        'mqtt_broker': 'mosquitto',
        'mqtt_port': 1883,
        'mqtt_username': '',
        'mqtt_password': '',
        'webui_port': 8080
    }

    def __init__(self, config_path: str = '/data/options.json'):
        self.config_path = Path(config_path)
        self.config: Dict[str, Any] = self.DEFAULT_CONFIG.copy()
        self.connection_mode: str = self.DEFAULT_CONFIG['connection_mode']
        self.serial_port: str = self.DEFAULT_CONFIG['serial_port']
        self.log_level: str = self.DEFAULT_CONFIG['log_level']
        self.enable_mqtt: bool = self.DEFAULT_CONFIG['enable_mqtt']
        self.mqtt_broker: str = self.DEFAULT_CONFIG['mqtt_broker']
        self.mqtt_port: int = self.DEFAULT_CONFIG['mqtt_port']
        self.mqtt_username: str = self.DEFAULT_CONFIG['mqtt_username']
        self.mqtt_password: str = self.DEFAULT_CONFIG['mqtt_password']
        self.webui_port: int = self.DEFAULT_CONFIG['webui_port']

    def load(self) -> bool:
        """Load configuration from file"""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r') as f:
                    user_config = json.load(f)
                    self.config.update(user_config)
                logger.info(f"✅ Configuration loaded from {self.config_path}")
            else:
                logger.warning(f"⚠️  Configuration file not found at {self.config_path}, using defaults")

            # Update instance attributes
            self.connection_mode = self.config.get('connection_mode', self.DEFAULT_CONFIG['connection_mode'])
            self.serial_port = self.config.get('serial_port', self.DEFAULT_CONFIG['serial_port'])
            self.log_level = self.config.get('log_level', self.DEFAULT_CONFIG['log_level'])
            self.enable_mqtt = self.config.get('enable_mqtt', self.DEFAULT_CONFIG['enable_mqtt'])
            self.mqtt_broker = self.config.get('mqtt_broker', self.DEFAULT_CONFIG['mqtt_broker'])
            self.mqtt_port = self.config.get('mqtt_port', self.DEFAULT_CONFIG['mqtt_port'])
            self.mqtt_username = self.config.get('mqtt_username', '')
            self.mqtt_password = self.config.get('mqtt_password', '')
            self.webui_port = self.config.get('webui_port', 8080)

            # Set logging level
            log_level = getattr(logging, self.log_level.upper(), logging.INFO)
            logging.getLogger().setLevel(log_level)

            return True
        except Exception as e:
            logger.error(f"❌ Failed to load configuration: {e}")
            return False

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)

    def __repr__(self) -> str:
        return f"Config(mode={self.connection_mode}, port={self.serial_port}, mqtt={self.enable_mqtt}, webui_port={self.webui_port})"
