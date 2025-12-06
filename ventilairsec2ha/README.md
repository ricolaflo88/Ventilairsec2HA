# 📡 Ventilairsec2HA - Addon Home Assistant

Addon Home Assistant OS pour contrôler une **VMI Purevent Ventilairsec** via le protocole **EnOcean**.

Cet addon reproduit la fonctionnalité du plugin Jeedom *Ventilairsec* en intégrant le protocole de communication *OpenEnOcean*, permettant à Home Assistant de communiquer directement avec votre VMI et ses capteurs associés.

## 🎯 Objectif Principal

Fournir une **intégration complète et autonome** permettant à Home Assistant de :

- 📡 **Communiquer en EnOcean** (réception + émission)
- 🌬️ **Contrôler la VMI Purevent** (vitesse, mode, arrêt, etc.)
- 📊 **Recevoir et afficher** tous les états et mesures
- 💾 **Enregistrer les données** localement
- 🏠 **S'intégrer nativement** dans Home Assistant

## 📦 Appareils Supportés

### 1️⃣ VMI Ventilairsec Purevent
- **RORG-FUNC-TYPE:** D1-07-9F (D1079-01-00)
- **Adresse:** `0x0421574F`
- **Commandes:** Vitesse, mode, arrêt, consultation d'état
- **Capteurs internes:** Température, erreurs, mode ventilation

### 2️⃣ Capteur CO₂ Externe
- **RORG-FUNC-TYPE:** A5-09-04
- **Adresse:** `0x81003227`
- **Mesure:** CO₂ en ppm (0-2500)

### 3️⃣ Capteur Température + Humidité
- **RORG-FUNC-TYPE:** A5-04-01
- **Adresse:** `0x810054F5`
- **Mesures:** Température (°C) et Humidité (%)

### 4️⃣ Assistant Ventilairsec (Télécommande)
- **RORG-FUNC-TYPE:** D1-07-9F (D1079-00-00)
- **Adresse:** `0x0422407D`

## 🚀 Fonctionnalités

### ✅ Implémentation
- [x] Pile EnOcean complète (réception/parsing/envoi)
- [x] Décodage des trames D1-07-9F (VMI Purevent)
- [x] Support des capteurs 4BS (A5-04-xx)
- [x] Gestion MQTT pour Home Assistant
- [x] API REST avec WebUI
- [x] Configuration flexible
- [x] Logging avancé

### 📋 En Développement
- [ ] Entités Home Assistant natives
- [ ] Dashboard Lovelace préconfiguré
- [ ] Tests complets hardware
- [ ] Documentation complète

## 📥 Installation

### Via dépôt GitHub (recommandé)

1. Aller dans **Paramètres > Modules complémentaires > Créer un dépôt**
2. Ajouter l'URL: `https://github.com/ricolaflo88/Ventilairsec2HA`
3. Chercher **Ventilairsec2HA** dans la boutique
4. Cliquer sur **Installer**

### Configuration

Après installation, configurer le port série et MQTT :

```json
{
  "serial_port": "/dev/ttyUSB0",
  "log_level": "info",
  "enable_mqtt": true,
  "mqtt_broker": "mosquitto",
  "mqtt_port": 1883
}
```

## 🔧 Configuration

### Port Série
- **Type:** USB avec adaptateur EnOcean (Husbands TCM310)
- **Vitesse:** 57600 baud (automatique)
- **Port par défaut:** `/dev/ttyUSB0`

### MQTT (optionnel)
- **Broker:** `mosquitto` (addon Home Assistant)
- **Port:** `1883`
- **Topics:** `homeassistant/ventilairsec2ha/#`

## 🌐 WebUI et API

### Accès WebUI
- **URL:** `http://<home-assistant>:8080`
- **Affiche:** État du système, appareils connectés, logs

### API REST

#### Status
```bash
GET /api/status
# Retourne: {connected, base_id, timestamp}
```

#### Liste des appareils
```bash
GET /api/devices
# Retourne: {address: {name, rorg, last_update, data}}
```

#### Envoyer une commande
```bash
POST /api/command
{
  "command": "set_speed",
  "speed": 50
}
```

## 📡 Topics MQTT

### Publication (de l'addon vers HA)
```
homeassistant/ventilairsec2ha/state/0421574F
→ {name: "VMI Purevent", data: {...}}

homeassistant/ventilairsec2ha/state/81003227
→ {name: "CO2 Sensor", data: {...}}
```

### Subscription (de HA vers l'addon)
```
homeassistant/ventilairsec2ha/command/set_speed
→ payload: 50 (vitesse 0-100%)
```

## 📊 Structures de Données

### État VMI (D1-07-9F)
```json
{
  "address": "0421574F",
  "name": "VMI Purevent",
  "rorg": "0xD1",
  "data": {
    "status": 0x01,
    "speed": 50,
    "temperature": 18,
    "errors": [0, 0]
  }
}
```

### CO₂ (A5-09-04)
```json
{
  "address": "81003227",
  "name": "CO2 Sensor",
  "rorg": "0xA5",
  "data": {
    "co2_ppm": 850
  }
}
```

### Température/Humidité (A5-04-01)
```json
{
  "address": "810054F5",
  "name": "Temp/Humidity Sensor",
  "rorg": "0xA5",
  "data": {
    "temperature": 21.5,
    "humidity": 55.0
  }
}
```

## 🔐 Sécurité

- ✅ Utilisateur non-root dans conteneur
- ✅ Isolation du processus Docker
- ✅ Pas d'exposition directe du port série
- ✅ Configuration sécurisée via Home Assistant

## 📝 Logs

Accédez aux logs via :
- **WebUI:** `http://<host>:8080/api/logs`
- **Conteneur:** `docker logs addon_ventilairsec2ha`
- **Level:** Configurable (debug|info|warning|error)

## 🐛 Troubleshooting

### Port série non trouvé
```bash
# Vérifier les ports disponibles
ls -la /dev/tty*

# Donner les permissions
chmod 666 /dev/ttyUSB0
```

### MQTT non connecté
- Vérifier que l'addon Mosquitto est installé
- Vérifier la configuration du broker MQTT
- Vérifier les logs de l'addon

### Pas de réception de trames
- Vérifier le port série
- Vérifier la distance et la ligne de vue
- Vérifier que les appareils EnOcean sont appairés

## 📚 Références

- [EnOcean Specification](https://www.enocean.com/)
- [Home Assistant Add-ons](https://developers.home-assistant.io/docs/add-ons)
- [Plugin Jeedom OpenEnOcean](https://github.com/Jeedom/plugin-openenocean)
- [Plugin Jeedom Ventilairsec](https://github.com/Jeedom/plugin-ventilairsec)

## 📄 Licence

MIT - Voir [LICENSE](LICENSE)

## 👥 Auteur

**ricolaflo88** - Créateur et mainteneur

## 🤝 Contributions

Les contributions sont bienvenues ! Veuillez :

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📧 Support

Pour les questions ou problèmes :
- Ouvrir une issue sur GitHub
- Consulter la [documentation Home Assistant](https://www.home-assistant.io/)
- Contacter le support EnOcean

---

**Fait avec ❤️ pour la domotique open-source**
