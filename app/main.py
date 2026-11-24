#!/usr/bin/env python3
"""
SHADOW GAMES — Legitimate Edition
Kiosk launcher for M5Stack CardputerZero (Raspberry Pi CM0, Linux).

Menu layout mirrors the Uagain Shadow screenshot, but every module is
read-only / receive-only:
  RFID      -> read UID + type (needs external PN532/ACR122 reader; no clone)
  NFC       -> read tag data (no emulate)
  Sub-GHz   -> RTL-SDR spectrum scan + "ghost hunting" RF-anomaly mode
  Tools     -> calculator, notes (NOT BadUSB/keystroke payloads)
  Utility   -> settings
  Terminal  -> real shell (xterm) since this is Linux
  Scanner   -> passive Wi-Fi / Bluetooth inventory (no deauth/jamming)
  Files     -> SD card file browser
"""
import pygame
import sys
import time
import os

import subghz
import rfid_nfc
import scanner
import tools
import files
import utility

pygame.init()
pygame.mouse.set_visible(False)

SCREEN_W, SCREEN_H = 320, 170  # CardputerZero's 1.9" panel
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Shadow Games")

RED = (160, 0, 0)
WHITE = (240, 240, 240)
GRAY = (40, 40, 44)
DARKGRAY = (90, 90, 90)
BLACK = (0, 0, 0)

font_big = pygame.font.SysFont("dejavusansmono", 16, bold=True)
font_small = pygame.font.SysFont("dejavusansmono", 9)

MENU = [
    ("RFID", "Read Only", rfid_nfc.run_rfid),
    ("NFC", "Read Only", rfid_nfc.run_nfc),
    ("Sub-GHz", "Scan / Ghost", subghz.run_menu),
    ("Tools", "Utilities", tools.run_menu),
    ("Utility", "Settings", utility.run_menu),
    ("Terminal", "Command Line", tools.run_terminal),
    ("Scanner", "WiFi / BLE", scanner.run_menu),
    ("Files", "Manage Files", files.run_menu),
]

selected = 0


def draw_boot_splash(elapsed_ms):
    screen.fill(BLACK)
    scale = min(1.0, elapsed_ms / 900.0)
    logo = font_big.render("UAGAIN SHADOW", True, RED)
    logo = pygame.transform.smoothscale(
        logo, (int(logo.get_width() * (0.4 + 0.6 * scale)),
               int(logo.get_height() * (0.4 + 0.6 * scale)))
    rect = logo.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 - 10))
    screen.blit(logo, rect)
    sub = font_small.render("SHADOW GAMES  v0.1-legit", True, DARKGRAY)
    screen.blit(sub, sub.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 + 30)))
    pygame.display.flip()


def draw_menu():
    screen.fill(BLACK)
    pygame.draw.rect(screen, GRAY, (0, 0, SCREEN_W, 16))
    hdr = font_small.render("SHADOW GAMES", True, WHITE)
    screen.blit(hdr, (6, 3))

    cols, rows = 2, 4
    cell_w, cell_h = SCREEN_W // cols, (SCREEN_H - 16 - 12) // rows

    for i, (label, sub, _fn) in enumerate(MENU):
        col, row = i // rows, i % rows
        x, y = col * cell_w, 16 + row * cell_h
        sel = (i == selected)
        color = RED if sel else DARKGRAY
        pygame.draw.rect(screen, color, (x + 3, y + 2, cell_w - 6, cell_h - 4), 1,
                          border_radius=4)
        t1 = font_small.render(label, True, WHITE)
        t2 = font_small.render(sub, True, RED if sel else DARKGRAY)
        screen.blit(t1, t1.get_rect(center=(x + cell_w // 2, y + cell_h // 2 - 5)))
        screen.blit(t2, t2.get_rect(center=(x + cell_w // 2, y + cell_h // 2 + 7)))

    foot = font_small.render(files.sd_usage_string(), True, DARKGRAY)
    screen.blit(foot, foot.get_rect(center=(SCREEN_W // 2, SCREEN_H - 6)))
    pygame.display.flip()


def main():
    global selected
    boot_start = time.time()

    # boot splash (~1.4s, logo pops in large)
    while time.time() - boot_start < 1.4:
        draw_boot_splash((time.time() - boot_start) * 1000)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
        time.sleep(0.02)

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    selected = (selected - 2) % 8
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    selected = (selected + 2) % 8
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    selected = (selected - 4) % 8
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    selected = (selected + 4) % 8
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    MENU[selected][2](screen, SCREEN_W, SCREEN_H)
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)

        draw_menu()
        clock.tick(30)


if __name__ == "__main__":
    main()
