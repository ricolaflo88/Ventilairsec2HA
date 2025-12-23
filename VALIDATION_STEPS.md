# Guide de Validation - Manifest, Config Flow et Tests

## 1. Validation du Manifest

### Vérifier le format JSON

\`\`\`bash
python3 -m json.tool custom_components/ventilairsec2ha/manifest.json
\`\`\`

### Exécuter les tests manifest

\`\`\`bash
pytest tests/test_manifest.py -v
\`\`\`

**Checklist:**

- ✅ `manifest_version`: 1
- ✅ `domain`: "ventilairsec2ha"
- ✅ `name`: descriptif
- ✅ `config_flow`: true
- ✅ `homeassistant`: "2024.1.0" minimum
- ✅ `requirements`: enocean>=0.60.0
- ✅ `version`: 1.0.0
- ✅ `codeowners`: ["@ricolaflo88"]

## 2. Validation Config Flow

### Vérifier la structure

\`\`\`bash
python3 -c "from custom_components.ventilairsec2ha.config_flow import VentilairsecConfigFlow; print('✅ Config flow importable')"
\`\`\`

### Exécuter les tests config flow

\`\`\`bash
pytest tests/test_config_flow.py -v
\`\`\`

**Checklist:**

- ✅ Classe `VentilairsecConfigFlow` hérite de `config_entries.ConfigFlow`
- ✅ Méthode `async_step_user()` implémentée
- ✅ Méthode `async_step_sensors()` implémentée
- ✅ Validation de connexion
- ✅ Prévention des doublons (unique_id)
- ✅ OptionsFlow pour options d'exécution

## 3. Validation Tests Unitaires

### Installer dépendances dev

\`\`\`bash
pip install -r requirements-dev.txt
\`\`\`

### Exécuter tous les tests

\`\`\`bash
pytest tests/ -v --cov
\`\`\`

### Tests spécifiques

\`\`\`bash

# Tests manifest

pytest tests/test_manifest.py -v

# Tests config flow

pytest tests/test_config_flow.py -v

# Avec couverture de code

pytest tests/ -v --cov=custom_components/ventilairsec2ha --cov-report=html
\`\`\`

## 4. Validation Qualité du Code

### Linting avec pylint

\`\`\`bash
pylint custom_components/ventilairsec2ha --disable=all --enable=E,F
\`\`\`

### Formatting avec black

\`\`\`bash
black --check custom_components/ventilairsec2ha
\`\`\`

### Type checking

\`\`\`bash
mypy custom_components/ventilairsec2ha
\`\`\`

### Vérification flake8

\`\`\`bash
flake8 custom_components/ventilairsec2ha --max-line-length=100
\`\`\`

## 5. Validation Home Assistant

### Vérifier la structure de l'intégration

\`\`\`bash
python3 -m homeassistant --script check_config ./
\`\`\`

### Charger l'intégration localement

Ajouter au `configuration.yaml`:
\`\`\`yaml
ventilairsec2ha:
\`\`\`

## 6. Validation Complète (Automation)

Créer un script de validation complète:

\`\`\`bash
#!/bin/bash
set -e

echo "🔍 Validation Manifest..."
python3 -m json.tool custom_components/ventilairsec2ha/manifest.json > /dev/null
pytest tests/test_manifest.py -v

echo "🔍 Validation Config Flow..."
pytest tests/test_config_flow.py -v

echo "🔍 Validation Code Quality..."
pylint custom_components/ventilairsec2ha --disable=all --enable=E,F
flake8 custom_components/ventilairsec2ha --max-line-length=100

echo "✅ Toutes les validations réussies!"
\`\`\`

## Résumé

| Composant       | Validé | Commande                           |
| --------------- | ------ | ---------------------------------- |
| Manifest JSON   | ✅     | `pytest tests/test_manifest.py`    |
| Config Flow     | ✅     | `pytest tests/test_config_flow.py` |
| Tests Unitaires | ✅     | `pytest tests/ -v`                 |
| Code Quality    | ✅     | `pylint && flake8`                 |
| Home Assistant  | ✅     | `check_config`                     |
