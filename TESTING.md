# 🧪 Guide de Test - Ventilairsec2HA

Ce document décrit comment tester l'addon Ventilairsec2HA en développement et avant déploiement.

## 📋 Table des Matières

1. [Tests Unitaires](#tests-unitaires)
2. [Tests d'Intégration](#tests-dintégration)
3. [Tests Manuels](#tests-manuels)
4. [Tests de Performance](#tests-de-performance)
5. [CI/CD](#cicd)

---

## 🧪 Tests Unitaires

### Installation des Dépendances

```bash
cd Ventilairsec2HA
pip install -r ventilairsec2ha/rootfs/requirements.txt
pip install pytest pytest-cov pytest-asyncio
```

### Lancer les Tests - Nouvelle Suite (Recommandé)

```bash
# Avec le script bash
bash run_tests.sh

# Ou directement avec Python3
python3 ventilairsec2ha/rootfs/app/test_ha_integration.py
```

**Nouvelle suite:** 40+ tests couvrant MQTT Discovery, entités HA, retry logic

### Tests Existants (pytest)

```bash
# Tous les tests
pytest tests/ -v

# Test spécifique
pytest tests/test_addon.py::TestEnOceanPacket -v

# Avec couverture
pytest --cov=ventilairsec2ha/rootfs/app tests/

# Mode watch (reruns on change)
pytest-watch tests/
```

### Structure des Tests

```
tests/
└── test_addon.py
    ├── TestEnOceanPacket      # Parsing/création paquets
    ├── TestRadioPacket        # Structure RadioPacket
    ├── TestPacketBuffer       # Gestion buffer
    ├── TestVentilairsecDevices # Logique VMI
    └── TestConfig             # Configuration
```

### Exemples de Tests

```python
# Test de parsing de paquet
def test_radio_packet_creation(self):
    packet = RadioPacket(...)
    self.assertEqual(packet.sender_hex, "0421574F")

# Test d'erreurs
def test_radio_packet_validation(self):
    with self.assertRaises(ValueError):
        RadioPacket(sender_addr=bytes([0x01]))
```

---

## 🔗 Tests d'Intégration

### Setup Local

```bash
# Créer un environnement de test avec Docker
docker-compose -f test-docker-compose.yml up

# Vérifier la connexion
docker ps
docker logs test_ventilairsec2ha

# Arrêter
docker-compose down
```

### Test avec Mosquitto

```bash
# Démarrer Mosquitto
docker run -it -p 1883:1883 eclipse-mosquitto

# Dans un autre terminal, subscriber
mosquitto_sub -h localhost -t "homeassistant/ventilairsec2ha/#" -v

# Publier un message test
mosquitto_pub -h localhost -t "test/topic" -m "test message"
```

### Test de Communication Série

```bash
# Voir l'addon
docker exec -it addon_ventilairsec2ha bash

# Vérifier les ports
ls -la /dev/ttyUSB*

# Tester la communication
python3 -c "import serial; s = serial.Serial('/dev/ttyUSB0', 57600); print(s.readline())"
```

---

## 🧑‍💻 Tests Manuels

### Checklist de Pré-Déploiement

#### Configuration

- [ ] Port série correctement configuré
- [ ] MQTT broker accessible
- [ ] Logs en mode info
- [ ] Permissions fichiers OK

#### Fonctionnalité

- [ ] Addon démarre sans erreurs
- [ ] WebUI accessible sur port 8080
- [ ] API /api/status répond
- [ ] API /api/devices répond

#### Appareils

- [ ] VMI détectée (0x0421574F)
- [ ] CO₂ détecté (0x81003227)
- [ ] Temp/Humidité détecté (0x810054F5)
- [ ] Assistant détecté (0x0422407D)

#### MQTT

- [ ] Topics publiés toutes les 10s
- [ ] Format JSON valide
- [ ] Données mises à jour

#### Commandes

- [ ] Changement vitesse VMI fonctionne
- [ ] Logs des commandes présents
- [ ] Pas d'erreurs

### Tests Manuels Détaillés

#### 1. Test de Réception de Paquet

```bash
# Activer debug et surveiller
docker logs -f addon_ventilairsec2ha | grep "📦"

# Envoi depuis un device (VMI, capteur, etc.)
# Vérifier que le paquet est reçu et parsé
```

#### 2. Test MQTT

```bash
# Terminal 1: Subscribe
mosquitto_sub -h mosquitto -t "homeassistant/ventilairsec2ha/#" -v

# Attendre les publications (toutes les 10s)
# Vérifier le format des données

# Terminal 2: Envoi commande
mosquitto_pub -h mosquitto -t "homeassistant/ventilairsec2ha/command/set_speed" -m "75"

# Vérifier que la commande est exécutée
```

#### 3. Test WebUI

```bash
# Ouvrir dans navigateur
http://homeassistant.local:8080

# Vérifier:
# - Titre et description
# - Status du système
# - Liste des appareils
# - Données en temps réel
```

#### 4. Test d'Erreur

```bash
# Débrancher la clé EnOcean
# Vérifier le message d'erreur
# Rebrancher et vérifier la reconnexion

# Arrêter Mosquitto
docker stop mosquitto
# Vérifier l'handling de l'erreur
# Redémarrer et vérifier la reconnexion
```

---

## 📊 Tests de Performance

### Ressources

```bash
# Monitorer en temps réel
docker stats addon_ventilairsec2ha

# Ou via SSH
top -p $(docker inspect -f '{{.State.Pid}}' addon_ventilairsec2ha)
```

### Benchmarks Attendus

| Métrique       | Attendu | Limite |
| -------------- | ------- | ------ |
| CPU            | <5%     | <10%   |
| Mémoire        | <50MB   | <100MB |
| Startup        | <10s    | <20s   |
| Latence MQTT   | <100ms  | <1s    |
| CPU par paquet | <0.1%   | <0.5%  |

### Profiling

```python
# Ajouter au code pour tester
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Votre code ici
async def process_packet(packet):
    pass

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)  # Top 10 fonctions
```

### Load Testing

```bash
# Simuler plusieurs paquets/seconde
# Vérifier que l'addon reste stable

# Générer paquets de test
python3 -c "
import time
for i in range(1000):
    # Simuler réception paquet
    print(f'Paquet {i}')
    time.sleep(0.01)
"
```

---

## 🔄 CI/CD

### GitHub Actions

Les tests s'exécutent automatiquement:

```yaml
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: pytest tests/
```

### Vérifier Localement ce que CI Fait

```bash
# Installer les dépendances comme CI
pip install pylint flake8 black yamllint pytest

# Linting
flake8 ventilairsec2ha/rootfs/app/
pylint ventilairsec2ha/rootfs/app/

# Tests
pytest tests/ -v

# YAML
yamllint ventilairsec2ha/config.yaml
```

### Déboguer les Erreurs de Build

```bash
# Vérifier les logs de build
docker build -f ventilairsec2ha/Dockerfile ventilairsec2ha/

# Ou avec buildx pour multi-arch
docker buildx build --load -f ventilairsec2ha/Dockerfile ventilairsec2ha/
```

---

## 🐛 Debugging

### Logs et Debugging

```bash
# Modo debug
docker exec addon_ventilairsec2ha cat /data/options.json

# Lancer avec debug logging
curl -X POST http://homeassistant.local/api/addon_options/ventilairsec2ha \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"log_level": "debug"}'

# Redémarrer l'addon
docker restart addon_ventilairsec2ha

# Voir les logs
docker logs -f addon_ventilairsec2ha
```

### Points de Break

```python
# Ajouter du debug dans le code
import logging
logger = logging.getLogger(__name__)

# Dans votre fonction
logger.debug(f"Variable valeur: {my_var}")
logger.info(f"État: {state}")
logger.warning(f"Attention: {problem}")
logger.error(f"Erreur: {error}")
```

### Inspection du Buffer

```python
# Dans enocean_packet.py
def extract_packet(self):
    logger.debug(f"Buffer content: {self.buffer.hex()}")
    logger.debug(f"Buffer length: {len(self.buffer)}")
    # ... reste du code
```

---

## 📝 Reporting de Tests

### Template de Rapport

```markdown
## Test Report - Ventilairsec2HA v0.1.0

### Configuration

- Home Assistant version: 2024.1.0
- Python version: 3.11
- Docker version: 24.0.0
- Hardware: Raspberry Pi 4

### Tests Effectués

- [x] Unit tests: 15/15 passed
- [x] Integration tests: 10/10 passed
- [x] Manual tests: 20/20 passed
- [x] Performance: OK
- [x] Security: OK

### Résultats

- Code coverage: 85%
- Build time: 45s
- Package size: 42MB

### Issues

- None

### Conclusion

✅ Ready for deployment

Date: 2024-12-06
Tester: your-name
```

---

## ✅ Checklist de Validation

Avant de déployer une nouvelle version:

```
Fonctionnalité
- [ ] Fonctionnalité complète
- [ ] Pas de bugs connus
- [ ] Documentation à jour

Tests
- [ ] Tests unitaires ✅
- [ ] Tests d'intégration ✅
- [ ] Tests manuels ✅
- [ ] Coverage > 80%

Performance
- [ ] CPU < 5%
- [ ] Mémoire < 50MB
- [ ] Startup < 10s

Qualité
- [ ] Linting ✅
- [ ] Formatting ✅
- [ ] Type hints ✅

Documentation
- [ ] README.md ✅
- [ ] DOCS.md ✅
- [ ] Changelog ✅
- [ ] Inline comments ✅

Sécurité
- [ ] Pas de secrets en dur
- [ ] Validation des entrées ✅
- [ ] Permissions minimales ✅

Build
- [ ] Build Docker ✅
- [ ] Push ECR/Registry ✅
- [ ] Tags vérifiés ✅
```

---

## 🤝 Contribution de Tests

Les nouvelles fonctionnalités doivent inclure des tests !

```bash
# Ajouter un test pour nouvelle feature
git checkout -b feat/new-feature
# ... développer la feature ...
# ... ajouter les tests ...
pytest tests/ -v
# Si ✅, soumettre PR
```

---

## 📞 Support de Test

Questions sur les tests ?

- Lire ce document
- Consulter les exemples dans `tests/`
- Ouvrir une [issue GitHub](https://github.com/ricolaflo88/Ventilairsec2HA/issues)

---

<div align="center">

**Happy Testing! 🚀**

</div>
