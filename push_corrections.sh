#!/bin/bash
# Script pour pousser les corrections lint

echo "=========================================="
echo "📤 Poussez les Corrections Lint"
echo "=========================================="

cd /workspaces/Ventilairsec2HA

# Afficher le statut git
echo ""
echo "📋 Fichiers modifiés :"
git status --short

# Ajouter les changements
echo ""
echo "➕ Ajout des changements..."
git add ventilairsec2ha/config.yaml

# Afficher les changements
echo ""
echo "📝 Différences :"
git diff --cached ventilairsec2ha/config.yaml

# Commit
echo ""
echo "💾 Création du commit..."
git commit -m "fix: correct config.yaml schema validation for Home Assistant lint

- Suppression des guillemets dans les définitions schema (non-supportés par lint)
- Ajout de tous les paramètres d'options avec valeurs par défaut
- Validation de plage pour les ports (1024-65535)
- Réorganisation de l'ordre des sections pour convention HA
- Tous les champs schema marqués comme optionnels

Ceci corrige les erreurs détectées par frenck/action-addon-linter"

# Afficher le commit créé
echo ""
echo "✅ Commit créé :"
git log -1 --oneline

# Ne pas pousser automatiquement (laisser l'utilisateur contrôler)
echo ""
echo "=========================================="
echo "✅ Changements prêts"
echo "=========================================="
echo ""
echo "📤 Pour pousser les changements :"
echo "   git push origin main"
echo ""
echo "🔍 Le lint workflow se lancera automatiquement"
echo "   et les images Docker seront reconstruites"
echo ""
