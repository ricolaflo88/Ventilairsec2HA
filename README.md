# 🌬️ Ventilairsec2HA - Addon Home Assistant OS

![License](https://img.shields.io/badge/License-MIT-green)
![Version](https://img.shields.io/badge/Version-0.1.0-blue)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2023.12+-blue)

Addon Home Assistant OS pour contrôler une **VMI Purevent Ventilairsec** via le protocole **EnOcean**.

Cet addon reproduit la fonctionnalité du plugin Jeedom *Ventilairsec* en intégrant le protocole de communication *EnOcean*, permettant à Home Assistant de communiquer directement avec votre VMI et ses capteurs associés.

## 🚀 Démarrage Rapide

### 1. Installation

```bash
# Ajouter le dépôt dans Home Assistant
Paramètres > Modules complémentaires > ⋮ > Gérer les dépôts
Ajouter: https://github.com/ricolaflo88/Ventilairsec2HA
```

### 2. Configuration Minimale

#### Option 1: GPIO UART (Raspberry Pi - Recommandé)
```json
{
  "connection_mode": "gpio",
  "serial_port": "/dev/ttyAMA0",
  "log_level": "info",
  "enable_mqtt": true,
  "mqtt_broker": "mosquitto"
}
```

#### Option 2: USB
```json
{
  "connection_mode": "usb",
  "serial_port": "/dev/ttyUSB0",
  "log_level": "info",
  "enable_mqtt": true,
  "mqtt_broker": "mosquitto"
}
```

#### Option 3: Auto-Détection (Flexible)
```json
{
  "connection_mode": "auto",
  "serial_port": "auto",
  "log_level": "info",
  "enable_mqtt": true,
  "mqtt_broker": "mosquitto"
}
```

### 3. Démarrer l'Addon

```
Paramètres > Modules complémentaires > Ventilairsec2HA > Démarrer
```

## 📋 Table des Matières

- [🎯 Objectif Principal](#-objectif-principal)
- [📦 Appareils Supportés](#-appareils-supportés)
- [✨ Fonctionnalités](#-fonctionnalités)
- [📥 Installation](#-installation)
- [⚙️ Configuration](#-configuration)
- [🌐 WebUI et API](#-webui-et-api)
- [🐛 Troubleshooting](#-troubleshooting)
- [📚 Documentation](#-documentation)
- [🤝 Contributions](#-contributions)

---

## 🎯 Objectif Principal

Fournir une **intégration complète et autonome** permettant à Home Assistant de :

- 📡 **Communiquer en EnOcean** (réception + émission)
- 🌬️ **Contrôler la VMI Purevent** (vitesse, mode, arrêt, etc.)
- 📊 **Recevoir et afficher** tous les états et mesures
- 💾 **Enregistrer les données** localement
- 🏠 **S'intégrer nativement** dans Home Assistant
---

## 📦 Appareils Supportés

### VMI Ventilairsec Purevent (D1-07-9F)
- **Adresse:** `0x0421574F`
- **Commandes:** Vitesse, mode, arrêt, consultation d'état
- **Capteurs internes:** Température, erreurs

### Capteur CO₂ (A5-09-04)
- **Adresse:** `0x81003227`
- **Mesure:** CO₂ en ppm (0-2500)

### Capteur Température + Humidité (A5-04-01)
- **Adresse:** `0x810054F5`
- **Mesures:** Température (°C) et Humidité (%)

### Assistant Ventilairsec / Télécommande (D1-07-9F)
- **Adresse:** `0x0422407D`

---

## ✨ Fonctionnalités

### ✅ Implémentation Actuelle
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
- [ ] Appairage semi-auto des nouveaux appareils

---

## 📥 Installation

### Via Dépôt GitHub (Recommandé)

1. **Paramètres > Modules complémentaires > ⋮ > Créer un dépôt**
2. Coller: `https://github.com/ricolaflo88/Ventilairsec2HA`
3. **Cliquer sur Créer**
4. Chercher **Ventilairsec2HA** dans la boutique
5. **Cliquer sur Installer**

### Installation Manuelle (Développement)

```bash
# SSH dans Home Assistant
ssh root@homeassistant.local

# Clone le repo dans /addons
cd /addons
git clone https://github.com/ricolaflo88/Ventilairsec2HA.git

# Rafraîchir les add-ons
# Paramètres > Modules complémentaires > ⋮ > Recharger les addons
```

---

## ⚙️ Configuration

### Paramètres Disponibles

| Paramètre | Type | Défaut | Description |
|-----------|------|--------|-------------|
| `connection_mode` | choice | `auto` | Mode connexion (auto\|gpio\|usb) |
| `serial_port` | string | `auto` | Port série (/dev/ttyAMA0, /dev/ttyUSB0, auto) |
| `log_level` | choice | `info` | Niveau de logging (debug\|info\|warning\|error) |
| `enable_mqtt` | boolean | `true` | Activer publication MQTT |
| `mqtt_broker` | string | `mosquitto` | Serveur MQTT |
| `mqtt_port` | integer | `1883` | Port MQTT |

### Exemple Configuration Complète

```json
{
  "connection_mode": "auto",
  "serial_port": "auto",
  "log_level": "info",
  "enable_mqtt": true,
  "mqtt_broker": "mosquitto",
  "mqtt_port": 1883
}
```

---

## 🌐 WebUI et API

### Accès WebUI
- **URL:** `http://<home-assistant>:8080`
- **Affiche:** État du système, appareils, logs

### API REST

```bash
# Status du système
GET /api/status

# Liste des appareils connectés
GET /api/devices

# Envoyer une commande
POST /api/command
# {"command": "set_speed", "speed": 50}

# Logs
GET /api/logs
```

---

## 📡 Topics MQTT

### Publication (Addon → HA)

```
homeassistant/ventilairsec2ha/state/0421574F
homeassistant/ventilairsec2ha/state/81003227
homeassistant/ventilairsec2ha/state/810054F5
```

### Subscription (HA → Addon)

```
homeassistant/ventilairsec2ha/command/set_speed
Payload: 50 (0-100%)
```

---

## 🐛 Troubleshooting

### Port série non détecté

```bash
ssh root@homeassistant.local
ls -la /dev/ttyUSB*
chmod 666 /dev/ttyUSB0
```

### Pas de réception de trames

```bash
# Vérifier les logs
docker logs addon_ventilairsec2ha

# Tester la clé EnOcean
screen /dev/ttyUSB0 57600
```

### MQTT non connecté

- Vérifier que l'addon Mosquitto est installé
- Vérifier la configuration du broker
- Consulter les logs: `docker logs addon_ventilairsec2ha`

---

## 📚 Documentation

- [📖 Installation Détaillée](ventilairsec2ha/INSTALL.md)
- [🔧 Documentation Technique](ventilairsec2ha/DOCS.md)
- [🔌 Guide GPIO vs USB](GPIO_USB_GUIDE.md)
- [📝 Changelog](ventilairsec2ha/CHANGELOG.md)
- [🎯 README de l'Addon](ventilairsec2ha/README.md)

---

## 🤝 Contributions

Les contributions sont bienvenues ! Veuillez :

1. **Fork** le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** vos changements (`git commit -m 'Add AmazingFeature'`)
4. **Push** vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une **Pull Request**

### Développement Local

```bash
# Clone & setup
git clone https://github.com/ricolaflo88/Ventilairsec2HA.git
cd Ventilairsec2HA

# Installer les dépendances
pip install -r ventilairsec2ha/rootfs/requirements.txt

# Lancer les tests
python -m pytest tests/

# Linter
flake8 ventilairsec2ha/rootfs/app/
pylint ventilairsec2ha/rootfs/app/
```

---

## 📄 Licence

MIT - Voir [LICENSE](LICENSE)

Crédits:
- Base addon: Home Assistant example addons
- Protocole EnOcean: spécifications officielles
- Logique Ventilairsec: adaptée du plugin Jeedom
- Communication OpenEnOcean: patterns du plugin Jeedom

---

## 👥 Auteur

**ricolaflo88** - Créateur et mainteneur

---

## 📞 Support

Pour les questions ou problèmes :
- 🐛 [Issues GitHub](https://github.com/ricolaflo88/Ventilairsec2HA/issues)
- 📚 [Documentation](ventilairsec2ha/DOCS.md)
- 🌐 [Home Assistant Community](https://community.home-assistant.io/)

---

## 🔗 Ressources

- [EnOcean Official](https://www.enocean.com/)
- [Home Assistant Docs](https://www.home-assistant.io/)
- [MQTT Specification](https://mqtt.org/)
- [Plugin Jeedom OpenEnOcean](https://github.com/Jeedom/plugin-openenocean)
- [Plugin Jeedom Ventilairsec](https://github.com/Jeedom/plugin-ventilairsec)

---

<div align="center">

**Fait avec ❤️ pour la domotique open-source**

⭐ Si ce projet vous plaît, n'hésitez pas à lui donner une star ! ⭐

</div>

