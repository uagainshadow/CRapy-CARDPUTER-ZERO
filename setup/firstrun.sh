#!/bin/bash
# =====================================================================
# SHADOW GAMES — Legitimate Edition — first-boot setup
#
# How to use with Raspberry Pi Imager:
#   1. In Raspberry Pi Imager, choose "Raspberry Pi OS Lite (64-bit)"
#      as the base OS for CardputerZero.
#   2. Click the gear icon -> "Advanced options" -> under
#      "Run a custom script on first boot" (or via the Imager's
#      OS customization screen), point it at this file, OR copy this
#      file into the boot partition as firstrun.sh per M5Stack's
#      CardputerZero "System Image and Recovery" docs.
#   3. Flash, boot once (it needs network to apt-get), then reboot.
#
# Scope: spectrum scanning (RTL-SDR), read-only RFID/NFC, passive
# Wi-Fi/BT inventory, file manager, terminal. No RF transmit, no
# RFID/NFC clone or emulate, no keystroke-injection payloads.
# =====================================================================
set -e

apt-get update
apt-get install -y \
  python3-pip python3-pygame \
  rtl-sdr librtlsdr-dev \
  libnfc-bin libnfc-dev pcscd pcsc-tools \
  network-manager bluez \
  git

pip3 install --break-system-packages pyrtlsdr nfcpy pyscard

mkdir -p /opt/shadow-games
cp -r /boot/shadow-games-app/* /opt/shadow-games/ 2>/dev/null || true

cat > /etc/systemd/system/shadow-games.service << 'EOF'
[Unit]
Description=Shadow Games kiosk app
After=multi-user.target

[Service]
Type=simple
Environment=SDL_FBDEV=/dev/fb0
ExecStart=/usr/bin/python3 /opt/shadow-games/main.py
Restart=always
User=root

[Install]
WantedBy=multi-user.target
EOF

systemctl enable shadow-games.service
