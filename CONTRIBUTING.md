# 🤝 Guide de Contribution

Merci de votre intérêt pour contribuer à **Ventilairsec2HA** ! Ce document décrit les processus et procédures pour contribuer au projet.

## 📋 Code de Conduite

Ce projet adopte le Covenant Code of Conduct. Tous les contributeurs sont attendus de respecter ce code. Merci de voir [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## 🚀 Comment Contribuer

### 1. Signaler des Bugs

**Avant de signaler un bug :**

- Vérifier que le bug n'a pas déjà été signalé
- Consulter la [documentation](ventilairsec2ha/DOCS.md)
- Vérifier les configurations recommandées

**Pour signaler un bug :**

1. Aller à [Issues GitHub](https://github.com/ricolaflo88/Ventilairsec2HA/issues)
2. Cliquer sur **New Issue > Bug Report**
3. Remplir tous les champs:
   - Description claire du problème
   - Étapes pour reproduire
   - Résultat attendu vs résultat actuel
   - Environment (version HA, version addon, appareils, etc.)
   - Logs complets avec `log_level: debug`

### 2. Proposer des Améliorations

**Pour une nouvelle fonctionnalité :**

1. Aller à [Issues GitHub](https://github.com/ricolaflo88/Ventilairsec2HA/issues)
2. Cliquer sur **New Issue > Feature Request**
3. Décrire:
   - Le problème résolu
   - Votre solution proposée
   - Alternatives considérées
   - Impact et cas d'usage

### 3. Soumettre du Code

#### Setup de Développement

```bash
# Clone le repository
git clone https://github.com/yourusername/Ventilairsec2HA.git
cd Ventilairsec2HA

# Créer une branche feature
git checkout -b feature/your-feature-name

# Installer les dépendances
pip install -r ventilairsec2ha/rootfs/requirements.txt
pip install pytest pylint flake8 black yamllint

# Installer les hooks pre-commit (optionnel)
pip install pre-commit
pre-commit install
```

#### Code Style

**Python (PEP 8):**

```bash
# Format avec Black
black ventilairsec2ha/rootfs/app/

# Lint avec Flake8
flake8 ventilairsec2ha/rootfs/app/ --max-line-length=120

# Analyse statique
pylint ventilairsec2ha/rootfs/app/
```

**YAML:**

```bash
# Valider YAML
yamllint -d relaxed ventilairsec2ha/config.yaml
```

#### Tests

```bash
# Lancer tous les tests
pytest tests/ -v

# Tester un fichier spécifique
pytest tests/test_addon.py -v

# Avec couverture
pytest --cov=ventilairsec2ha tests/
```

#### Workflow de Pull Request

1. **Créer une branche feature**

   ```bash
   git checkout -b feature/descriptive-name
   ```

2. **Développer et tester**

   ```bash
   # Votre développement...
   git add .
   git commit -m "feat: add amazing feature"
   ```

3. **Soumettre la PR**

   - Pousser vers votre fork: `git push origin feature/descriptive-name`
   - Ouvrir une Pull Request sur le repo principal
   - Remplir le template de PR complet

4. **Répondre aux reviews**
   - Adresser les commentaires des reviewers
   - Faire des commits supplémentaires si nécessaire
   - Re-demander une review quand prêt

### 4. Améliorer la Documentation

**Documentation à mettre à jour :**

- [README.md](README.md) - Vue d'ensemble
- [ventilairsec2ha/README.md](ventilairsec2ha/README.md) - Addon
- [ventilairsec2ha/DOCS.md](ventilairsec2ha/DOCS.md) - Technique
- [ventilairsec2ha/INSTALL.md](ventilairsec2ha/INSTALL.md) - Installation

**Pour améliorer la doc :**

1. Fork et créer une branche
2. Éditer les fichiers Markdown
3. Vérifier la syntaxe: `yamllint` et `markdownlint`
4. Soumettre une PR

---

## 📝 Messages de Commit

Suivre le format [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**

- `feat`: Nouvelle fonctionnalité
- `fix`: Correction de bug
- `docs`: Changements de documentation
- `style`: Formatage du code
- `refactor`: Refactoring de code
- `perf`: Améliorations de performance
- `test`: Ajout/modification de tests
- `chore`: Maintenance, dependencies, etc.

**Exemples:**

```
feat(packet): add support for new RORG type A5-10-01
fix(mqtt): fix connection timeout on broker unavailable
docs(install): update installation instructions for Docker
test(device): add unit tests for device manager
```

---

## 🔍 Checklist avant PR

- [ ] Le code suit les conventions de style (PEP 8, etc.)
- [ ] Les tests passent: `pytest tests/`
- [ ] Le linting passe: `flake8 ventilairsec2ha/rootfs/app/`
- [ ] La documentation est à jour
- [ ] Le CHANGELOG.md est mis à jour
- [ ] Pas de fichiers inutiles committés (.pyc, **pycache**, etc.)
- [ ] Le commit message est explicite
- [ ] La branche est à jour avec `main`: `git rebase main`

---

## 🏗️ Architecture et Structure

### Structure du Projet

```
Ventilairsec2HA/
├── ventilairsec2ha/              # Addon principal
│   ├── rootfs/app/               # Code application
│   │   ├── run.py               # Point d'entrée
│   │   ├── config.py            # Configuration
│   │   ├── enocean_*.py         # Modules EnOcean
│   │   ├── ventilairsec_*.py    # Gestion VMI
│   │   ├── home_assistant_*.py  # Intégration HA
│   │   └── webui_*.py           # Serveur WebUI
│   ├── config.yaml              # Config addon HA
│   ├── build.yaml               # Config Docker
│   ├── Dockerfile               # Image Docker
│   ├── README.md                # Doc addon
│   ├── DOCS.md                  # Tech doc
│   └── INSTALL.md               # Installation
├── tests/                        # Tests unitaires
├── .github/workflows/           # CI/CD
├── repository.yaml              # Config repo
├── LICENSE                      # Licence MIT
└── README.md                    # README principal
```

### Modules Principaux

#### `config.py`

- Charge configuration depuis `/data/options.json`
- Gère les paramètres et logging

#### `enocean_constants.py`

- Constantes EnOcean (RORG, adresses, etc.)
- Définitions des appareils

#### `enocean_packet.py`

- Parsing et création des paquets ESP3
- Gestion du buffer

#### `enocean_communicator.py`

- Communication série
- Envoi/réception des paquets

#### `ventilairsec_manager.py`

- Gestion de la VMI et capteurs
- Décodage des trames
- État des appareils

#### `home_assistant_integration.py`

- Publication MQTT
- Topics et payloads

#### `webui_server.py`

- Serveur aiohttp
- API REST et dashboard

---

## 🧪 Ajouter des Tests

**Structure d'un test:**

```python
import unittest
from pathlib import Path
import sys

# Ajouter app au path
app_dir = Path(__file__).parent.parent / "ventilairsec2ha" / "rootfs" / "app"
sys.path.insert(0, str(app_dir))

from enocean_packet import EnOceanPacket

class TestMyFeature(unittest.TestCase):
    """Test ma nouvelle fonctionnalité"""

    def setUp(self):
        """Setup avant chaque test"""
        pass

    def tearDown(self):
        """Cleanup après chaque test"""
        pass

    def test_something(self):
        """Test d'une fonction spécifique"""
        result = my_function()
        self.assertEqual(result, expected_value)

    def test_error_handling(self):
        """Test gestion d'erreurs"""
        with self.assertRaises(ValueError):
            invalid_function()

if __name__ == '__main__':
    unittest.main()
```

---

## 📚 Ressources pour Contribueurs

### Documentation

- [EnOcean Specification](https://www.enocean.com/en/enocean-modules/enocean-profiles/)
- [ESP3 Protocol](https://www.enocean.com/esp3protocol/)
- [Home Assistant Add-on Dev](https://developers.home-assistant.io/docs/add-ons/)
- [MQTT Protocol](https://mqtt.org/)

### Outils

- [Python 3.9+](https://www.python.org/)
- [Docker](https://www.docker.com/)
- [Git](https://git-scm.com/)
- [VS Code](https://code.visualstudio.com/)

### Pour Apprendre

- Lire le code existant
- Consulter les issues ouvertes
- Participer aux discussions
- Expérimenter localement

---

## 🐛 Reporting Issues

### Sécurité

**NE PAS créer une issue publique pour les failles de sécurité !**

Envoyer un email à: ricolaflo88@users.noreply.github.com

Incluire:

- Description de la vulnérabilité
- Étapes pour reproduire
- Impact potentiel
- Suggestions de fix si disponibles

### Autres Issues

Créer une issue GitHub avec:

- Titre clair et descriptif
- Description détaillée
- Reproduction steps si applicable
- Logs en mode debug
- Environment (versions, hardware, etc.)
- Screenshots si pertinent

---

## 📞 Contact et Questions

- **Issues GitHub:** Pour les bugs et features
- **Discussions:** Pour les questions générales
- **Email:** ricolaflo88@users.noreply.github.com (sécurité seulement)

---

## ✅ Standards de Qualité

### Code Quality

- ✅ Tests: >80% couverture
- ✅ Linting: 0 erreurs Pylint
- ✅ Type hints: Recommandés
- ✅ Documentation: Docstrings pour toutes les fonctions

### Performance

- ✅ CPU: <10% en usage normal
- ✅ Mémoire: <100MB
- ✅ Startup: <10 secondes
- ✅ Latence MQTT: <1 seconde

### Sécurité

- ✅ Pas de hardcoding de secrets
- ✅ Validation des entrées
- ✅ Permissions minimales
- ✅ Dépendances à jour

---

## 📅 Roadmap

Pour le roadmap du projet, voir:

- [Milestones GitHub](https://github.com/ricolaflo88/Ventilairsec2HA/milestones)
- [Projects GitHub](https://github.com/ricolaflo88/Ventilairsec2HA/projects)

---

## 🙏 Remerciements

Merci à tous les contributeurs qui aident à améliorer ce projet !

**Contributeurs:**

- Vous ! 👋

---

<div align="center">

**Fait avec ❤️ pour la communauté**

Questions ? Créez une [issue](https://github.com/ricolaflo88/Ventilairsec2HA/issues) ou une [discussion](https://github.com/ricolaflo88/Ventilairsec2HA/discussions)

</div>
