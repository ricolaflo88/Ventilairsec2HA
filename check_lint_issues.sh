#!/bin/bash
# Script pour vérifier les erreurs lint Home Assistant addon

echo "=========================================="
echo "🔍 Vérification Lint Home Assistant Addon"
echo "=========================================="

addon_path="/workspaces/Ventilairsec2HA/ventilairsec2ha"

# Vérifier la structure basique
echo ""
echo "📋 Structure Addon"
echo "=========================================="

files=(
    "config.yaml"
    "build.yaml"
    "Dockerfile"
    "README.md"
    "apparmor.txt"
)

for file in "${files[@]}"; do
    if [ -f "$addon_path/$file" ]; then
        echo "✅ $file présent"
    else
        echo "❌ $file MANQUANT"
    fi
done

# Vérifier config.yaml
echo ""
echo "🔧 Vérification config.yaml"
echo "=========================================="

if grep -q "^name:" "$addon_path/config.yaml"; then
    echo "✅ Champ 'name' présent"
else
    echo "❌ Champ 'name' MANQUANT"
fi

if grep -q "^slug:" "$addon_path/config.yaml"; then
    echo "✅ Champ 'slug' présent"
else
    echo "❌ Champ 'slug' MANQUANT"
fi

if grep -q "^version:" "$addon_path/config.yaml"; then
    echo "✅ Champ 'version' présent"
else
    echo "❌ Champ 'version' MANQUANT"
fi

if grep -q "^description:" "$addon_path/config.yaml"; then
    echo "✅ Champ 'description' présent"
else
    echo "❌ Champ 'description' MANQUANT"
fi

if grep -q "^arch:" "$addon_path/config.yaml"; then
    echo "✅ Champ 'arch' présent"
else
    echo "❌ Champ 'arch' MANQUANT"
fi

# Vérifier schema
if grep -q "^schema:" "$addon_path/config.yaml"; then
    echo "✅ Champ 'schema' présent"
else
    echo "⚠️  Champ 'schema' MANQUANT (important pour UI)"
fi

# Vérifier Dockerfile
echo ""
echo "🐳 Vérification Dockerfile"
echo "=========================================="

if grep -q "^FROM" "$addon_path/Dockerfile"; then
    echo "✅ Instruction FROM présente"
else
    echo "❌ Instruction FROM MANQUANTE"
fi

if grep -q "^WORKDIR" "$addon_path/Dockerfile"; then
    echo "✅ Instruction WORKDIR présente"
else
    echo "⚠️  Instruction WORKDIR absente"
fi

# Vérifier que les instructions importantes existent
if grep -q "RUN.*apk add" "$addon_path/Dockerfile"; then
    echo "✅ Installation paquets présente"
else
    echo "❌ Installation paquets MANQUANTE"
fi

if grep -q "COPY.*requirements" "$addon_path/Dockerfile"; then
    echo "✅ Copie requirements présente"
else
    echo "⚠️  Copie requirements absente"
fi

if grep -q "COPY.*rootfs" "$addon_path/Dockerfile"; then
    echo "✅ Copie rootfs présente"
else
    echo "❌ Copie rootfs MANQUANTE"
fi

# Vérifier build.yaml
echo ""
echo "🏗️  Vérification build.yaml"
echo "=========================================="

if grep -q "^build_from:" "$addon_path/build.yaml"; then
    echo "✅ Champ 'build_from' présent"
else
    echo "❌ Champ 'build_from' MANQUANT"
fi

# Vérifier README
echo ""
echo "📖 Vérification README.md"
echo "=========================================="

if [ -f "$addon_path/README.md" ]; then
    lines=$(wc -l < "$addon_path/README.md")
    if [ "$lines" -gt 50 ]; then
        echo "✅ README suffisamment détaillé ($lines lignes)"
    else
        echo "⚠️  README court ($lines lignes)"
    fi
else
    echo "❌ README.md MANQUANT"
fi

# Vérifier CommonIssues
echo ""
echo "🆘 Erreurs Courantes Lint"
echo "=========================================="

# Vérifier slugs invalides
if grep -q "slug:" "$addon_path/config.yaml"; then
    slug=$(grep "slug:" "$addon_path/config.yaml" | awk '{print $2}' | tr -d '"')
    if [[ $slug =~ ^[a-z0-9_]+$ ]]; then
        echo "✅ Slug valide: $slug"
    else
        echo "❌ Slug invalide: $slug (doit être lowercase + underscores)"
    fi
fi

# Vérifier les ports
if grep -q "ports:" "$addon_path/config.yaml"; then
    echo "✅ Ports configurés"
else
    echo "⚠️  Pas de ports configurés"
fi

# Vérifier privileged
if grep -q "privileged:" "$addon_path/config.yaml"; then
    echo "✅ Privileged configuré"
else
    echo "⚠️  Pas de privileged configuré"
fi

echo ""
echo "=========================================="
echo "✅ Vérification Terminée"
echo "=========================================="
