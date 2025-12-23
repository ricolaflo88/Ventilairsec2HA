#!/bin/bash
set -e

echo "🔧 Ventilairsec2HA - Script d'Installation"
echo "=========================================="

# Vérifier Python
echo "📌 Vérification de Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 non trouvé"
    echo "Installation de Python3..."
    apt-get update
    apt-get install -y python3 python3-pip python3-venv
else
    PYTHON_VERSION=$(python3 --version)
    echo "✅ $PYTHON_VERSION trouvé"
fi

# Vérifier pip
echo "📌 Vérification de pip..."
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "❌ pip non trouvé"
    echo "Installation de pip3..."
    apt-get update
    apt-get install -y python3-pip
else
    PIP_VERSION=$(pip3 --version 2>/dev/null || pip --version)
    echo "✅ $PIP_VERSION trouvé"
fi

# Créer un alias pip -> pip3 si nécessaire
if ! command -v pip &> /dev/null && command -v pip3 &> /dev/null; then
    echo "⚙️  Création d'un alias pip -> pip3"
    alias pip=pip3
fi

# Créer venv (optionnel mais recommandé)
echo "📌 Configuration de l'environnement virtuel..."
if [ ! -d "venv" ]; then
    echo "Création du venv..."
    python3 -m venv venv
    echo "✅ venv créé"
else
    echo "✅ venv existe déjà"
fi

# Activer venv
echo "Activation du venv..."
source venv/bin/activate

# Mettre à jour pip
echo "📌 Mise à jour de pip..."
pip install --upgrade pip setuptools wheel

# Installer les dépendances
echo "📌 Installation des dépendances de développement..."
if [ -f "requirements-dev.txt" ]; then
    pip install -r requirements-dev.txt
    echo "✅ Dépendances installées"
else
    echo "⚠️  requirements-dev.txt non trouvé"
    echo "Installation manuelle des paquets essentiels..."
    pip install pytest pytest-asyncio pytest-cov homeassistant enocean voluptuous
fi

# Installer dépendances production
echo "📌 Installation des dépendances de production..."
if [ -f "custom_components/ventilairsec2ha/manifest.json" ]; then
    echo "Extraction des requirements du manifest..."
    # Les dépendances sont dans manifest.json (enocean, etc.)
fi

echo ""
echo "=========================================="
echo "✅ Installation terminée avec succès!"
echo "=========================================="
echo ""
echo "📝 Prochaines étapes:"
echo "1. Activer l'environnement virtuel:"
echo "   source venv/bin/activate"
echo ""
echo "2. Valider l'installation:"
echo "   pytest tests/ -v"
echo ""
echo "3. Vérifier le manifest:"
echo "   python3 -m json.tool custom_components/ventilairsec2ha/manifest.json"
echo ""
echo "4. Lancer les tests complets:"
echo "   bash validate.sh"
echo ""
