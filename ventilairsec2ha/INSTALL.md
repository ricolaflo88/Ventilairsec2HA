# 🚀 Guide d'Installation et Déploiement

## 📋 Prérequis

### Matériel
- **Clé USB EnOcean** (TCM310 ou compatible)
  - Fréquence: 868.3 MHz
  - Protocole: ESP3
  - Vitesse: 57600 baud
  
- **Home Assistant OS** version 2023.12+
  - Accès SSH activé
  - Addon Mosquitto installé (optionnel, pour MQTT)

### Logiciels
- Python 3.9+
- pip3
- Docker (fourni avec HA OS)

---

## 🔌 Préparation du Matériel

### 1. Identifier le Port Série

```bash
# Lister les ports USB disponibles
ls -la /dev/ttyUSB*
ls -la /dev/ttyACM*

# Vérifier les permissions
chmod 666 /dev/ttyUSB0
```

### 2. Vérifier la Clé EnOcean

```bash
# Test avec minicom ou screen
screen /dev/ttyUSB0 57600

# Ou envoyer une requête de version (optionnel)
echo -e '\xAA\x00\x05\x05\x70\x01\x80' > /dev/ttyUSB0
```

---

## 💾 Installation via Dépôt GitHub

### Option 1: Installation Recommandée (Store HA)

1. Aller dans **Paramètres > Modules complémentaires > ⋮ > Gérer les dépôts**
2. Cliquer sur **Créer un dépôt**
3. Coller: `https://github.com/ricolaflo88/Ventilairsec2HA`
4. Cliquer sur **Créer**
5. Chercher **Ventilairsec2HA** dans la boutique
6. Cliquer sur **Installer**
7. Configurer et démarrer

### Option 2: Installation Manuelle (Développement)

```bash
# SSH into Home Assistant
ssh root@homeassistant.local

# Clone the repository
cd /addons
git clone https://github.com/ricolaflo88/Ventilairsec2HA.git

# Refresh add-ons
# Go to Settings > Add-ons > ⋮ > Reload Add-on Store

# Install from local repository
# Look for Ventilairsec2HA in the local store
```

---

## ⚙️ Configuration Initiale

### 1. Configuration du Port Série

```json
{
  "serial_port": "/dev/ttyUSB0",
  "log_level": "info"
}
```

### 2. Configuration MQTT (optionnel)

```json
{
  "enable_mqtt": true,
  "mqtt_broker": "mosquitto",
  "mqtt_port": 1883,
  "mqtt_username": "",
  "mqtt_password": ""
}
```

### 3. Démarrer l'Addon

- **Paramètres > Modules complémentaires > Ventilairsec2HA**
- Cliquer sur **Démarrer**
- Consulter les **Journaux** pour vérifier

---

## 🔧 Configuration Avancée

### Automations Home Assistant

```yaml
# Augmenter automatiquement la vitesse si CO₂ élevé
automation:
  - alias: "Augmenter VMI si CO₂ > 1200 ppm"
    trigger:
      platform: numeric_state
      entity_id: sensor.co2_sensor
      above: 1200
    action:
      service: number.set_value
      target:
        entity_id: number.vmi_purevent_speed
      data:
        value: 75

  - alias: "Diminuer VMI la nuit"
    trigger:
      platform: time
      at: "22:00:00"
    action:
      service: number.set_value
      target:
        entity_id: number.vmi_purevent_speed
      data:
        value: 25
```

### Scripts Personnalisés

```yaml
script:
  vmi_boost:
    description: "Mode boost VMI (5 min à 100%)"
    sequence:
      - service: number.set_value
        target:
          entity_id: number.vmi_purevent_speed
        data:
          value: 100
      - delay: "00:05:00"
      - service: number.set_value
        target:
          entity_id: number.vmi_purevent_speed
        data:
          value: 50
```

### Template Sensors

```yaml
template:
  - sensor:
      - name: "Qualité Air VMI"
        icon: mdi:air-purifier
        state: >
          {% if states('sensor.co2_sensor')|float(0) < 600 %}
            Excellent
          {% elif states('sensor.co2_sensor')|float(0) < 1000 %}
            Bon
          {% elif states('sensor.co2_sensor')|float(0) < 1500 %}
            Acceptable
          {% else %}
            Élevé
          {% endif %}
```

---

## 📊 Dashboard Lovelace

```yaml
views:
  - title: "Ventilation"
    path: "ventilation"
    cards:
      - type: vertical-stack
        cards:
          - type: markdown
            content: |
              # 🌬️ Contrôle VMI Purevent
              État du système de ventilation mécanique
          
          - type: entities
            entities:
              - entity: number.vmi_purevent_speed
                name: "Vitesse VMI"
              - entity: sensor.vmi_temperature
                name: "Température VMI"
              - entity: sensor.vmi_errors
                name: "Erreurs VMI"
          
          - type: gauge
            entity: sensor.co2_sensor
            min: 0
            max: 2000
            segments:
              - from: 0
                color: green
                to: 600
              - from: 600
                color: yellow
                to: 1000
              - from: 1000
                color: orange
                to: 1500
              - from: 1500
                color: red
                to: 2000
          
          - type: history-graph
            entities:
              - entity: sensor.co2_sensor
              - entity: sensor.temp_humidity_sensor_temperature
              - entity: sensor.temp_humidity_sensor_humidity
            hours_to_show: 24
```

---

## 🔍 Troubleshooting

### Port série non détecté

```bash
# Vérifier les permissions
ls -la /dev/ttyUSB0

# Ajouter les permissions
sudo chmod 666 /dev/ttyUSB0

# Redémarrer l'addon
```

### Pas de réception de trames

```bash
# Vérifier les logs
docker logs addon_ventilairsec2ha

# Vérifier la connexion série
minicom -b 57600 -D /dev/ttyUSB0

# Tester la clé EnOcean avec un outil Python
python3 -c "import serial; s = serial.Serial('/dev/ttyUSB0', 57600); print(s.readline())"
```

### MQTT non connecté

```bash
# Vérifier Mosquitto addon
docker ps | grep mosquitto

# Tester la connexion MQTT
mosquitto_sub -h mosquitto -t "homeassistant/ventilairsec2ha/#" -v

# Vérifier les logs de l'addon
cat /data/ventilairsec2ha/logs.txt
```

### Entités non créées dans HA

1. Vérifier les logs du websocket HA
2. Redémarrer Home Assistant
3. Vérifier que l'addon est vraiment connecté
4. Consulter les topics MQTT: `mosquitto_sub -h mosquitto -t "#" -v`

---

## 🐛 Debugging

### Activer le mode debug

Configuration:
```json
{
  "log_level": "debug"
}
```

Consulter les logs:
```bash
# Via Docker
docker logs -f addon_ventilairsec2ha

# Via SSH puis tail
ssh root@homeassistant.local
tail -f /data/ventilairsec2ha/addon_log.txt
```

### Captures de paquets

```bash
# Sauvegarder les paquets reçus
docker logs addon_ventilairsec2ha | grep "📦" > packets.log

# Analyser les données
cat packets.log | grep "0x0421574F"  # VMI
cat packets.log | grep "0x81003227"  # CO₂
```

---

## 🚀 Mise à Jour

### Mise à jour de l'Addon

1. **Paramètres > Modules complémentaires > Ventilairsec2HA**
2. Si une mise à jour est disponible, cliquer sur **Mise à jour**
3. Attendre et redémarrer si nécessaire

### Mise à Jour Manuelle (Développement)

```bash
ssh root@homeassistant.local
cd /addons/Ventilairsec2HA
git pull
```

---

## 📦 Sauvegarde et Restauration

### Sauvegarder la Configuration

```bash
# SSH
ssh root@homeassistant.local

# Copier la configuration
cp -r /data/ventilairsec2ha ~/ventilairsec2ha_backup/

# Ou via SCP
scp -r root@homeassistant.local:/data/ventilairsec2ha ~/backup/
```

### Restaurer la Configuration

```bash
# Via SCP
scp -r ~/backup/ventilairsec2ha/* root@homeassistant.local:/data/ventilairsec2ha/

# Redémarrer l'addon
docker restart addon_ventilairsec2ha
```

---

## 🔐 Sécurité

### Bonnes Pratiques

- ✅ Utiliser des credentials MQTT forts
- ✅ Restreindre l'accès SSH
- ✅ Mettre à jour Home Assistant régulièrement
- ✅ Consulter les logs pour des anomalies
- ✅ Faire des sauvegardes régulières

### Exposer l'API de Manière Sécurisée

```yaml
# Via reverse proxy (Nginx, Let's Encrypt)
# Ne PAS exposer directement le port 8080 sur Internet

# Utiliser un VPN (WireGuard, OpenVPN)
# Ou accès local uniquement
```

---

## 📞 Support et Issues

### Signaler un Bug

1. Aller sur [GitHub Issues](https://github.com/ricolaflo88/Ventilairsec2HA/issues)
2. Cliquer sur **New Issue**
3. Décrire le problème avec:
   - Version de l'addon
   - Version de HA
   - Logs complets
   - Étapes pour reproduire

### Questions Fréquentes

**Q: L'addon consomme-t-il beaucoup de ressources?**
R: Non, typiquement <5% CPU et <50MB RAM

**Q: Peut-on utiliser plusieurs clés EnOcean?**
R: Actuellement non, mais prévu dans une version future

**Q: La communication est-elle chiffrée?**
R: EnOcean supporte le chiffrement (A-128 bits), implémentation future

---

## 🎓 Ressources Additionnelles

- [Documentation EnOcean](https://www.enocean.com/)
- [Home Assistant Documentation](https://www.home-assistant.io/docs/)
- [MQTT Essentials](https://www.hivemq.com/mqtt-essentials/)
- [Docker pour débutants](https://docs.docker.com/get-started/)

---

**Fait avec ❤️ pour la domotique open-source**
