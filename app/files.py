"""File browser + SD usage string for the footer."""
import pygame
import os
import shutil

WHITE = (240, 240, 240)
RED = (160, 0, 0)
BLACK = (0, 0, 0)
GRAY = (90, 90, 90)

ROOT = "/home/pi"


def sd_usage_string():
    try:
        total, used, free = shutil.disk_usage("/")
        return f"SD: {used // (1024**3)}GB / {total // (1024**3)}GB"
    except Exception:
        return "SD: --"


def run_menu(screen, w, h):
    font = pygame.font.SysFont("dejavusansmono", 9)
    path = ROOT
    sel = 0
    clock = pygame.time.Clock()

    while True:
        try:
            entries = sorted(os.listdir(path))
        except Exception:
            entries = []
        display = [".."] + entries

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key in (pygame.K_UP, pygame.K_w):
                    sel = (sel - 1) % max(1, len(display))
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    sel = (sel + 1) % max(1, len(display))
                if event.key == pygame.K_RETURN and display:
                    choice = display[sel]
                    new_path = os.path.dirname(path) if choice == ".." else os.path.join(path, choice)
                    if os.path.isdir(new_path):
                        path, sel = new_path, 0

        screen.fill(BLACK)
        screen.blit(font.render(f"FILES: {path}", True, WHITE), (4, 2))
        for i, name in enumerate(display[:10]):
            screen.blit(font.render(name[:28], True, RED if i == sel else GRAY),
                        (6, 18 + i * 12))
        screen.blit(font.render("ESC: back", True, GRAY), (4, h - 14))
        pygame.display.flip()
        clock.tick(15)
