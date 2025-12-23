#!/bin/bash
# Script de test pour Ventilairsec2HA
# Utiliser: bash run_tests.sh

echo "🧪 Lancement des tests Ventilairsec2HA..."
echo ""

# Check Python availability
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ Python n'est pas installé"
    exit 1
fi

echo "✅ Utilisation de: $PYTHON_CMD"
echo ""

# Run tests
$PYTHON_CMD ventilairsec2ha/rootfs/app/test_ha_integration.py

# Capture exit code
EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ Tous les tests sont passés!"
else
    echo "❌ Certains tests ont échoué (code: $EXIT_CODE)"
fi

exit $EXIT_CODE
