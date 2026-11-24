# Shadow Games — Legitimate Edition (CardputerZero)

A kiosk-style launcher for the M5Stack **CardputerZero** (Raspberry Pi
CM0 / BCM2710A1, real Linux — not the ESP32-S3 Cardputer ADV). Menu
layout follows the Uagain Shadow screenshot. Every module is
**receive/read-only**:

| Menu item | What it does | What's deliberately NOT here |
|---|---|---|
| RFID / NFC | Reads tag UID/type via an external PN532 or ACR122U reader (nfcpy) | Clone, write, emulate |
| Sub-GHz | RTL-SDR spectrum scan across 315/433/868/915 MHz + "ghost hunting" RF-anomaly gauge | Capture-and-replay, transmit |
| Scanner | Passive Wi-Fi (`nmcli`) / Bluetooth inventory | Deauth, jamming, injection |
| Tools | Calculator, notes, system info (replaces "Payloads") | BadUSB / keystroke-injection scripts |
| Utility | Wi-Fi settings, reboot/shutdown | — |
| Terminal | Real `xterm` shell — it's Linux | — |
| Files | SD card browser | — |

## Why this isn't a ready `.img`

I can't compile/assemble a full Raspberry Pi OS image in this
sandbox — that needs an ARM build environment (or `pi-gen`) and
internet access to pull packages, neither of which is available here.
What's included instead is everything Raspberry Pi Imager needs to
build one *for* you:

1. Open **Raspberry Pi Imager**, choose **Raspberry Pi OS Lite (64-bit)**
   as the base, and CardputerZero as the device (or "Raspberry Pi CM
   generic" if it's not yet a listed device option).
2. Click the gear icon → under "Run a custom script on first boot",
   point it at `setup/firstrun.sh` from this project (Imager's OS
   customization screen supports this directly in recent versions).
3. Copy the `app/` folder into the image's `/boot/shadow-games-app/`
   path before/after flashing (Imager lets you mount the boot
   partition, or you can `scp` it in after first boot) — `firstrun.sh`
   copies it into `/opt/shadow-games` and enables it as a systemd
   service, so it autostarts on every boot.
4. Flash, insert the SD card, boot once with network/Wi-Fi available
   for the package install, then reboot — it should come up straight
   into the Shadow Games menu.

## Hardware notes

- **RFID/NFC**: CardputerZero has no onboard RFID/NFC reader — you'll
  need an external PN532 breakout (UART/I2C) or a USB ACR122U.
- **Sub-GHz**: needs an RTL-SDR USB dongle (the Nano 3 works fine here
  since this is a real Linux host with `librtlsdr` support — unlike
  the ESP32-S3 boards, no custom USB driver is required).
- Legal note: receiving/scanning is broadly legal for personal use in
  most places, but transmitting on licensed/ISM bands, and
  cloning/replaying RFID or key-fob signals you don't own or lack
  authorization for, can violate FCC/local radio regulations and
  computer-fraud or wiretapping laws — that's the line this build
  intentionally stays behind.
