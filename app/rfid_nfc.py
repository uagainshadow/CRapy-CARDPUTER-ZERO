"""
RFID / NFC module — READ ONLY.

CardputerZero has no RFID/NFC reader built in; this talks to an
external reader over USB/UART (e.g. a PN532 breakout or an ACR122U),
using nfcpy. It shows the tag UID and type. It does not write,
clone, or emulate tags.
"""
import pygame
import time

try:
    import nfc
    NFC_AVAILABLE = True
except ImportError:
    NFC_AVAILABLE = False

WHITE = (240, 240, 240)
RED = (160, 0, 0)
BLACK = (0, 0, 0)
GRAY = (90, 90, 90)


def _poll_once(timeout_s=2.0):
    """Return (uid_hex, tag_type) or None."""
    if not NFC_AVAILABLE:
        return None
    try:
        clf = nfc.ContactlessFrontend('usb')
    except Exception:
        return None
    result = {}

    def on_connect(tag):
        result["uid"] = tag.identifier.hex().upper()
        result["type"] = type(tag).__name__
        return True

    try:
        clf.connect(rdwr={"on-connect": on_connect}, terminate=lambda: False,
                    interval=0.2)
    except Exception:
        pass
    finally:
        clf.close()
    return result or None


def _run(screen, w, h, title):
    font = pygame.font.SysFont("dejavusansmono", 10)
    clock = pygame.time.Clock()
    last = None
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        screen.fill(BLACK)
        hdr = font.render(f"{title} — READ ONLY", True, WHITE)
        screen.blit(hdr, (4, 4))

        if not NFC_AVAILABLE:
            msg = ["nfcpy / reader not detected.",
                   "Connect a PN532 or ACR122U reader.", "ESC: back"]
            for i, line in enumerate(msg):
                t = font.render(line, True, GRAY)
                screen.blit(t, (10, 30 + i * 14))
        else:
            tag = _poll_once()
            if tag:
                last = tag
            if last:
                screen.blit(font.render(f"UID:  {last['uid']}", True, RED), (10, 40))
                screen.blit(font.render(f"Type: {last['type']}", True, WHITE), (10, 58))
            else:
                screen.blit(font.render("Hold a tag near the reader...", True, GRAY),
                            (10, 40))

        screen.blit(font.render("ESC: back", True, GRAY), (4, h - 14))
        pygame.display.flip()
        clock.tick(10)


def run_rfid(screen, w, h):
    _run(screen, w, h, "RFID")


def run_nfc(screen, w, h):
    _run(screen, w, h, "NFC")
