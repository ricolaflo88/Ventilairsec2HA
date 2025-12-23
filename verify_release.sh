#!/bin/bash
# Script de vérification avant publication v1.0.0

echo "🔍 Vérification Ventilairsec2HA v1.0.0 pour Store HA"
echo ""

ERRORS=0
WARNINGS=0

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✅${NC} $1"
    else
        echo -e "${RED}❌${NC} $1 (MANQUANT)"
        ((ERRORS++))
    fi
}

check_version() {
    file=$1
    version=$2
    if grep -q "\"version\": \"$version\"" "$file" || grep -q "version: \"$version\"" "$file"; then
        echo -e "${GREEN}✅${NC} $file version $version"
    else
        echo -e "${RED}❌${NC} $file version non trouvée"
        ((ERRORS++))
    fi
}

echo "📋 Fichiers Critiques"
echo "===================="
check_file "ventilairsec2ha/manifest.json"
check_file "ventilairsec2ha/config.yaml"
check_file "ventilairsec2ha/Dockerfile"
check_file "ventilairsec2ha/README.md"
check_file ".github/workflows/build.yml"
echo ""

echo "🔧 Fichiers Modifiés"
echo "===================="
check_file "ventilairsec2ha/rootfs/app/ha_entities.py"
check_file "ventilairsec2ha/rootfs/app/home_assistant_integration.py"
check_file "ventilairsec2ha/rootfs/app/enocean_communicator.py"
check_file "ventilairsec2ha/rootfs/app/test_ha_integration.py"
echo ""

echo "📚 Documentation"
echo "==============="
check_file "ventilairsec2ha/MQTT_TOPICS.md"
check_file "ventilairsec2ha/CHANGELOG.md"
check_file "STORE_PUBLICATION_GUIDE.md"
check_file "TESTING.md"
check_file "run_tests.sh"
check_file "RELEASE_NOTES_v1.0.0.md"
echo ""

echo "🏷️  Versions"
echo "==========="
check_version "ventilairsec2ha/manifest.json" "1.0.0"
check_version "ventilairsec2ha/config.yaml" "1.0.0"
echo ""

echo "📊 Résumé"
echo "========"

if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ Tous les fichiers sont présents!${NC}"
    echo ""
    echo "🎉 Plugin prêt pour la publication!"
    echo ""
    echo "Prochaines étapes:"
    echo "1. Créer une GitHub Release: git tag -a v1.0.0 -m 'v1.0.0'"
    echo "2. Soumettre au store community"
    echo "3. Tester en environnement réel"
    exit 0
else
    echo -e "${RED}❌ $ERRORS fichier(s) manquant(s)${NC}"
    exit 1
fi
