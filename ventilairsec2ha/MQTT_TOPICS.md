## 📡 MQTT Topics et Structure - Ventilairsec2HA

### Configuration MQTT Discovery

Ventilairsec2HA utilise **MQTT Discovery** pour créer automatiquement les entités dans Home Assistant. Aucune configuration manuelle n'est nécessaire.

---

## 🏠 Entités Créées Automatiquement

### 1️⃣ VMI Purevent Ventilairsec (Device ID: 0421574F)

#### Climate Entity - Contrôle Ventilation

**Discovery Topic:**
```
homeassistant/climate/0421574F/vmi_climate/config
```

**State Topic (RO):**
```
ventilairsec2ha/0421574F/vmi_climate/state
```

**Command Topic (RW):**
```
ventilairsec2ha/0421574F/vmi_climate/set
```

**Modes Disponibles:**
- `off` (0) - Ventilateur arrêté
- `low` (1) - Basse vitesse (~40%)
- `medium` (2) - Vitesse moyenne (~60%)
- `high` (3) - Haute vitesse (~80%)
- `auto` (4) - Turbo/Boost (100%)

**Exemple de Commande:**
```bash
mosquitto_pub -h localhost -t "ventilairsec2ha/0421574F/vmi_climate/set" -m "high"
```

**State Payload:**
```json
{
  "state": 2,
  "last_update": "2024-01-15T14:30:45.123456"
}
```

---

#### Sensor: VMI Temperature

**Discovery Topic:**
```
homeassistant/sensor/0421574F/vmi_temperature/config
```

**State Topic:**
```
ventilairsec2ha/0421574F/vmi_temperature/state
```

**Unit:** °C
**Device Class:** temperature

**State Example:**
```json
{
  "state": 22.5
}
```

---

#### Sensor: VMI Status

**Discovery Topic:**
```
homeassistant/sensor/0421574F/vmi_status/config
```

**State Topic:**
```
ventilairsec2ha/0421574F/vmi_status/state
```

**Possible Values:**
- `normal` - Fonctionnement normal
- `maintenance` - Mode maintenance
- `fault` - Erreur détectée

---

#### Sensor: VMI Error Code

**Discovery Topic:**
```
homeassistant/sensor/0421574F/vmi_error/config
```

**State Topic:**
```
ventilairsec2ha/0421574F/vmi_error/state
```

**State Example:**
```json
{
  "state": 0
}
```

---

### 2️⃣ Capteur CO₂ (Device ID: 81003227)

#### Sensor: CO2 Level

**Discovery Topic:**
```
homeassistant/sensor/81003227/co2_level/config
```

**State Topic:**
```
ventilairsec2ha/81003227/co2_level/state
```

**Unit:** ppm (parts per million)
**Device Class:** carbon_dioxide
**Range:** 0-2500 ppm

**State Example:**
```json
{
  "state": 450
}
```

**Niveaux Recommandés:**
- < 400 ppm : Excellent
- 400-800 ppm : Bon
- 800-1200 ppm : Acceptable
- > 1200 ppm : Mauvais

---

### 3️⃣ Capteur Température + Humidité (Device ID: 810054F5)

#### Sensor: Temperature

**Discovery Topic:**
```
homeassistant/sensor/810054F5/temperature/config
```

**State Topic:**
```
ventilairsec2ha/810054F5/temperature/state
```

**Unit:** °C
**Device Class:** temperature
**Range:** -20 à +60°C

**State Example:**
```json
{
  "state": 21.2
}
```

---

#### Sensor: Humidity

**Discovery Topic:**
```
homeassistant/sensor/810054F5/humidity/config
```

**State Topic:**
```
ventilairsec2ha/810054F5/humidity/state
```

**Unit:** %
**Device Class:** humidity
**Range:** 0-100%

**State Example:**
```json
{
  "state": 55
}
```

---

## 🔄 Format des Messages MQTT

### Discovery Message (Retained)

```json
{
  "name": "VMI Ventilation Control",
  "state_topic": "ventilairsec2ha/0421574F/vmi_climate/state",
  "command_topic": "ventilairsec2ha/0421574F/vmi_climate/set",
  "modes": ["off", "low", "medium", "high", "auto"],
  "temperature_unit": "C",
  "min_temp": 0,
  "max_temp": 4,
  "precision": 1,
  "unique_id": "ventilairsec2ha_0421574F_vmi_climate",
  "device": {
    "identifiers": ["ventilairsec2ha_0421574F"],
    "name": "Ventilairsec2HA 0421574F",
    "manufacturer": "Ventilairsec2HA",
    "model": "Purevent Ventilairsec"
  }
}
```

### State Message (Retained)

```json
{
  "state": 2,
  "last_update": "2024-01-15T14:30:45.123456"
}
```

---

## 📊 Fréquence de Publication

- **Climate State:** Tous les 10 secondes
- **Sensors:** Tous les 10 secondes
- **Tous les messages:** Retained = true (persistant)

---

## 🎯 Utilisation dans Home Assistant

### Créer une Automatisation

```yaml
automation:
  - alias: "Auto-boost VMI si CO2 élevé"
    trigger:
      platform: numeric_state
      entity_id: sensor.co2_level
      above: 1000
    action:
      service: mqtt.publish
      data:
        topic: "ventilairsec2ha/0421574F/vmi_climate/set"
        payload: "auto"
```

### Afficher sur un Dashboard

```yaml
cards:
  - type: climate
    entity: climate.vmi_ventilation_control
    name: "Ventilation"
  
  - type: gauge
    entity: sensor.co2_level
    min: 400
    max: 2500
    
  - type: entities
    entities:
      - entity: sensor.temperature
      - entity: sensor.humidity
      - entity: sensor.vmi_temperature
```

---

## 🔍 Debugging MQTT

### Écouter tous les messages Ventilairsec

```bash
mosquitto_sub -h localhost -t "ventilairsec2ha/#" -v
```

### Écouter les découvertes Home Assistant

```bash
mosquitto_sub -h localhost -t "homeassistant/+/0421574F/+/config" -v
```

### Tester une commande

```bash
mosquitto_pub -h localhost -t "ventilairsec2ha/0421574F/vmi_climate/set" -m "high"
```

---

## ⚙️ Configuration MQTT dans Home Assistant

Aucune configuration supplémentaire n'est nécessaire si vous avez l'addon Mosquitto installé, car Ventilairsec2HA utilise automatiquement la découverte MQTT (MQTT Discovery).

**Configuration optionnelle avancée (si broker externe):**

```yaml
mqtt:
  broker: example.com
  port: 1883
  username: user
  password: pass
```

---

## 🛠️ Troubleshooting

### Les entités n'apparaissent pas dans Home Assistant

1. Vérifier que le broker MQTT est connecté
2. Vérifier que MQTT Discovery est activé dans HA
3. Consulter les logs: `mosquitto_sub -h localhost -t "#" -v`

### Les commandes ne répondent pas

1. Vérifier le topic de command exact
2. Vérifier que la VMI est bien connectée
3. Consulter les logs du addon

### Loss de connexion MQTT

1. Vérifier la configuration du broker
2. Vérifier les credentials
3. Vérifier les logs pour l'erreur exacte
