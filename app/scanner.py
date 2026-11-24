"""
Scanner module — PASSIVE inventory only.
Lists nearby Wi-Fi networks (nmcli) and Bluetooth/BLE devices
(bluetoothctl). No deauthentication, no jamming, no packet injection.
"""
import pygame
import subprocess
import time

WHITE = (240, 240, 240)
RED = (160, 0, 0)
BLACK = (0, 0, 0)
GRAY = (90, 90, 90)


def _wifi_scan():
    try:
        out = subprocess.check_output(
            ["nmcli", "-t", "-f", "SSID,SIGNAL,CHAN", "dev", "wifi", "list"],
            timeout=6, text=True)
        rows = []
        for line in out.strip().splitlines():
            parts = line.split(":")
            if len(parts) >= 3 and parts[0]:
                rows.append((parts[0], parts[1], parts[2]))
        return rows
    except Exception:
        return []


def run_menu(screen, w, h):
    font = pygame.font.SysFont("dejavusansmono", 9)
    clock = pygame.time.Clock()
    results = []
    last_scan = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        if time.time() - last_scan > 5:
            results = _wifi_scan()
            last_scan = time.time()

        screen.fill(BLACK)
        screen.blit(font.render("WIFI SCAN (passive)", True, WHITE), (4, 2))
        for i, (ssid, sig, chan) in enumerate(results[:10]):
            line = f"{ssid[:16]:16s} {sig:>3s}% ch{chan}"
            screen.blit(font.render(line, True, RED if i == 0 else GRAY),
                        (6, 18 + i * 12))
        screen.blit(font.render("ESC: back", True, GRAY), (4, h - 14))
        pygame.display.flip()
        clock.tick(10)
