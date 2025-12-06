# 🤖 Automatisations Home Assistant pour Ventilairsec2HA

Ce document fournit des automatisations clé-en-main à copier dans votre configuration Home Assistant.

## Prérequis

- Addon Ventilairsec2HA installé et fonctionnel
- MQTT configuré et connecté
- Automations activées dans Home Assistant

## Configuration YAML

Ajoutez ces blocs à votre `configuration.yaml` (ou utilisez l'interface UI) :

---

## 1️⃣ Monitoring de la Qualité de l'Air

### Alerte CO2 Élevé

```yaml
automation:
  - id: 'alert_high_co2'
    alias: "🚨 Alerte CO2 Élevé"
    description: "Notification quand CO2 > 800 ppm"
    trigger:
      platform: mqtt
      topic: "homeassistant/ventilairsec2ha/state/0x81003227"
    condition:
      - template: "{{ trigger.payload_json.co2 | float(0) > 800 }}"
    action:
      - service: persistent_notification.create
        data:
          title: "⚠️ CO2 Élevé"
          message: "CO2 = {{ trigger.payload_json.co2 }} ppm (> 800 seuil)"
          notification_id: "high_co2_alert"
```

### Historique CO2

```yaml
# Dans configuration.yaml, ajouter :
mqtt:
  sensor:
    - name: "CO2 Purevent"
      unique_id: "mqtt_co2_purevent"
      unit_of_measurement: "ppm"
      device_class: "carbon_dioxide"
      state_topic: "homeassistant/ventilairsec2ha/state/0x81003227"
      value_template: "{{ value_json.co2 | float(0) }}"
      json_attributes_topic: "homeassistant/ventilairsec2ha/state/0x81003227"
```

---

## 2️⃣ Contrôle VMI (Ventilateur)

### Augmenter Vitesse si Température Élevée

```yaml
automation:
  - id: 'increase_vmi_high_temp'
    alias: "🌡️ Augmente Ventilation si Chaud"
    description: "Passe VMI à vitesse 3 si T > 25°C"
    trigger:
      platform: mqtt
      topic: "homeassistant/ventilairsec2ha/state/0x810054F5"
    condition:
      - template: "{{ trigger.payload_json.temperature | float(0) > 25 }}"
      - template: "{{ now().hour >= 6 and now().hour < 22 }}"
    action:
      - service: mqtt.publish
        data:
          topic: "homeassistant/ventilairsec2ha/command"
          payload: '{"address": "0x0421574F", "speed": 3, "command": "speed_control"}'
      - service: persistent_notification.create
        data:
          title: "🌡️ VMI Augmentée"
          message: "Température = {{ trigger.payload_json.temperature }}°C, VMI vitesse 3"
```

### Réduire Vitesse la Nuit

```yaml
automation:
  - id: 'reduce_vmi_night'
    alias: "🌙 Réduit VMI la Nuit"
    description: "Passe VMI en vitesse 1 après 22h"
    trigger:
      platform: time
      at: "22:00:00"
    action:
      - service: mqtt.publish
        data:
          topic: "homeassistant/ventilairsec2ha/command"
          payload: '{"address": "0x0421574F", "speed": 1, "command": "speed_control"}'
      - service: persistent_notification.create
        data:
          title: "🌙 Mode Nuit VMI"
          message: "VMI réduite à vitesse 1"
```

### Ventilation Boost (Courte Durée)

```yaml
automation:
  - id: 'vmi_boost_30min'
    alias: "⚡ Boost Ventilation 30 min"
    description: "Passe VMI vitesse max pour 30 minutes"
    trigger:
      platform: mqtt
      topic: "homeassistant/ventilairsec2ha/state/0x81003227"
    condition:
      - template: "{{ trigger.payload_json.co2 | float(0) > 1200 }}"
    action:
      - service: mqtt.publish
        data:
          topic: "homeassistant/ventilairsec2ha/command"
          payload: '{"address": "0x0421574F", "speed": 4, "command": "speed_control"}'
      - delay:
          minutes: 30
      - service: mqtt.publish
        data:
          topic: "homeassistant/ventilairsec2ha/command"
          payload: '{"address": "0x0421574F", "speed": 2, "command": "speed_control"}'
```

---

## 3️⃣ Gestion Humidité

### Alerte Humidité Trop Basse (< 30%)

```yaml
automation:
  - id: 'alert_low_humidity'
    alias: "💧 Alerte Humidité Basse"
    description: "Notification si humidité < 30%"
    trigger:
      platform: mqtt
      topic: "homeassistant/ventilairsec2ha/state/0x810054F5"
    condition:
      - template: "{{ trigger.payload_json.humidity | float(100) < 30 }}"
    action:
      - service: persistent_notification.create
        data:
          title: "💧 Humidité Basse"
          message: "Humidité = {{ trigger.payload_json.humidity }}% (< 30% seuil)"
          notification_id: "low_humidity_alert"
```

### Alerte Humidité Trop Haute (> 70%)

```yaml
automation:
  - id: 'alert_high_humidity'
    alias: "💦 Alerte Humidité Élevée"
    description: "Notification si humidité > 70%"
    trigger:
      platform: mqtt
      topic: "homeassistant/ventilairsec2ha/state/0x810054F5"
    condition:
      - template: "{{ trigger.payload_json.humidity | float(0) > 70 }}"
    action:
      - service: mqtt.publish
        data:
          topic: "homeassistant/ventilairsec2ha/command"
          payload: '{"address": "0x0421574F", "speed": 3, "command": "speed_control"}'
      - service: persistent_notification.create
        data:
          title: "💦 Humidité Élevée"
          message: "Humidité = {{ trigger.payload_json.humidity }}% (> 70% seuil). Ventilation augmentée."
```

---

## 4️⃣ Monitoring Santé du Système

### Alerte Erreur VMI

```yaml
automation:
  - id: 'alert_vmi_error'
    alias: "⚠️ Erreur VMI Détectée"
    description: "Notification si erreur sur VMI"
    trigger:
      platform: mqtt
      topic: "homeassistant/ventilairsec2ha/state/0x0421574F"
    condition:
      - template: "{{ trigger.payload_json.error_code | int(-1) != -1 }}"
    action:
      - service: persistent_notification.create
        data:
          title: "⚠️ Erreur VMI"
          message: "Code erreur = {{ trigger.payload_json.error_code }}. Consultez les logs."
          notification_id: "vmi_error_alert"
```

### Perte de Connexion Module EnOcean

```yaml
automation:
  - id: 'alert_enocean_lost'
    alias: "📡 Perte Connexion EnOcean"
    description: "Notification si aucun packet reçu depuis 5 min"
    trigger:
      platform: template
      value_template: "{{ (now() - states.automation.check_enocean_connection.attributes.last_triggered | as_datetime).total_seconds() > 300 }}"
    action:
      - service: persistent_notification.create
        data:
          title: "📡 Connexion Perdue"
          message: "Aucun packet EnOcean reçu depuis 5 minutes."
          notification_id: "enocean_lost_alert"
```

---

## 5️⃣ Dashboard / Frontend

### Créer un Panel Ventilation (YAML)

Ajoutez à `ui-lovelace.yaml` ou via l'UI :

```yaml
views:
  - title: "🌬️ Ventilation"
    icon: mdi:fan
    cards:
      - type: grid
        cards:
          # VMI Speed Indicator
          - type: entities
            title: "🌬️ Vitesse VMI"
            entities:
              - entity: mqtt.ventilairsec2ha_state_0x0421574f
                name: "Vitesse Actuelle"
          
          # CO2 Gauge
          - type: gauge
            title: "CO2"
            unit_of_measurement: "ppm"
            min: 0
            max: 2000
            severity:
              green: 0
              yellow: 800
              red: 1200
            entity: mqtt.co2_purevent
          
          # Temperature/Humidity
          - type: entities
            title: "🌡️ Climat Intérieur"
            entities:
              - entity: mqtt.temperature_purevent
                name: "Température"
              - entity: mqtt.humidity_purevent
                name: "Humidité"
          
          # Control Buttons
          - type: button
            name: "💨 Boost 30min"
            tap_action:
              action: perform-action
              action: mqtt.publish
              data:
                topic: homeassistant/ventilairsec2ha/command
                payload: '{"address": "0x0421574F", "speed": 4}'
          
          - type: button
            name: "🌙 Mode Nuit"
            tap_action:
              action: perform-action
              action: mqtt.publish
              data:
                topic: homeassistant/ventilairsec2ha/command
                payload: '{"address": "0x0421574F", "speed": 1}'
```

---

## 6️⃣ Scripts Utiles

### Script : Diagnostic Rapide

```yaml
script:
  diagnose_ventilation:
    alias: "🔍 Diagnostic Ventilation"
    description: "Vérifie l'état de tous les capteurs"
    sequence:
      - service: persistent_notification.create
        data:
          title: "📋 Diagnostic Ventilation"
          message: |
            **VMI:** {{ state_attr('mqtt.ventilairsec2ha_state_0x0421574f', 'status') }}
            **CO2:** {{ states('mqtt.co2_purevent') }} ppm
            **Température:** {{ states('mqtt.temperature_purevent') }}°C
            **Humidité:** {{ states('mqtt.humidity_purevent') }}%
            **Dernière mise à jour:** {{ now() }}
```

### Script : Redémarrage Module

```yaml
script:
  restart_enocean_addon:
    alias: "🔄 Redémarrer Module EnOcean"
    description: "Redémarre l'addon Ventilairsec2HA"
    sequence:
      - service: hassio.addon_restart
        data:
          addon: local_ventilairsec2ha
      - service: persistent_notification.create
        data:
          title: "🔄 Redémarrage"
          message: "Module EnOcean redémarré. Reconnexion en cours..."
```

---

## 7️⃣ Intégration avec Autres Services

### Envoyer Alert via Telegram

```yaml
automation:
  - id: 'alert_co2_telegram'
    alias: "📱 CO2 via Telegram"
    trigger:
      platform: mqtt
      topic: "homeassistant/ventilairsec2ha/state/0x81003227"
    condition:
      - template: "{{ trigger.payload_json.co2 | float(0) > 1000 }}"
    action:
      - service: notify.telegram
        data:
          message: "⚠️ CO2 élevé: {{ trigger.payload_json.co2 }} ppm"
          title: "Alerte Ventilation"
```

### Synchroniser avec Google Calendar

```yaml
automation:
  - id: 'boost_vmi_work_hours'
    alias: "💼 Boost VMI Heures Bureau"
    description: "Augmente ventilation pendant heures de bureau"
    trigger:
      platform: calendar
      event: start
      entity_id: calendar.work_hours
    action:
      - service: mqtt.publish
        data:
          topic: "homeassistant/ventilairsec2ha/command"
          payload: '{"address": "0x0421574F", "speed": 3}'
```

---

## 📞 Support

- **Issues** : https://github.com/ricolaflo88/Ventilairsec2HA/issues
- **Discussions** : https://github.com/ricolaflo88/Ventilairsec2HA/discussions
- **Documentation** : Voir `DOCS.md`

---

**Version** : 0.1.0  
**Dernière mise à jour** : 2024  
**Auteur** : Ventilairsec2HA Project
