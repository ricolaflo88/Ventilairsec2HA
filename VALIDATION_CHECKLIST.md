# Checklist Validation - Home Assistant App Store

## ✅ Structure du Projet

- [ ] Dossier `custom_components/ventilairsec2ha/` existe
- [ ] `manifest.json` présent et valide
- [ ] `__init__.py` avec `async_setup_entry`
- [ ] `config_flow.py` pour configuration UI
- [ ] `strings.json` pour traductions
- [ ] README.md avec instructions
- [ ] LICENSE présent (MIT, Apache 2.0, etc.)

## ✅ Fonctionnalités ENocean

- [ ] Communication bidirectionnelle ENocean fonctionnelle
- [ ] Découverte automatique des capteurs
- [ ] Support des protocoles ENocean standards
- [ ] Gestion des erreurs de connexion
- [ ] Logs détaillés pour débogage

## ✅ Intégration Home Assistant

- [ ] Entités VMI (ventilation) exposées
- [ ] Entités capteurs (température, humidité, CO2, etc.)
- [ ] États persistants dans `homeassistant.states`
- [ ] Services personnalisés documentés
- [ ] Automation-friendly

## ✅ Stockage & Données

- [ ] Historique des données sauvegardé
- [ ] Compatible avec `history` Home Assistant
- [ ] Compatible avec `influxdb` (optionnel)
- [ ] Export de graphiques possibles
- [ ] API REST pour accès aux données

## ✅ Code Quality

- [ ] Pas d'erreurs de linting (`pylint`, `flake8`)
- [ ] Tests unitaires présents (`pytest`)
- [ ] Docstrings complètes
- [ ] Type hints Python 3.10+
- [ ] Pas de dépendances bloatées

## ✅ Documentation

- [ ] README.md en FR et EN
- [ ] Instructions installation
- [ ] Configuration step-by-step
- [ ] Troubleshooting guide
- [ ] CHANGELOG.md

## ✅ Boutique Home Assistant

- [ ] Logo 256x256 PNG présent
- [ ] `hacs.json` configuré
- [ ] Repository public GitHub
- [ ] Versioning sémantique (v1.0.0)
- [ ] Releases GitHub taggées
- [ ] LICENSE valide

---

## Commandes de Validation

\`\`\`bash

# Valider la structure

python -m homeassistant -c ./custom_components/ventilairsec2ha --script check_config

# Lancer les tests

pytest tests/

# Vérifier le linting

pylint custom_components/ventilairsec2ha
flake8 custom_components/ventilairsec2ha
\`\`\`
