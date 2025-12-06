# 📝 Changelog - Ventilairsec2HA

## [0.1.0] - 2024-01-15 - Production Ready

### 🎉 Première Release Complète

#### ✨ Nouvelles Fonctionnalités

- **Contrôle VMI Purevent** : Support complet de la D1-07-9F avec 5 niveaux de vitesse
- **Monitoring CO₂** : Capteur A5-09-04 avec détection de qualité air
- **Monitoring Température/Humidité** : Capteur A5-04-01
- **Contrôle GPIO** : Support natif Raspberry Pi UART (ttyAMA0, ttyS0, serial0)
- **Contrôle USB** : Support EnOcean USB dongle (ttyUSB, ttyACM)
- **Auto-détection** : Mode automatique GPIO/USB avec fallback intelligent
- **MQTT Integration** : Publication complète des états sur topics MQTT
- **WebUI Dashboard** : Interface web avec status et contrôles
- **REST API** : Endpoints pour status, devices, commands, logs
- **Diagnostic Tool** : Outil de troubleshooting complet
- **Home Assistant UI** : Interface de configuration via Home Assistant

#### 🔧 Améliorations Techniques

- **EnOcean ESP3 Stack** : Implémentation complète du protocole
- **CRC8 Validation** : Vérification d'intégrité des paquets
- **Async/Await** : Architecture 100% asynchrone
- **Multi-architecture** : Support amd64, aarch64, armv7
- **Docker Alpine** : Image légère et sécurisée
- **AppArmor Security** : Profil sécurité renforcé
- **Logging** : Debug, Info, Warning, Error levels
- **Configuration** : Fichiers JSON + Home Assistant schema

#### 📚 Documentation

- ✅ README complet avec quick start
- ✅ DOCS.md technique (600+ lignes)
- ✅ INSTALL.md guide d'installation
- ✅ GPIO_USB_GUIDE.md configuration détaillée
- ✅ HOME_ASSISTANT_INTEGRATION.md intégration HA
- ✅ AUTOMATIONS.md exemples d'automatisations
- ✅ SUPPORTED_DEVICES.md appareils supportés
- ✅ CONTRIBUTING.md guide contribution

#### 🧪 Tests & CI/CD

- ✅ 20+ unit tests
- ✅ GitHub Actions CI/CD pipeline
- ✅ Multi-architecture Docker builds
- ✅ Automated testing on push

#### 🐛 Bugs Corrigés

N/A - Première release

#### ⚠️ Notes de Migration

N/A - Première release

---

## [0.2.0] - À Venir

### Prévisions

#### ✨ Nouvelles Fonctionnalités

- [ ] Native Home Assistant Entities (intégration native HA)
- [ ] Lovelace Dashboard Template (dashboard prêt à l'emploi)
- [ ] Semi-Automatic Pairing (auto discovery des appareils)
- [ ] Historical Charts (graphiques dans WebUI)
- [ ] Device Health Status (monitoring batterie, signal)
- [ ] Support YAML Configuration (alternative JSON)

#### 🔧 Améliorations

- [ ] Performance optimisations
- [ ] Support capteurs additionnels (luminance, pression)
- [ ] WebUI amélioré avec graphiques en temps réel
- [ ] Documentation supplémentaires

---

## Support et Issues

### Signaler un Bug

1. GitHub Issues : https://github.com/ricolaflo88/Ventilairsec2HA/issues
2. Incluez :
   - Adresse appareil (ex: 0x0421574F)
   - Logs du module (DEBUG level)
   - Type de connexion (GPIO/USB)
   - Système d'exploitation

---

Mise à jour : **2024-01-15**  
Maintenu par : **ricolaflo88**
