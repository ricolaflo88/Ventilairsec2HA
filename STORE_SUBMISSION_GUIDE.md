# Guide de Soumission - Home Assistant App Store

## Prérequis pour la Boutique

### 1. Dépôt GitHub
- Repository **public**
- README.md complet
- LICENSE valide (MIT/Apache 2.0 recommandé)
- Releases taguées en versioning sémantique

### 2. Structure Requise
\`\`\`
custom_components/ventilairsec2ha/
├── __init__.py
├── config_flow.py
├── manifest.json
├── strings.json
├── const.py
├── services.yaml
├── entity.py
├── binary_sensor.py
├── sensor.py
├── climate.py
└── translations/
    ├── en.json
    └── fr.json
\`\`\`

### 3. manifest.json - Checklist
- ✅ `manifest_version`: 1
- ✅ `domain`: unique et minuscule
- ✅ `name`: descriptif
- ✅ `codeowners`: contributeurs principaux
- ✅ `documentation`: lien GitHub
- ✅ `issue_tracker`: lien GitHub issues
- ✅ `requirements`: dépendances Python listées
- ✅ `homeassistant`: version minimale (2023.1.0 minimum)

### 4. Code Quality Requirements
\`\`\`bash
# Installer les outils
pip install homeassistant pylint flake8 pytest

# Valider la structure
python -m homeassistant.util.check_config ./

# Linting
pylint custom_components/ventilairsec2ha
flake8 custom_components/ventilairsec2ha --max-line-length=100

# Tests
pytest tests/ --cov=custom_components/ventilairsec2ha
\`\`\`

## Étapes de Soumission

1. **Préparer le dépôt**
   - Créer une branche `main` stable
   - Tagger version `v1.0.0`
   - Créer Release GitHub

2. **Intégrer HACS** (optionnel mais recommandé)
   - Ajouter `hacs.json`:
   ```json
   {
     "name": "Ventilairsec2HA",
     "homeassistant": "2024.1.0",
     "render_readme": true,
     "content_in_root": false
   }
   ```

3. **Soumettre à la Boutique Officielle**
   - Fork: https://github.com/home-assistant/home-assistant.io
   - Créer PR dans `/source/_integrations/ventilairsec2ha.markdown`
   - Suivre le template officiel

4. **Documentation Officielle**
   ```markdown
   ---
   title: Ventilairsec2
   description: Intégration VMI via ENocean pour Home Assistant
   ha_category:
     - Climate
     - Sensor
   ha_release_summary: Première version stable
   ha_release_date: 2024-01-15
   ha_iot_class: Local Polling
   ha_config_flow: true
   ha_codeowners:
     - @ricolaflo88
   ha_domain: ventilairsec2ha
   ha_homekit: true
   ha_platforms:
     - binary_sensor
     - climate
     - sensor
     - select
   ha_integration_type: integration
   ---
   ```

## Post-Soumission

- Monitorer les retours (reviews peuvent prendre 2-4 semaines)
- Répondre aux questions des reviewers
- Appliquer corrections suggérées
- Une fois approuvé, l'intégration sera listée dans la boutique officielle

## Support ENocean

Vérifier la compatibilité avec:
- Enocean USB 300 / 400
- Enocean modules EEP A5-09-04 (température/humidité)
- Enocean modules EEP A5-04-01 (capteurs de présence)

Utiliser la bibliothèque: `enocean>=0.60.0`
