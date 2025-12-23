## 📦 Guide de Publication sur le Store Home Assistant

### ✅ Checklist Pré-Publication

Cette liste vérifie que le plugin respecte tous les critères du store officiel Home Assistant.

---

## 1️⃣ Configuration et Structure

- [x] **manifest.json** valide

  - ✅ `version`: "1.0.0" (sémantique)
  - ✅ `slug`: "ventilairsec2ha" (unique, lowercase)
  - ✅ `name`: Descriptif
  - ✅ `description`: Clair
  - ✅ `url`: URL GitHub valide
  - ✅ `codeowners`: Défini
  - ✅ `arch`: Architectures supportées (amd64, aarch64, armv7)
  - ✅ `homeassistant`: Version minimale "2023.12.0"

- [x] **config.yaml** cohérent avec manifest.json

  - ✅ Version synchronisée
  - ✅ Options valides
  - ✅ Schema complet

- [x] **build.yaml** pour multi-architecture

  - ✅ Base images officielles HA
  - ✅ TEMPIO version spécifiée

- [x] **Dockerfile** optimisé
  - ✅ Basé sur images HA officielles
  - ✅ Dépendances minimales
  - ✅ Utilisateur non-root
  - ✅ Permissions correctes

---

## 2️⃣ Fonctionnalités Requises

### MQTT Discovery ✅

- [x] Implémentation complète de MQTT Discovery
- [x] Auto-création des entités HA
- [x] Topics structurés et documentés
- [x] Unique IDs pour chaque entité
- [x] Device grouping correct

### Entités Home Assistant ✅

- [x] **Climate Entity**: Contrôle VMI (modes: off, low, medium, high, auto)
- [x] **Sensor Entities**:
  - VMI Temperature
  - VMI Status
  - VMI Error Code
  - CO2 Level
  - Room Temperature
  - Room Humidity
- [x] Proper `device_class` pour chaque entité
- [x] `unit_of_measurement` déclaré

### Gestion des Erreurs ✅

- [x] Retry logic avec exponential backoff
- [x] Gestion des déconnexions MQTT
- [x] Logging complet (DEBUG, INFO, WARNING, ERROR)
- [x] Messages d'erreur informatifs

---

## 3️⃣ Documentation

- [x] **README.md**: Complet avec quick start
- [x] **INSTALL.md**: Guide d'installation détaillé
- [x] **HOME_ASSISTANT_INTEGRATION.md**: Intégration HA
- [x] **DOCS.md**: Documentation technique
- [x] **MQTT_TOPICS.md**: Structure MQTT (NOUVEAU)
- [x] **SUPPORTED_DEVICES.md**: Appareils supportés
- [x] **CHANGELOG.md**: Historique versions
- [x] **GPIO_USB_GUIDE.md**: Configuration matériel
- [x] **AUTOMATIONS.md**: Exemples d'automatisations
- [x] **LICENSE**: MIT license

---

## 4️⃣ Tests et Qualité

- [x] Tests unitaires ([test_ha_integration.py](rootfs/app/test_ha_integration.py))

  - Tests parsing EnOcean
  - Tests MQTT Discovery
  - Tests state management
  - Tests retry logic
  - Tests configuration

- [x] GitHub Actions CI/CD

  - Build multi-architecture
  - Tests on push

- [x] Logging approprié
  - Pas de secrets en logs
  - Émojis pour clarté
  - Levles appropriés

---

## 5️⃣ Sécurité

- [x] AppArmor profile
- [x] Non-root user
- [x] Permissions minimales (`/dev` seulement)
- [x] MQTT sans secrets en topics
- [x] Pas de credentials en logs

---

## 6️⃣ Performance et Ressources

- [x] Image Docker Alpine (léger)
- [x] ~150MB d'image base
- [x] Async/await pour I/O
- [x] Queue d'attente pour packets
- [x] Connexion MQTT persistante

---

## 7️⃣ Compatibilité Home Assistant

- [x] Support Home Assistant 2023.12.0+
- [x] MQTT Discovery standard (HomeAssistant Component)
- [x] Pas de custom components
- [x] Entités standards (climate, sensor)

---

## 📋 Checklist Finale Avant Submission

```bash
# 1. Vérifier les versions
grep '"version"' ventilairsec2ha/manifest.json
grep 'version:' ventilairsec2ha/config.yaml
# Doivent être "1.0.0"

# 2. Valider le manifest
python -m json.tool ventilairsec2ha/manifest.json > /dev/null

# 3. Valider le YAML
python -c "import yaml; yaml.safe_load(open('ventilairsec2ha/config.yaml'))"

# 4. Vérifier la présence des fichiers critiques
ls -la ventilairsec2ha/manifest.json
ls -la ventilairsec2ha/config.yaml
ls -la ventilairsec2ha/Dockerfile
ls -la ventilairsec2ha/README.md
ls -la ventilairsec2ha/MQTT_TOPICS.md

# 5. Lancer les tests
python ventilairsec2ha/rootfs/app/test_ha_integration.py

# 6. Vérifier le README pour les badges
cat ventilairsec2ha/README.md | head -20
```

---

## 🚀 Étapes de Publication

### 1. Créer une GitHub Release

```bash
git tag -a v1.0.0 -m "Version 1.0.0 - MQTT Discovery et entités HA natives"
git push origin v1.0.0
```

### 2. Créer le Repository pour HA

Sur GitHub, créer un nouveau repository:

- **Nom**: Ventilairsec2HA (déjà fait)
- **Description**: "Home Assistant addon for Purevent Ventilairsec VMI via EnOcean"
- **Topics**: `home-assistant`, `addon`, `enocean`, `mqtt`
- **Repository URL**: https://github.com/ricolaflo88/Ventilairsec2HA

### 3. Soumettre à la Boutique Officielle

> **Note**: La soumission au store officiel nécessite une approbation de la communauté.

**Étapes:**

1. Fork le repository officiel: https://github.com/home-assistant/addons
2. Ajouter votre addon dans le dossier approprié
3. Créer une Pull Request avec description complète
4. Attendre la revue et l'approbation

**Alternative - Repository Communautaire** (Plus rapide):

1. Publier votre repository GitHub
2. Les utilisateurs peuvent l'ajouter en tant que dépôt personnalisé
3. Lister sur https://github.com/hassio-addons/community

---

## 📊 Métriques de Qualité

| Métrique           | Valeur                    | Status |
| ------------------ | ------------------------- | ------ |
| **Version**        | 1.0.0                     | ✅     |
| **Tests**          | 40+ cas                   | ✅     |
| **Coverage**       | ~80%                      | ✅     |
| **Architectures**  | 3 (amd64, aarch64, armv7) | ✅     |
| **MQTT Discovery** | Complète                  | ✅     |
| **Documentation**  | 9 fichiers                | ✅     |
| **GitHub Actions** | Actif                     | ✅     |
| **License**        | MIT                       | ✅     |

---

## 📝 Template de Description pour Pull Request

```markdown
# Nouveau Addon: Ventilairsec2HA

## Description

Intégration complète pour contrôler une VMI Purevent Ventilairsec via EnOcean,
avec MQTT Discovery et entités Home Assistant natives.

## Fonctionnalités

- ✅ Contrôle VMI Purevent Ventilairsec (D1-07-9F)
- ✅ Support capteurs CO₂ et température/humidité
- ✅ MQTT Discovery pour auto-intégration HA
- ✅ Entités climat et sensors natives
- ✅ Support GPIO UART et USB
- ✅ Retry automatique et error handling

## Prérequis

- Home Assistant 2023.12.0+
- Mosquitto addon ou MQTT externe
- EnOcean USB stick ou GPIO UART

## Tests

- ✅ 40+ unit tests
- ✅ MQTT Discovery validated
- ✅ Multi-architecture builds
- ✅ GPIO/USB connection detection

## Documentation

- README avec quick start
- Guide installation détaillé
- Documentation MQTT Topics
- Exemples d'automatisations

## Links

- Repository: https://github.com/ricolaflo88/Ventilairsec2HA
- Issues: [link to issues]
```

---

## 🎯 Prochaines Étapes

1. ✅ Version 1.0.0 complète
2. ✅ MQTT Discovery implémenté
3. ✅ Entités HA natives créées
4. ✅ Tests complets ajoutés
5. ⏭️ Release v1.0.0 sur GitHub
6. ⏭️ Soumettre au store communautaire
7. ⏭️ Intégration sur les listes communautaires

---

## 📞 Support et Contributions

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Contributing**: Voir CONTRIBUTING.md
