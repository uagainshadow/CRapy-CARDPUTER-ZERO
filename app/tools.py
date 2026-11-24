"""
Tools module — replaces the "Payloads" concept with ordinary utilities.
No BadUSB / keystroke-injection / duckyscript execution lives here.
"""
import pygame
import subprocess

WHITE = (240, 240, 240)
RED = (160, 0, 0)
BLACK = (0, 0, 0)
GRAY = (90, 90, 90)


def run_menu(screen, w, h):
    font = pygame.font.SysFont("dejavusansmono", 10)
    items = ["Calculator (opens xcalc)", "Notes (opens nano in terminal)",
              "System info"]
    sel = 0
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key in (pygame.K_UP, pygame.K_w):
                    sel = (sel - 1) % len(items)
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    sel = (sel + 1) % len(items)
                if event.key == pygame.K_RETURN:
                    if sel == 0:
                        subprocess.Popen(["xcalc"])
                    elif sel == 1:
                        subprocess.Popen(["xterm", "-e", "nano", "/home/pi/notes.txt"])
                    elif sel == 2:
                        subprocess.Popen(["xterm", "-e", "htop"])

        screen.fill(BLACK)
        screen.blit(font.render("TOOLS", True, WHITE), (4, 2))
        for i, label in enumerate(items):
            screen.blit(font.render(label, True, RED if i == sel else GRAY),
                        (6, 20 + i * 14))
        screen.blit(font.render("ESC: back", True, GRAY), (4, h - 14))
        pygame.display.flip()
        clock.tick(15)


def run_terminal(screen, w, h):
    """Launches a real shell — this is a Linux computer, not a BadUSB target."""
    subprocess.Popen(["xterm"])
