## 🚀 Quick Start Publication v1.0.0

Guide rapide pour publier Ventilairsec2HA sur le store Home Assistant.

---

## ✅ Avant de Commencer

Vérifier que tout est prêt:

```bash
bash verify_release.sh
```

Doit afficher:

```
✅ Tous les fichiers sont présents!
🎉 Plugin prêt pour la publication!
```

---

## 📦 Étape 1: Créer une Release GitHub

```bash
# Clone ou naviguez dans le repo
cd Ventilairsec2HA

# Vérifier que tout est commité
git status

# Créer le tag v1.0.0
git tag -a v1.0.0 -m "Version 1.0.0 - MQTT Discovery et entités HA natives

- ✨ MQTT Discovery pour auto-intégration HA
- ✨ Entités HA natives (Climate + Sensors)
- 🔧 Retry logic avec exponential backoff
- ✅ 40+ tests unitaires
- 📚 Documentation complète
- 🏪 Prêt pour le store HA"

# Pousser le tag
git push origin v1.0.0

# Vérifier sur GitHub
# https://github.com/ricolaflo88/Ventilairsec2HA/releases
```

---

## 🏪 Étape 2: Soumettre au Store Community

### Option A: Home Assistant Community Addons (Plus rapide)

1. Fork: https://github.com/hassio-addons/community
2. Ajouter votre addon
3. Créer une PR

**Template PR:**

```markdown
## Nouveau Addon: Ventilairsec2HA

### Description

Intégration complète pour VMI Purevent Ventilairsec avec MQTT Discovery.

### Features

- ✅ MQTT Discovery
- ✅ Entités HA natives
- ✅ Retry automatique
- ✅ 40+ tests

### Repository

https://github.com/ricolaflo88/Ventilairsec2HA
```

### Option B: Store Officiel Home Assistant (Plus strict)

1. Fork: https://github.com/home-assistant/addons
2. Ajouter votre addon dans le dossier approprié
3. Créer une PR avec description détaillée

**Critères:**

- [x] Version 1.0.0+
- [x] Tests complets
- [x] Documentation
- [x] CI/CD
- [x] License

---

## ✅ Étape 3: Tester en Local (Optionnel)

### Pré-requis

- Home Assistant installé
- SSH activé
- Docker disponible

### Installation de Test

```bash
# SSH dans HA
ssh root@homeassistant.local

# Clone le repo
cd /addons
git clone https://github.com/ricolaflo88/Ventilairsec2HA.git

# Recharger les addons
# Paramètres > Modules complémentaires > ⋮ > Recharger
```

### Vérifier le Fonctionnement

1. Installer l'addon
2. Configurer la connexion EnOcean
3. Vérifier MQTT Discovery
4. Tester commandes VMI
5. Afficher les sensors

---

## 📋 Checklist Publication

- [ ] `git tag -a v1.0.0` créé
- [ ] GitHub Release créée
- [ ] PR soumise au store community
- [ ] Tests validés
- [ ] MQTT Discovery fonctionne
- [ ] Entités HA apparaissent
- [ ] Commandes VMI répondent

---

## 🎯 Après Publication

1. **Communiquer**

   - Post sur forum HA
   - Tweet/Social media
   - GitHub Discussions

2. **Support**

   - Répondre aux issues
   - Fixer les bugs rapidement
   - Maintenir la documentation

3. **Améliorations v1.1.0**
   - Dashboard Lovelace préconfiguré
   - Appairage semi-automatique
   - Plus de capteurs supportés

---

## 📞 Support en Cas de Problème

### MQTT Discovery ne marche pas

- Vérifier que Mosquitto est installé
- Vérifier les logs: `docker logs addon_ventilairsec2ha`
- Lire [MQTT_TOPICS.md](ventilairsec2ha/MQTT_TOPICS.md)

### Entités HA n'apparaissent pas

- Vérifier la configuration MQTT dans HA
- Redémarrer HA
- Vérifier l'addon est bien démarré

### Issues GitHub

- Créer une issue détaillée
- Inclure les logs complets
- Spécifier la version HA et du matériel

---

## 🎉 Félicitations!

Ventilairsec2HA v1.0.0 est maintenant prêt pour le store officiel Home Assistant.

**Merci d'avoir suivi ce guide! 🙏**
