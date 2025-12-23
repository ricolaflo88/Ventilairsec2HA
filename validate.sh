#!/bin/bash
set -e

echo "🔍 Ventilairsec2HA - Validation Complète"
echo "========================================"

# Vérifier que l'environnement est activé
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Environnement virtuel non activé"
    echo "Activation automatique..."
    if [ -d "venv" ]; then
        source venv/bin/activate
    else
        echo "❌ venv non trouvé. Lancer: bash setup.sh"
        exit 1
    fi
fi

# Vérifier les outils disponibles
echo "📌 Vérification des dépendances..."
python3 -c "import pytest; print('✅ pytest installé')" || {
    echo "❌ pytest non installé"
    pip install pytest pytest-asyncio pytest-cov
}

python3 -c "import homeassistant; print('✅ homeassistant installé')" || {
    echo "❌ homeassistant non installé"
    pip install homeassistant
}

# Valider manifest.json
echo ""
echo "📌 Validation du manifest.json..."
python3 -m json.tool custom_components/ventilairsec2ha/manifest.json > /dev/null && \
echo "✅ manifest.json valide" || \
echo "❌ manifest.json invalide"

# Vérifier imports
echo ""
echo "📌 Vérification des imports..."
python3 -c "from custom_components.ventilairsec2ha.config_flow import VentilairsecConfigFlow" && \
echo "✅ config_flow importable" || \
echo "❌ config_flow non importable"

python3 -c "from custom_components.ventilairsec2ha.const import DOMAIN" && \
echo "✅ const importable" || \
echo "❌ const non importable"

# Lancer les tests
echo ""
echo "📌 Exécution des tests..."
pytest tests/test_manifest.py -v && echo "✅ Tests manifest passés" || echo "❌ Tests manifest échoués"
pytest tests/test_config_flow.py -v && echo "✅ Tests config_flow passés" || echo "⚠️  Tests config_flow (attendus si setup incomplet)"

# Coberture
echo ""
echo "📌 Rapport de couverture..."
pytest tests/ --cov=custom_components/ventilairsec2ha --cov-report=term-missing --cov-report=html

echo ""
echo "========================================"
echo "✅ Validation terminée!"
echo "========================================"
echo ""
echo "📊 Rapports générés:"
echo "- htmlcov/index.html (couverture de code)"
echo ""
