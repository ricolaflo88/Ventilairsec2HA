# 🔌 Guide de Configuration - GPIO vs USB

## Deux Options de Connexion pour l'EnOcean

Votre module EnOcean peut être connecté de deux façons :

### 1️⃣ GPIO UART (Raspberry Pi)

**Avantages:**
- ✅ Pas de port USB occupé
- ✅ Connexion directe aux broches GPIO
- ✅ Stable et fiable

**Broches GPIO Standard:**
```
┌─────────────────────────────────────────┐
│  Raspberry Pi GPIO Header               │
├─────────────────────────────────────────┤
│ GND       → GPIO GND (pin 6, 9, 14, 20, 25, 30, 34, 39)
│ VCC (+3V) → GPIO 3V3 (pin 1, 17)
│ RXD       → GPIO 15 (pin 10) - UART0_RXD
│ TXD       → GPIO 14 (pin 8)  - UART0_TXD
└─────────────────────────────────────────┘

Numérotation des pins (vue du dessus):
┌─────────────────────────────┐
│ 1  2  3  4  5  6  7  8  9 10│
│11 12 13 14 15 16 17 18 19 20│
│21 22 23 24 25 26 27 28 29 30│
│31 32 33 34 35 36 37 38 39 40│
└─────────────────────────────┘

RXD = Pin 10
TXD = Pin 8
GND = Pin 6, 9, 14, 20, 25, 30, 34, 39
3V3 = Pin 1, 17
```

**Ports disponibles:**
- `/dev/ttyAMA0` - Primary UART (GPIO 14/15)
- `/dev/serial0` - Alias pour ttyAMA0
- `/dev/ttyS0` - Mini UART (GPIO 32/33, Pi 5 uniquement)

**Vérifier la connexion:**
```bash
ssh root@homeassistant.local

# Vérifier que le port existe
ls -la /dev/ttyAMA0
ls -la /dev/serial0

# Test basique
strace -e open,openat -e write ls /dev/ttyAMA0
```

**Configuration Home Assistant:**

```json
{
  "connection_mode": "gpio",
  "serial_port": "/dev/ttyAMA0",
  "log_level": "info",
  "enable_mqtt": true,
  "mqtt_broker": "mosquitto"
}
```

Ou mode auto-détection:
```json
{
  "connection_mode": "auto",
  "serial_port": "auto",
  "log_level": "info"
}
```

---

### 2️⃣ USB (Adaptateur USB-UART)

**Avantages:**
- ✅ Plug & play facile
- ✅ Portable et flexible
- ✅ Multiple sticks possibles

**Ports disponibles:**
- `/dev/ttyUSB0` - Premier stick USB
- `/dev/ttyUSB1` - Deuxième stick USB
- `/dev/ttyACM0` - Adaptateur USB-ACM

**Vérifier la connexion:**
```bash
ssh root@homeassistant.local

# Vérifier les ports USB
ls -la /dev/ttyUSB*
ls -la /dev/ttyACM*

# Identifier le stick EnOcean
dmesg | grep -i enocean
```

**Configuration Home Assistant:**

```json
{
  "connection_mode": "usb",
  "serial_port": "/dev/ttyUSB0",
  "log_level": "info",
  "enable_mqtt": true,
  "mqtt_broker": "mosquitto"
}
```

---

## ⚙️ Mode Auto-Détection (Recommandé)

Le mode `auto` détecte automatiquement :

```json
{
  "connection_mode": "auto",
  "serial_port": "auto",
  "log_level": "info"
}
```

**Priorité de détection:**
1. GPIO UART (`/dev/ttyAMA0`, `/dev/serial0`, `/dev/ttyS0`)
2. USB (`/dev/ttyUSB*`, `/dev/ttyACM*`)
3. Défaut: `/dev/ttyUSB0`

---

## 🔧 Troubleshooting

### Port non détecté

```bash
# SSH dans Home Assistant
ssh root@homeassistant.local

# Vérifier les ports disponibles
ls -la /dev/tty*

# Donner les permissions (si nécessaire)
chmod 666 /dev/ttyAMA0
chmod 666 /dev/ttyUSB0
```

### UART GPIO désactivée (Raspberry Pi)

Si `/dev/ttyAMA0` n'existe pas, vous devez activer UART:

**Via SSH:**
```bash
# Éditer la config
sudo nano /boot/firmware/config.txt

# Ajouter ou modifier:
[all]
dtoverlay=uart0
enable_uart=1

# Sauvegarder (Ctrl+X, Y, Enter)

# Redémarrer
sudo reboot
```

**Via Home Assistant UI:**
```
Paramètres > Système > Redémarrage
```

### Teste la clé EnOcean

```bash
# Avec minicom
minicom -b 57600 -D /dev/ttyAMA0

# Ou screen
screen /dev/ttyAMA0 57600

# Ou avec python
python3 << 'EOF'
import serial
s = serial.Serial('/dev/ttyAMA0', 57600, timeout=1)
data = s.read(100)
print(f"Reçu: {data.hex()}")
s.close()
EOF
```

### Permission Denied

```bash
# Donner permissions permanentes (via udev rules)
sudo nano /etc/udev/rules.d/50-ttyAMA0.rules

# Ajouter:
KERNEL=="ttyAMA0", GROUP="dialout", MODE="0666"

# Recharger
sudo udevadm control --reload-rules
sudo udevadm trigger
```

---

## 📋 Checklist Installation GPIO

- [ ] Broches GPIO correctement raccordées
- [ ] UART activé sur Raspberry Pi
- [ ] Port `/dev/ttyAMA0` ou `/dev/serial0` accessible
- [ ] Configuration mode = "gpio" ou "auto"
- [ ] Addon redémarré
- [ ] Logs montrent "GPIO UART" ou "Connection type: gpio"
- [ ] Paquets reçus dans WebUI

---

## 🔌 Brochage Détaillé (Exemple)

### Module EnOcean → Raspberry Pi GPIO

```
Module EnOcean:
  Pin 1: VCC (+3V3)   → Raspberry Pi Pin 1 ou 17 (3V3)
  Pin 2: GND          → Raspberry Pi Pin 6, 9, 14, 20, 25, 30, 34, 39 (GND)
  Pin 3: RXD (entrée) → Raspberry Pi Pin 10 (GPIO 15, UART0_RXD)
  Pin 4: TXD (sortie) → Raspberry Pi Pin 8 (GPIO 14, UART0_TXD)

Alternative (GPIO 16/17 si reconfiguration):
  RXD → GPIO 17
  TXD → GPIO 27
```

### Câblage Photo Virtuelle

```
       VCC ────────── 3V3 (Pin 1)
       
Stick  RXD ────────── GPIO 15 (Pin 10)
Enocean
       TXD ────────── GPIO 14 (Pin 8)
       
       GND ────────── GND (Pin 6, 9, 14, 20, 25, 30, 34, 39)
```

---

## 📊 Comparaison GPIO vs USB

| Critère | GPIO UART | USB |
|---------|-----------|-----|
| Installation | Câblage GPIO | Plug & Play |
| Ports USB libres | ✅ Oui | ❌ Non |
| Stabilité | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Configuration | Nécessite activation UART | Automatique |
| Portabilité | Fixe (GPIO) | Mobile |
| Coût adaptateur | Bas | Moyen |
| Nombre de sticks | 1 | Plusieurs |

---

## ✅ Vérifier la Connexion

### Logs Addon

Activer mode debug:
```json
{
  "log_level": "debug"
}
```

Vérifier les logs:
```bash
docker logs -f addon_ventilairsec2ha

# Chercher:
# ✅ "GPIO UART opened" ou "USB" selon la connexion
# ✅ "Controller Base ID"
# ✅ "Received packet from VMI"
```

### WebUI

- Ouvrir: `http://homeassistant.local:8080`
- Vérifier:
  - Status: Connected
  - Devices: VMI + capteurs détectés
  - Logs: Paquets reçus

---

## 🚀 Configuration Finale

### GPIO (Recommandé pour Raspberry Pi)

```json
{
  "connection_mode": "gpio",
  "serial_port": "/dev/ttyAMA0",
  "log_level": "info",
  "enable_mqtt": true,
  "mqtt_broker": "mosquitto",
  "mqtt_port": 1883
}
```

### USB

```json
{
  "connection_mode": "usb",
  "serial_port": "/dev/ttyUSB0",
  "log_level": "info",
  "enable_mqtt": true,
  "mqtt_broker": "mosquitto",
  "mqtt_port": 1883
}
```

### Auto (Mieux pour flexibilité)

```json
{
  "connection_mode": "auto",
  "serial_port": "auto",
  "log_level": "info",
  "enable_mqtt": true,
  "mqtt_broker": "mosquitto",
  "mqtt_port": 1883
}
```

---

**C'est prêt! Votre module EnOcean est maintenant configuré ! 🎉**
