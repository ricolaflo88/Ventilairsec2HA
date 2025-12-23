#!/bin/bash

echo "📦 Installation de pip et dépendances Python..."

# Mise à jour des paquets système
echo "Mise à jour du système..."
apt-get update

# Installation de Python3 et pip
echo "Installation de Python3 et pip..."
apt-get install -y python3 python3-pip python3-venv python3-dev

# Vérification
echo ""
echo "Versions installées:"
python3 --version
pip3 --version

# Créer un alias si pip n'existe pas
if ! command -v pip &> /dev/null; then
    echo ""
    echo "Création d'un alias: pip -> pip3"
    echo "alias pip=pip3" >> ~/.bashrc
    echo "alias pip=pip3" >> ~/.zshrc 2>/dev/null || true
    source ~/.bashrc 2>/dev/null || true
    source ~/.zshrc 2>/dev/null || true
fi

echo ""
echo "✅ Installation terminée!"
echo "Utilisez: pip3 install -r requirements-dev.txt"
