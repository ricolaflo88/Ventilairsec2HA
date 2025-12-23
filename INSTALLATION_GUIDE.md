# 📦 Guide d'Installation - Ventilairsec2HA

## Problème Initial
```
zsh: command not found: pip
```

## Solution Rapide (3 étapes)

### 1️⃣ Installer les dépendances système

**Option A: Avec apt (Debian/Ubuntu)**
```bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv python3-dev
```

**Option B: Avec le script fourni**
```bash
bash install-dependencies.sh
```

### 2️⃣ Vérifier l'installation
```bash
python3 --version  # Devrait afficher Python 3.x
pip3 --version     # Devrait afficher pip version
```

### 3️⃣ Créer un alias pip (optionnel mais recommandé)
```bash
# Pour zsh
echo "alias pip=pip3" >> ~/.zshrc
source ~/.zshrc

# Pour bash
echo "alias pip=pip3" >> ~/.bashrc
source ~/.bashrc
```

---

## Installation Complète du Projet

### Option 1: Script automatisé (Recommandé)
```bash
# Tout en un
bash setup.sh

# Puis valider
bash validate.sh
```

### Option 2: Commandes manuelles

```bash
# 1. Installer les dépendances système
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv

# 2. Créer l'environnement virtuel
python3 -m venv venv

# 3. Activer l'environnement
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# 4. Mettre à jour pip
pip install --upgrade pip setuptools wheel

# 5. Installer les dépendances
pip install -r requirements-dev.txt
```

### Option 3: Avec Makefile
```bash
# Installer dépendances système
make install

# Configurer le projet
make setup

# Valider
make validate

# Tests
make test
```

---

## Vérifications Après Installation

### Vérifier pip
```bash
pip --version
pip3 --version
which pip
which pip3
```

### Vérifier les dépendances installées
```bash
pip list | grep -E "pytest|homeassistant|enocean"
```

### Vérifier les imports Python
```bash
python3 -c "import pytest; print('✅ pytest OK')"
python3 -c "import homeassistant; print('✅ homeassistant OK')"
python3 -c "import enocean; print('✅ enocean OK')"
```

---

## Dépannage

### Erreur: "command not found: pip"
**Cause**: pip3 n'est pas dans le PATH

**Solutions**:
```bash
# Option 1: Utiliser pip3 à la place
pip3 install -r requirements-dev.txt

# Option 2: Créer un alias
alias pip=pip3
pip install -r requirements-dev.txt

# Option 3: Ajouter au PATH dans ~/.bashrc ou ~/.zshrc
export PATH="$PATH:$(python3 -m site --user-base)/bin"
```

### Erreur: "command not found: python3"
**Cause**: Python3 n'est pas installé

**Solution**:
```bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip
```

### Erreur: Permission denied
**Cause**: Droits d'accès insuffisants

**Solution**:
```bash
# Ne PAS utiliser sudo pour pip avec venv activé
pip install -r requirements-dev.txt  # Sans sudo!
```

### Environnement virtuel ne s'active pas
**Cause**: Mauvais shell ou chemin

**Solution**:
```bash
# Vérifier le shell
echo $SHELL

# Réactiver avec le bon chemin
source /workspaces/Ventilairsec2HA/venv/bin/activate
```

---

## Structure Finale

Après installation réussie:
```
Ventilairsec2HA/
├── venv/                    # ← Environnement virtuel
├── custom_components/
│   └── ventilairsec2ha/
│       ├── __init__.py
│       ├── config_flow.py
│       ├── const.py
│       └── manifest.json
├── tests/
│   ├── test_manifest.py
│   ├── test_config_flow.py
│   └── conftest.py
├── requirements-dev.txt     # ← Dépendances Python
├── setup.sh                 # ← Script d'installation
├── validate.sh              # ← Script de validation
├── Makefile                 # ← Alternative aux scripts
└── INSTALLATION_GUIDE.md    # ← Ce fichier
```

---

## Commandes Usuelles

```bash
# Activer l'environnement
source venv/bin/activate

# Désactiver l'environnement
deactivate

# Lancer les tests
pytest tests/ -v

# Générer rapport de couverture
pytest tests/ --cov --cov-report=html

# Valider le manifest
python3 -m json.tool custom_components/ventilairsec2ha/manifest.json

# Linter le code
pylint custom_components/ventilairsec2ha

# Nettoyer les caches
make clean
```

---

## Prochaines Étapes

1. ✅ Installer pip (ce guide)
2. ⬜ Configurer l'intégration Home Assistant
3. ⬜ Lancer les tests: `bash validate.sh`
4. ⬜ Préparer la soumission à la boutique

---

## Support

Si vous avez des problèmes:

1. Vérifier les logs: `pytest tests/ -v -s`
2. Vérifier les versions: `python3 --version`, `pip3 --version`
3. Consulter les rapports: `htmlcov/index.html`
4. Ouvrir une issue: https://github.com/ricolaflo88/Ventilairsec2HA/issues
