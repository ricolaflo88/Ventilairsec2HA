## 📚 Index de la Documentation v1.0.0

Guide pour naviguer dans la documentation complète de Ventilairsec2HA.

---

## 🎯 Commencer Ici

### Pour Utilisateurs

1. **[README.md](README.md)** - Vue d'ensemble générale
2. **[ventilairsec2ha/INSTALL.md](ventilairsec2ha/INSTALL.md)** - Guide d'installation
3. **[ventilairsec2ha/HOME_ASSISTANT_INTEGRATION.md](ventilairsec2ha/HOME_ASSISTANT_INTEGRATION.md)** - Intégration HA

### Pour Développeurs

1. **[ventilairsec2ha/DOCS.md](ventilairsec2ha/DOCS.md)** - Architecture technique
2. **[TESTING.md](TESTING.md)** - Guide des tests
3. **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribuer au projet

### Pour Publication

1. **[QUICK_START_PUBLICATION.md](QUICK_START_PUBLICATION.md)** - Guide rapide
2. **[STORE_PUBLICATION_GUIDE.md](STORE_PUBLICATION_GUIDE.md)** - Guide détaillé
3. **[verify_release.sh](verify_release.sh)** - Vérification pré-publication

---

## 📖 Documentation Complète

### Installation & Configuration

| Document                                                                       | Purpose                | Audience     |
| ------------------------------------------------------------------------------ | ---------------------- | ------------ |
| [INSTALL.md](ventilairsec2ha/INSTALL.md)                                       | Guide d'installation   | Utilisateurs |
| [HOME_ASSISTANT_INTEGRATION.md](ventilairsec2ha/HOME_ASSISTANT_INTEGRATION.md) | Intégration HA         | Utilisateurs |
| [GPIO_USB_GUIDE.md](ventilairsec2ha/GPIO_USB_GUIDE.md)                         | Configuration matériel | Développeurs |
| [SUPPORTED_DEVICES.md](ventilairsec2ha/SUPPORTED_DEVICES.md)                   | Appareils supportés    | Tous         |

### Technique & API

| Document                                         | Purpose                    | Audience             |
| ------------------------------------------------ | -------------------------- | -------------------- |
| [DOCS.md](ventilairsec2ha/DOCS.md)               | Documentation technique    | Développeurs         |
| [MQTT_TOPICS.md](ventilairsec2ha/MQTT_TOPICS.md) | Structure MQTT & Discovery | Développeurs/Avancés |
| [AUTOMATIONS.md](ventilairsec2ha/AUTOMATIONS.md) | Exemples d'automations     | Utilisateurs avancés |

### Tests & Qualité

| Document                                                                    | Purpose               | Audience     |
| --------------------------------------------------------------------------- | --------------------- | ------------ |
| [TESTING.md](TESTING.md)                                                    | Guide des tests       | Développeurs |
| [test_ha_integration.py](ventilairsec2ha/rootfs/app/test_ha_integration.py) | Tests unitaires (40+) | Développeurs |
| [run_tests.sh](run_tests.sh)                                                | Script de test        | Tous         |

### Publication & Release

| Document                                                 | Purpose                       | Audience     |
| -------------------------------------------------------- | ----------------------------- | ------------ |
| [QUICK_START_PUBLICATION.md](QUICK_START_PUBLICATION.md) | Guide rapide publication      | Mainteneurs  |
| [STORE_PUBLICATION_GUIDE.md](STORE_PUBLICATION_GUIDE.md) | Guide complet store HA        | Mainteneurs  |
| [RELEASE_NOTES_v1.0.0.md](RELEASE_NOTES_v1.0.0.md)       | Notes de version              | Tous         |
| [FINAL_SUMMARY.md](FINAL_SUMMARY.md)                     | Résumé complet v1.0.0         | Tous         |
| [CHANGES_DETAILED.md](CHANGES_DETAILED.md)               | Liste détaillée modifications | Développeurs |

### Historique & Contribution

| Document                                     | Purpose             | Audience      |
| -------------------------------------------- | ------------------- | ------------- |
| [CHANGELOG.md](ventilairsec2ha/CHANGELOG.md) | Historique versions | Tous          |
| [CONTRIBUTING.md](CONTRIBUTING.md)           | Guide contribution  | Contributeurs |
| [LICENSE](LICENSE)                           | MIT License         | Tous          |

---

## 🔍 Par Type de Lecteur

### 👤 Nouvel Utilisateur

1. Lire [README.md](README.md) (vue d'ensemble)
2. Suivre [INSTALL.md](ventilairsec2ha/INSTALL.md) (installation)
3. Consulter [HOME_ASSISTANT_INTEGRATION.md](ventilairsec2ha/HOME_ASSISTANT_INTEGRATION.md) (config HA)
4. Voir [AUTOMATIONS.md](ventilairsec2ha/AUTOMATIONS.md) pour des exemples

### 👨‍💻 Développeur

1. Lire [ventilairsec2ha/DOCS.md](ventilairsec2ha/DOCS.md) (architecture)
2. Consulter [TESTING.md](TESTING.md) (tests)
3. Voir [ventilairsec2ha/rootfs/app/](ventilairsec2ha/rootfs/app/) (code source)
4. Lire [CONTRIBUTING.md](CONTRIBUTING.md) pour contribuer

### 🏪 Mainteneur/Publisher

1. Vérifier [FINAL_SUMMARY.md](FINAL_SUMMARY.md) (état v1.0.0)
2. Suivre [QUICK_START_PUBLICATION.md](QUICK_START_PUBLICATION.md) (guide rapide)
3. Consulter [STORE_PUBLICATION_GUIDE.md](STORE_PUBLICATION_GUIDE.md) (détails)
4. Lancer [verify_release.sh](verify_release.sh) (vérification)

### 🔧 Troubleshooter

1. Voir [GPIO_USB_GUIDE.md](ventilairsec2ha/GPIO_USB_GUIDE.md) (matériel)
2. Consulter [MQTT_TOPICS.md](ventilairsec2ha/MQTT_TOPICS.md) (debugging MQTT)
3. Lancer [run_tests.sh](run_tests.sh) (vérifier tests)
4. Voir [DOCS.md](ventilairsec2ha/DOCS.md) architecture

---

## 🗂️ Arborescence Documentation

```
/
├── README.md                          # Vue d'ensemble
├── TESTING.md                         # Tests
├── CONTRIBUTING.md                    # Guide contribution
├── LICENSE                            # MIT License
│
├── STORE_PUBLICATION_GUIDE.md        # Guide store complet
├── QUICK_START_PUBLICATION.md        # Guide rapide
├── FINAL_SUMMARY.md                  # Résumé v1.0.0
├── RELEASE_NOTES_v1.0.0.md           # Notes de version
├── CHANGES_DETAILED.md               # Modifications détaillées
│
├── run_tests.sh                       # Script tests
├── verify_release.sh                  # Vérification pré-pub
│
└── ventilairsec2ha/
    ├── README.md                      # Addon README
    ├── INSTALL.md                     # Installation guide
    ├── DOCS.md                        # Docs techniques
    ├── CHANGELOG.md                   # Historique versions
    ├── MQTT_TOPICS.md                # Structure MQTT (NOUVEAU)
    ├── HOME_ASSISTANT_INTEGRATION.md  # Intégration HA
    ├── GPIO_USB_GUIDE.md              # Configuration matériel
    ├── SUPPORTED_DEVICES.md           # Appareils supportés
    ├── AUTOMATIONS.md                 # Exemples automations
    │
    ├── manifest.json                  # Addon manifest
    ├── config.yaml                    # Addon config
    ├── Dockerfile                     # Docker image
    ├── build.yaml                     # Build config
    │
    └── rootfs/app/
        ├── run.py                      # Point d'entrée
        ├── ha_entities.py              # Entités HA (NOUVEAU)
        ├── test_ha_integration.py      # Tests (NOUVEAU)
        ├── home_assistant_integration.py # HA integration
        ├── enocean_communicator.py     # Communication
        ├── ventilairsec_manager.py     # Gestion VMI
        ├── webui_server.py             # WebUI
        ├── config.py                   # Configuration
        └── ... (autres fichiers)
```

---

## 🎯 Checklist Lecture

Pour comprendre complètement le projet:

- [ ] Lire [README.md](README.md) (5 min)
- [ ] Voir [ventilairsec2ha/DOCS.md](ventilairsec2ha/DOCS.md) (20 min)
- [ ] Consulter [ventilairsec2ha/MQTT_TOPICS.md](ventilairsec2ha/MQTT_TOPICS.md) (10 min)
- [ ] Parcourir [TESTING.md](TESTING.md) (10 min)
- [ ] Lancer [run_tests.sh](run_tests.sh) (5 min)
- [ ] Lire [CONTRIBUTING.md](CONTRIBUTING.md) (10 min)

**Temps total:** ~60 minutes

---

## 🔗 Raccourcis Utiles

### Documentation Officielle

- [Home Assistant Docs](https://www.home-assistant.io/docs/)
- [EnOcean Official](https://www.enocean.com/)
- [MQTT Spec](https://mqtt.org/)

### Code Source

- [GitHub Repo](https://github.com/ricolaflo88/Ventilairsec2HA)
- [Code Source Addon](ventilairsec2ha/rootfs/app/)
- [Tests Unitaires](ventilairsec2ha/rootfs/app/test_ha_integration.py)

### Support

- [GitHub Issues](https://github.com/ricolaflo88/Ventilairsec2HA/issues)
- [GitHub Discussions](https://github.com/ricolaflo88/Ventilairsec2HA/discussions)

---

## 📊 Statistics Documentation

```
README.md:                        ~50 KB
Documentation Technique:          ~300 KB
Guides Installation:              ~100 KB
Code Source (Python):             ~200 KB
Tests:                            ~50 KB
─────────────────────────────
Total Documentation:              ~700 KB

Fichiers:                         ~70
```

---

**Bienvenue dans la documentation complète de Ventilairsec2HA v1.0.0! 🎉**

Pour toute question, consulter [CONTRIBUTING.md](CONTRIBUTING.md) ou ouvrir une issue sur GitHub.
