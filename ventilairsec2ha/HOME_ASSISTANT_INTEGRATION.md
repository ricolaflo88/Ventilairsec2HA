# 🏠 Intégration Home Assistant - Ventilairsec2HA

## Prérequis

Pour une intégration réussie, vous devez avoir :

1. **Home Assistant OS** installé sur une Raspberry Pi (ou compatible) ou sur votre serveur
2. **MQTT Broker** (obligatoire) - soit mosquitto, soit un broker MQTT externe
3. **EnOcean USB Dongle** ou **module GPIO UART** correctement configuré

## Étape 1 : Configuration du Broker MQTT

### Option A : Broker MQTT Local (Mosquitto)

1. Allez dans Home Assistant → **Paramètres → Modules complémentaires** → **Mosquitto broker**
2. Installez le module si non présent
3. Notez le nom d'hôte : généralement `localhost` ou `127.0.0.1`
4. Port par défaut : `1883`

### Option B : Broker MQTT Externe

Si vous utilisez un broker MQTT externe (par ex. test.mosquitto.org) :

1. Notez l'adresse IP/hostname
2. Notez le port (généralement 1883 ou 8883 avec TLS)
3. Notez les identifiants si nécessaire

## Étape 2 : Installation de l'Addon Ventilairsec2HA

### Depuis le Repository

1. Ajoutez ce repository à Home Assistant :
   - **Paramètres → Modules complémentaires → Créer un module** (coin en bas à droite)
   - **Autre** (onglet en bas)
   - **Ajouter un repository** : `https://github.com/ricolaflo88/Ventilairsec2HA`

2. Retournez à **Modules complémentaires → Parcourir les modules**
3. Cherchez **Ventilairsec2HA** 
4. Cliquez sur le module et **Installer**

### Depuis un Repository Local

Pour développement local :

```bash
# Dans votre machine de dev
git clone https://github.com/ricolaflo88/Ventilairsec2HA.git
cd Ventilairsec2HA

# Copier vers Home Assistant add-ons directory
cp -r ventilairsec2ha /path/to/home/assistant/addons/
```

## Étape 3 : Configuration Initiale

### Configuration Minimale

1. Ouvrez le module Ventilairsec2HA dans Home Assistant
2. Cliquez sur **Configuration**
3. Remplissez les champs obligatoires :

**Pour MQTT Local (recommandé) :**
```json
{
  "mqtt_host": "localhost",
  "mqtt_port": 1883,
  "mqtt_username": "",
  "mqtt_password": "",
  "mqtt_retain": true,
  "log_level": "INFO",
  "connection_mode": "auto",
  "serial_port": "auto"
}
```

**Pour MQTT Externe :**
```json
{
  "mqtt_host": "example.com",
  "mqtt_port": 1883,
  "mqtt_username": "user",
  "mqtt_password": "pass",
  "mqtt_retain": true,
  "log_level": "INFO",
  "connection_mode": "auto",
  "serial_port": "auto"
}
```

### Configuration Avancée

Pour un contrôle plus fin sur la connexion :

**Pour GPIO (Raspberry Pi) :**
```json
{
  "mqtt_host": "localhost",
  "mqtt_port": 1883,
  "connection_mode": "gpio",
  "serial_port": "/dev/ttyAMA0",
  "log_level": "DEBUG"
}
```

**Pour USB Dongle :**
```json
{
  "mqtt_host": "localhost",
  "mqtt_port": 1883,
  "connection_mode": "usb",
  "serial_port": "/dev/ttyUSB0",
  "log_level": "DEBUG"
}
```

## Étape 4 : Démarrage du Module

1. **Enregistrer** la configuration
2. Cliquez sur **Démarrer**
3. Vérifiez les logs pour confirmer :
   ```
   ✓ Connection type: gpio (or usb)
   ✓ Connected to MQTT broker
   ✓ Listening for EnOcean packets...
   ```

## Étape 5 : Intégration dans Home Assistant

### Vérifier la Réception des Données

1. **Paramètres → Appareils et Services → MQTT**
2. Cherchez les topics publiés :
   - `homeassistant/ventilairsec2ha/state/0x0421574F` (VMI)
   - `homeassistant/ventilairsec2ha/state/0x81003227` (CO2)
   - `homeassistant/ventilairsec2ha/state/0x810054F5` (Temp/Humidity)

### Créer des Automations

**Exemple 1 : Notification si CO2 > 1000 ppm**

```yaml
automation:
  - alias: "Alerte CO2 Élevé"
    trigger:
      platform: mqtt
      topic: homeassistant/ventilairsec2ha/state/0x81003227
    condition:
      template: "{{ trigger.payload_json.co2 > 1000 }}"
    action:
      - service: notify.pushbullet
        data:
          message: "⚠️ CO2 élevé: {{ trigger.payload_json.co2 }} ppm"
```

**Exemple 2 : Augmenter Vitesse VMI si Température > 24°C**

```yaml
automation:
  - alias: "Augmente VMI si Température Haute"
    trigger:
      platform: mqtt
      topic: homeassistant/ventilairsec2ha/state/0x810054F5
    condition:
      template: "{{ trigger.payload_json.temperature > 24 }}"
    action:
      - service: mqtt.publish
        data:
          topic: homeassistant/ventilairsec2ha/command
          payload: '{"address": "0x0421574F", "speed": 3}'
```

## Troubleshooting

### Le Module ne Démarre pas

1. Vérifiez les logs : **Affichage des logs (coin en haut à droite)**
2. Vérifiez la connexion MQTT
3. Vérifiez la connexion au port série (GPIO/USB)

### Pas de Données Reçues

Consultez le [Guide GPIO vs USB](GPIO_USB_GUIDE.md) pour :
- Vérifier les permissions GPIO
- Tester la détection automatique
- Faire un diagnostic complet

### Erreur de Permission

```
✗ Permission denied: /dev/ttyAMA0
```

Exécutez le diagnostic :
```bash
docker exec addon_ventilairsec2ha python3 /app/diagnostics.py
```

## Interfaces Web Disponibles

### Dashboard WebUI

Accédez au dashboard web en visitant :
- `http://homeassistant.local:8080`
- Ou via l'URL fournie dans la description du module

### Endpoints API REST

```bash
# État du système
curl http://homeassistant.local:8080/api/status

# Liste des appareils
curl http://homeassistant.local:8080/api/devices

# Commandes
curl -X POST http://homeassistant.local:8080/api/command \
  -H "Content-Type: application/json" \
  -d '{"address": "0x0421574F", "speed": 2}'
```

## Support et Ressources

- **Problèmes** : https://github.com/ricolaflo88/Ventilairsec2HA/issues
- **Documentation Technique** : `ventilairsec2ha/DOCS.md`
- **Guide GPIO/USB** : `GPIO_USB_GUIDE.md`
- **Logs du Module** : Affichage des logs Home Assistant

---

**Version** : 0.1.0  
**Mise à jour** : $(date)  
**Auteur** : Ventilairsec2HA Project
