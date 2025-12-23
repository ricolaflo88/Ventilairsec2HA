"""Constants for Ventilairsec2HA integration."""

DOMAIN = "ventilairsec2ha"
DEFAULT_NAME = "Ventilairsec2"
DEFAULT_POLL_INTERVAL = 60

# Configuration keys
CONF_DEVICE_NAME = "device_name"
CONF_DEVICE_ADDRESS = "device_address"
CONF_DEVICE_TYPE = "device_type"
CONF_PORT = "port"
CONF_SENSORS = "sensors"

# Device types
DEVICE_TYPE_VMI = "VMI"
DEVICE_TYPE_SENSOR = "Sensor"

# Attributes
ATTR_DEVICE_ID = "device_id"
ATTR_DEVICE_TYPE = "device_type"
ATTR_RSSI = "rssi"
ATTR_BATTERY = "battery"

# Entity IDs
ENTITY_ID_FORMAT = "{}.{{}}".format(DOMAIN)

# Services
SERVICE_SEND_COMMAND = "send_command"
SERVICE_PAIR_DEVICE = "pair_device"

# Enocean EEP profiles
EEP_TEMPERATURE = "A5-09-04"
EEP_PRESENCE = "D5-00-01"
EEP_HUMIDITY = "A5-04-01"

# Data storage
DATA_VENTILAIRSEC = f"{DOMAIN}_data"
DATA_COORDINATOR = f"{DOMAIN}_coordinator"
