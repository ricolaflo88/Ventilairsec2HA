.PHONY: help install setup validate test lint clean

help:
	@echo "Ventilairsec2HA - Commandes disponibles:"
	@echo ""
	@echo "  make install      - Installer les dépendances système + Python"
	@echo "  make setup        - Créer venv et installer dépendances"
	@echo "  make validate     - Valider manifest et config_flow"
	@echo "  make test         - Lancer les tests unitaires"
	@echo "  make lint         - Vérifier la qualité du code"
	@echo "  make clean        - Nettoyer les fichiers temporaires"
	@echo ""

install:
	@echo "📦 Installation des dépendances système..."
	apt-get update
	apt-get install -y python3 python3-pip python3-venv python3-dev
	python3 --version
	pip3 --version

setup:
	@echo "🔧 Configuration de l'environnement..."
	python3 -m venv venv
	. venv/bin/activate && pip install --upgrade pip setuptools wheel
	. venv/bin/activate && pip install -r requirements-dev.txt
	@echo "✅ Configuration terminée"
	@echo "Activez l'environnement: source venv/bin/activate"

validate:
	@echo "🔍 Validation du manifest et config_flow..."
	python3 -m json.tool custom_components/ventilairsec2ha/manifest.json > /dev/null
	python3 -c "from custom_components.ventilairsec2ha.config_flow import VentilairsecConfigFlow; print('✅ Config flow valide')"
	@echo "✅ Validation réussie"

test:
	@echo "🧪 Lancement des tests..."
	pytest tests/test_manifest.py -v
	pytest tests/test_config_flow.py -v
	@echo "✅ Tests terminés"

coverage:
	@echo "📊 Rapport de couverture..."
	pytest tests/ --cov=custom_components/ventilairsec2ha --cov-report=html --cov-report=term-missing
	@echo "Voir: htmlcov/index.html"

lint:
	@echo "🔍 Vérification de la qualité du code..."
	pylint custom_components/ventilairsec2ha --disable=all --enable=E,F || true
	flake8 custom_components/ventilairsec2ha --max-line-length=100 || true

clean:
	@echo "🧹 Nettoyage des fichiers temporaires..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .coverage htmlcov .mypy_cache
	@echo "✅ Nettoyage terminé"
