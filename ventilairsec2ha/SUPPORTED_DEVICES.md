# 📱 Appareils Supportés - Ventilairsec2HA

## Appareils EnOcean Actuellement Supportés

### 1. 🌬️ VMI Purevent Ventilairsec

**Type** : Variante propriétaire D1-07-9F
**Adresse Exemple** : `0x0421574F`
**Fabricant** : Purevent
**Protocole** : 4 octets manufacturier

#### Informations

La VMI Purevent Ventilairsec est une unité de ventilation mécanique contrôlée (VMC) avec :

- Contrôle de vitesse (5 niveaux : 0, 1, 2, 3, 4)
- Détection de pannes
- Communication par radio EnOcean 868 MHz
- Consommation énergétique réduite

#### Structure du Paquet

```
Octet 0 : Contrôle/Status
  [7:6] : Mode (00=Normal, 01=Panne, 10=Maintenance)
  [5:4] : Vitesse Actuelle (0-3)
  [3:0] : Réservé

Octet 1 : Commande Vitesse
  [7:4] : Vitesse Demandée (0-4)
  [3:0] : Réservé

Octets 2-3 : Données Supplémentaires
  Code erreur, status système
```

#### Plages de Vitesse

| Vitesse     | Valeur | État            |
| ----------- | ------ | --------------- |
| Arrêt       | 0      | Ventilateur off |
| Basse       | 1      | ~40% puissance  |
| Moyenne     | 2      | ~60% puissance  |
| Haute       | 3      | ~80% puissance  |
| Turbo/Boost | 4      | 100% puissance  |

#### Commandes Possibles

```python
# Changer la vitesse
{
    "address": "0x0421574F",
    "command": "speed_control",
    "speed": 2  # 0-4
}

# Demander l'état
{
    "address": "0x0421574F",
    "command": "status_request"
}

# Arrêt d'urgence
{
    "address": "0x0421574F",
    "command": "emergency_stop"
}
```

#### Topics MQTT Publiés

```
homeassistant/ventilairsec2ha/state/0x0421574F
└─ Payload:
   {
     "address": "0x0421574F",
     "name": "VMI Purevent",
     "type": "d1_07_9f_01",
     "status": "running",
     "current_speed": 2,
     "target_speed": 2,
     "error_code": 0,
     "operating_hours": 12847,
     "temperature": 24.5,
     "rssi": -65,
     "timestamp": "2024-01-15T14:30:00Z"
   }
```

---

### 2. 📊 Capteur CO₂

**Type** : RfP / A5-09-04 (4BS)
**Adresse Exemple** : `0x81003227`
**Fabricant** : Enocean Generics (ELTAKO, Therkon, etc.)
**Protocole** : 4 octets (CMS/Variateur)

#### Spécifications

- **Plage CO₂** : 0-2000 ppm
- **Précision** : ±50 ppm @ 20°C
- **Type Capteur** : Capteur infrarouge (NDIR) ou chimique
- **Fréquence de Transmission** : Déclenche à changement > 50 ppm

#### Structure du Paquet A5-09-04

```
Octets 0-3 : Données 4BS
  [23:16] : Données CO₂ brutes (0-255 = 0-2000 ppm linéaire)
  [15:8]  : Données Température (ELTAKO) ou réservé
  [7:0]   : Flags/Status
```

#### Calcul CO₂

```python
# Depuis les données brutes (octets ENOCEAN)
def calculate_co2(raw_value):
    """Convertit valeur brute (0-255) en ppm (0-2000)"""
    co2_ppm = (raw_value / 255.0) * 2000
    return co2_ppm

# Valeurs typiques
100 ppm = 12.75 (brut)  # Air extérieur très pur
400 ppm = 51.0          # Air extérieur normal
800 ppm = 102.0         # Seuil alerte confort
1000 ppm = 127.5        # Seuil recommandé
1200 ppm = 152.9        # Mauvaise qualité
```

#### Topics MQTT Publiés

```
homeassistant/ventilairsec2ha/state/0x81003227
└─ Payload:
   {
     "address": "0x81003227",
     "name": "Capteur CO₂ Salon",
     "type": "a5_09_04",
     "co2": 550,
     "co2_ppm": 550,
     "quality": "acceptable",
     "battery_low": false,
     "rssi": -72,
     "timestamp": "2024-01-15T14:30:15Z"
   }
```

---

### 3. 🌡️ Capteur Température / Humidité

**Type** : A5-04-01 (4BS)
**Adresse Exemple** : `0x810054F5`
**Fabricant** : Generic EnOcean
**Protocole** : 4 octets (4BS - température et humidité)

#### Spécifications

- **Plage Température** : -20°C à +60°C
- **Résolution Température** : 0.1°C
- **Plage Humidité** : 0 à 100% RH
- **Résolution Humidité** : 1% RH
- **Fréquence de Transmission** : ~10 minutes ou changement significatif

#### Structure du Paquet A5-04-01

```
Octets 0-3 : Données 4BS
  [23:16] : Humidité (0-200 = 0-100% RH)
  [15:8]  : Température (0-200 ≈ -20°C à +60°C)
  [7]     : Température négative flag
  [6]     : Batterie basse
  [5:0]   : Status bits
```

#### Calcul Température/Humidité

```python
def calculate_temperature(raw_value, sign_bit):
    """Convertit valeur brute en °C"""
    temp_raw = (raw_value / 200.0) * 80  # Plage: -20 à +60°C
    if sign_bit:
        temp_raw = -temp_raw
    return round(temp_raw, 1)

def calculate_humidity(raw_value):
    """Convertit valeur brute en % RH"""
    humidity = (raw_value / 200.0) * 100
    return round(humidity, 1)

# Valeurs typiques
0°C = 128 (brut)
20°C = 160 (brut)  # Température confortable
25°C = 170 (brut)
40°C = 192 (brut)

0% = 0 (brut)
50% = 100 (brut)
100% = 200 (brut)
```

#### Topics MQTT Publiés

```
homeassistant/ventilairsec2ha/state/0x810054F5
└─ Payload:
   {
     "address": "0x810054F5",
     "name": "Capteur Climat Salon",
     "type": "a5_04_01",
     "temperature": 22.5,
     "humidity": 45,
     "temperature_unit": "°C",
     "humidity_unit": "%",
     "battery_low": false,
     "rssi": -68,
     "timestamp": "2024-01-15T14:30:30Z"
   }
```

---

### 4. 🎮 Télécommande Assistant (Variante D1-07-9F)

**Type** : Variante D1-07-9F Telecommande
**Adresse Exemple** : `0x0422407D`
**Protocole** : Compatible VMI Purevent

#### Boutons Disponibles

| Bouton       | Code | Action             |
| ------------ | ---- | ------------------ |
| On/Off       | 0x01 | Allume/Éteint      |
| Vitesse +    | 0x02 | Augmente vitesse   |
| Vitesse -    | 0x03 | Réduit vitesse     |
| Boost 30 min | 0x04 | Vitesse max 30 min |
| Auto         | 0x05 | Mode auto (CO₂)    |

#### Topics MQTT Reçus

```
homeassistant/ventilairsec2ha/state/0x0422407D
└─ Payload:
   {
     "address": "0x0422407D",
     "name": "Télécommande Assistant",
     "type": "d1_07_9f_telecommand",
     "last_button": "speed_up",
     "button_code": 2,
     "rssi": -55,
     "timestamp": "2024-01-15T14:30:45Z"
   }
```

---

## Appareils Futurs Supportés

### 🔄 En Développement (v0.2)

- **A5-07-01** : Variateur de lumière
- **A5-08-01** : Capteur de luminosité
- **A5-13-01** : Capteur pression atmosphérique
- **D2-01-0C** : Détecteur de fuite d'eau
- **F6-02-01** : Interrupteur sans fil 4 canaux

### 🎯 Prévus (v0.3+)

- **A5-06-01** : Luminance / rayonnement
- **D1-06-03** : Variateur standard
- **D5-00-01** : Capteurs numériques simples

---

## Ajout de Nouveaux Appareils

Si vous avez un appareil EnOcean non supporté, veuillez :

1. **Créer une Issue** : https://github.com/ricolaflo88/Ventilairsec2HA/issues

   - Incluez le RORG et les données du paquet
   - Décrivez les données envoyées

2. **Ou contribuer directement** :
   - Fork le repository
   - Ajoutez le support dans `enocean_constants.py`
   - Créez des tests unitaires
   - Soumettez une Pull Request

### Format pour Rapport

```yaml
Appareil: [Nom commercial]
Fabricant: [Brand]
RORG: 0x??
Adresse Exemple: 0x????????
Données Brutes: [Format: 0xABCDEFGH]
Interprétation: [Que signifient les octets]
Documentation: [Lien datasheet si disponible]
```

---

## Structure de Configuration

```python
# Dans enocean_constants.py

ENOCEAN_DEVICES = {
    0x0421574F: {
        "name": "VMI Purevent",
        "type": "d1_07_9f_01",
        "rorg": 0xD1,
        "func": 0x07,
        "type_id": 0x9F,
        "variant": 0x01,
        "fields": {
            "status": {"offset": 0, "length": 1},
            "speed": {"offset": 1, "length": 1},
        }
    }
}
```

---

## Debugging des Appareils

### Voir les Paquets Bruts

```bash
# Via les logs
docker logs -f addon_ventilairsec2ha | grep "0xYOURADDRESS"

# Résultat attendu:
# 📦 Received packet from 0xYOURADDRESS: [D1][07][9F][01][...]
```

### Tester une Adresse

```bash
# Envoyer une commande de test
curl -X POST http://homeassistant.local:8080/api/command \
  -H "Content-Type: application/json" \
  -d '{
    "address": "0xADDRESS",
    "command": "status_request"
  }'
```

---

## Resources

- 📖 [Specification EnOcean (EEP)](https://www.enocean-alliance.org/eep/)
- 🔧 [Documentation Technique](DOCS.md)
- 🆘 [Support](https://github.com/ricolaflo88/Ventilairsec2HA/issues)

---

**Version** : 0.1.0
**Mise à jour** : 2024
**Auteur** : Ventilairsec2HA Project
