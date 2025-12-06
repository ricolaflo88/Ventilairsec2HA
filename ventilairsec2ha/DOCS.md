# 📡 Documentation Technique - Ventilairsec2HA

## Table des Matières

1. [Architecture Globale](#architecture-globale)
2. [Protocole EnOcean](#protocole-enocean)
3. [Format des Trames](#format-des-trames)
4. [Appareils Supportés](#appareils-supportés)
5. [Commandes VMI](#commandes-vmi)
6. [Intégration HA](#intégration-ha)

---

## Architecture Globale

### Vue d'ensemble

```
┌─────────────────┐
│  Appareils      │
│  EnOcean        │
│  (Radio)        │
└────────┬────────┘
         │ 868 MHz
         │
    ┌────▼──────────┐
    │  USB Stick    │
    │  (TCM310)     │
    │  EnOcean      │
    └────┬──────────┘
         │ /dev/ttyUSB0
         │
    ┌────▼──────────────────┐
    │  Ventilairsec2HA      │
    │  (Addon HA)           │
    ├───────────────────────┤
    │ ▪ EnOcean Comm.       │
    │ ▪ Packet Parser       │
    │ ▪ Device Manager      │
    │ ▪ MQTT Publisher      │
    │ ▪ WebUI Server        │
    └────┬──────────────────┘
         │
    ┌────▼──────────────────┐
    │  Home Assistant       │
    │  ▪ Entities           │
    │  ▪ Automations        │
    │  ▪ Dashboard          │
    └───────────────────────┘
```

### Structure des Modules Python

```
/app/
├── run.py                        # Point d'entrée principal
├── config.py                     # Gestion configuration
├── enocean_constants.py          # Constantes EnOcean
├── enocean_packet.py             # Parsing des paquets
├── enocean_communicator.py       # Communication série
├── ventilairsec_manager.py       # Gestion VMI & capteurs
├── home_assistant_integration.py # Intégration MQTT
└── webui_server.py              # API WebUI
```

---

## Protocole EnOcean

### Spécifications Générales

| Paramètre       | Valeur                        |
| --------------- | ----------------------------- |
| Fréquence       | 868.3 MHz                     |
| Modulation      | FSK                           |
| Débit           | 125 kbps                      |
| Portée          | ~30m en ligne de vue          |
| Protocole série | ESP3 (900-ESP3)               |
| Vitesse série   | 57600 baud                    |
| Format          | 8 bits, No parity, 1 stop bit |

### Types de Télégrammes (RORG)

| Code | Hex  | Nom                   | Description             |
| ---- | ---- | --------------------- | ----------------------- |
| RPS  | 0xF6 | Repeated Switch       | Switch simple           |
| BS1  | 0xD5 | 1-byte Single Data    | 1 byte de données       |
| BS4  | 0xA5 | 4-byte Variable       | 4 bytes (capteurs)      |
| VLD  | 0xB0 | Variable Length Data  | Données variables       |
| MSC  | 0xD1 | Manufacturer Specific | Spécifique fabricant    |
| UTE  | 0xC6 | Universal Teach-In    | Appairage apprentissage |

---

## Format des Trames

### Structure ESP3 (protocole série)

```
┌─────┬──────────┬─────────┬──────────────┬─────────────────┬──────────┐
│ AA  │ LEN_H LEN_L │ CRC_LEN │ PACKET_TYPE │ DATA              │ CRC_DATA │
├─────┼──────────┼─────────┼──────────────┼─────────────────┼──────────┤
│ 1B  │ 2B       │ 1B      │ 1B           │ Variable (1-255)│ 1B      │
└─────┴──────────┴─────────┴──────────────┴─────────────────┴──────────┘

AA        = 0xAA (frame header)
LEN_H/L   = Length of DATA (big-endian)
CRC_LEN   = CRC of length bytes
PACKET_TYPE = 0x01 (RADIO_ERP1)
DATA      = Payload (voir structure radio ci-dessous)
CRC_DATA  = CRC-8 du DATA
```

### Structure Données Radio (RADIO_ERP1)

```
┌──────┬───────────────────────────┬──────────┬──────────┬──────────┐
│ RORG │ Données                   │ Adresse  │ Statut   │ Checksum │
├──────┼───────────────────────────┼──────────┼──────────┼──────────┤
│ 1B   │ 1-14B (selon RORG)       │ 4B       │ 1B       │ CRC8     │
└──────┴───────────────────────────┴──────────┴──────────┴──────────┘

RORG    = Type de télégramme (0xA5, 0xD1, etc.)
Données = Dépend du RORG et de l'appareil
Adresse = Adresse de l'émetteur (4 bytes)
Statut  = Repeater count, Learn flag, etc.
```

### Byte de Statut

```
Bits:  7  6  5  4  3  2  1  0
       ├─ LEARN (1=Learn, 0=Data)
       │  ├─ Sec.Level
       │  │  ├─ Repeater Error
       │  │  │  └─ Repeater Count (0-15)
```

---

## Appareils Supportés

### 1. VMI Purevent Ventilairsec (D1-07-9F)

**Informations Générales:**

- RORG-FUNC-TYPE: D1-07-9F
- Variante VMI: D1079-01-00 (Addr: 0x0421574F)
- Variante Assistant: D1079-00-00 (Addr: 0x0422407D)
- Type: Manufacturer Specific Command (MSC)

**Structure des Données (4 bytes):**

```
Byte 0: Status/Command
  Bits 7-6: Mode (00=Off, 01=Manual, 10=Auto, 11=Bypass)
  Bits 5-4: Réservé
  Bits 3-0: Commande spécifique

Byte 1: Vitesse/Densité
  0x10: Vitesse Basse (Low)
  0x20: Vitesse Moyenne (Medium)
  0x30: Vitesse Haute (High)
  0x40: Vitesse Max (Max)

Byte 2: Température
  Valeur directe en °C (0-255)

Byte 3-4: Erreurs
  Codification spécifique Purevent (voir table erreurs)
```

**Codes d'Erreur (Byte 3-4):**

```
Erreur 1 (Byte 3):
0x01 = Panne résistance
0x02 = Trop froid pour chauffage
0x10 = Panne moteur
0x20 = Filtre à changer
0x30 = Panne capteur QAI
...

Erreur 2 (Byte 4):
0x51 = Panne sonde chauffage
0x52 = Panne sonde VMI
...
```

**Commandes Envoyées:**

```python
# Changer vitesse
send_d1079(0x0421574F, [0x20, 50, 0, 0])  # Vitesse 50%

# Activer mode auto
send_d1079(0x0421574F, [0x02, 0, 0, 0])  # Mode Auto

# Arrêter
send_d1079(0x0421574F, [0x00, 0, 0, 0])  # Off
```

---

### 2. Capteur CO₂ (A5-09-04)

**Informations:**

- RORG: 0xA5 (4BS)
- FUNC: 0x09 (Environmental Sensor)
- TYPE: 0x04 (CO2 Sensor)
- Adresse: 0x81003227

**Structure Données:**

```
Byte 0-3: Valeur CO₂ (big-endian)

Formule de conversion:
  co2_ppm = (raw_value * 2500) / 0xFFFFFFFF

Plage: 0-2500 ppm
```

**Interprétation:**

- 0 ppm: Erreur/Pas d'appareil
- 400-600 ppm: Normal extérieur/bon
- 600-1000 ppm: Acceptable
- 1000-1500 ppm: Élevé, aération recommandée
- > 1500 ppm: Très élevé, action nécessaire

---

### 3. Capteur Température/Humidité (A5-04-01)

**Informations:**

- RORG: 0xA5 (4BS)
- FUNC: 0x04 (Temperature/Humidity Sensor)
- TYPE: 0x01 (Standard sensor)
- Adresse: 0x810054F5

**Structure Données:**

```
Byte 0-1: Température
  Valeur brute (0-1023)
  Plage: 0-40°C (ou -20 à +60°C selon variante)
  Conversion: temp_C = (raw / 1023) * 40

Byte 2-3: Humidité
  Valeur brute (0-1023)
  Plage: 0-100%
  Conversion: humidity_% = (raw / 1023) * 100
```

**Interprétation:**

- Température: 18-25°C optimal
- Humidité: 40-60% optimal

---

## Commandes VMI

### API Commandes

```python
# Classe: VentilairsecManager

# Changer vitesse
await manager.set_vmi_speed(speed: int)  # 0-100%

# Mode automatique
await manager.set_vmi_mode('auto')

# Mode manuel
await manager.set_vmi_mode('manual')

# Arrêter
await manager.set_vmi_mode('off')

# Mode bypass
await manager.set_vmi_mode('bypass')
```

### Format Paquet D1-07-9F

```python
# Exemple: Augmenter vitesse à 75%
packet = RadioPacket(
    rorg=0xD1,
    func=0x07,
    type_byte=0x9F,
    data=bytes([0x20, 75, 20, 0])  # [mode, speed%, temp, err]
)
```

---

## Intégration HA

### Topics MQTT

#### Publication (Addon → HA)

```
# État VMI
homeassistant/ventilairsec2ha/state/0421574F
{
  "name": "VMI Purevent",
  "address": "0421574F",
  "rorg": "0xD1",
  "last_update": "2024-12-06T10:30:45",
  "data": {
    "status": 2,
    "speed": 50,
    "temperature": 18,
    "errors": [0, 0]
  }
}

# État CO₂
homeassistant/ventilairsec2ha/state/81003227
{
  "name": "CO2 Sensor",
  "data": {
    "co2_ppm": 850
  }
}

# État Temp/Humidité
homeassistant/ventilairsec2ha/state/810054F5
{
  "name": "Temp/Humidity Sensor",
  "data": {
    "temperature": 21.5,
    "humidity": 55.0
  }
}
```

#### Subscription (HA → Addon)

```
# Changer vitesse
homeassistant/ventilairsec2ha/command/set_speed
Payload: 50 (0-100)

# Changer mode
homeassistant/ventilairsec2ha/command/set_mode
Payload: "auto" | "manual" | "off" | "bypass"
```

### Entités Home Assistant

Les entités suivantes sont créées automatiquement :

```yaml
# Capteur CO₂
sensor.co2_sensor:
  friendly_name: "CO₂ Pièce"
  unit_of_measurement: "ppm"
  device_class: "carbon_dioxide"

# Capteur Température
sensor.temp_humidity_sensor_temperature:
  friendly_name: "Température Pièce"
  unit_of_measurement: "°C"
  device_class: "temperature"

# Capteur Humidité
sensor.temp_humidity_sensor_humidity:
  friendly_name: "Humidité Pièce"
  unit_of_measurement: "%"
  device_class: "humidity"

# VMI Vitesse
number.vmi_purevent_speed:
  friendly_name: "Vitesse VMI"
  unit_of_measurement: "%"
  min: 0
  max: 100
```

---

## Debugging

### Activer les logs de debug

Configuration:

```json
{
  "log_level": "debug"
}
```

### Exemples de logs

```
2024-12-06 10:30:45 - INFO - 📡 Packet from VMI Purevent (0421574F)
2024-12-06 10:30:45 - DEBUG - 📦 Processing packet from 0421574F
2024-12-06 10:30:45 - INFO - 🌬️  VMI: Speed=50%, Temp=18°C, Errors=0
2024-12-06 10:30:50 - INFO - 💨 CO2 Sensor: 850 ppm
2024-12-06 10:30:50 - INFO - 🌡️  Temp/Humidity: 21.5°C, 55.0%
```

---

## Références

- [EnOcean Equipment Profiles (EEP)](https://www.enocean.com/en/enocean-modules/enocean-profiles/)
- [ESP3 Protocol](https://www.enocean.com/esp3protocol)
- [Home Assistant Add-ons Development](https://developers.home-assistant.io/docs/add-ons/)
- [MQTT Specification](https://mqtt.org/)
