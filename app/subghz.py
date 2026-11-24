"""
Sub-GHz module — RECEIVE ONLY.

Two modes:
  1. Spectrum scan: sweeps ISM bands (315/433/868/915 MHz) and plots
     power level, using an RTL-SDR dongle via pyrtlsdr.
  2. "Ghost hunting": treats sudden RF power spikes above the ambient
     noise floor as "anomalies" and shows a live gauge + spike log.
     This is the same principle commercial EMF meters use (RF energy
     detection), just visualized for fun — it is not detecting
     actual ghosts, it is detecting ambient/transient RF energy.

No transmit capability is implemented or exposed here.
"""
import pygame
import time

try:
    from rtlsdr import RtlSdr
    SDR_AVAILABLE = True
except ImportError:
    SDR_AVAILABLE = False

BANDS = [("315 MHz", 315.0e6), ("433 MHz", 433.92e6),
         ("868 MHz", 868.0e6), ("915 MHz", 915.0e6)]

RED = (160, 0, 0)
WHITE = (240, 240, 240)
GRAY = (90, 90, 90)
BLACK = (0, 0, 0)


def _read_power_dbm(sdr, freq_hz):
    sdr.center_freq = freq_hz
    samples = sdr.read_samples(8 * 1024)
    power = (abs(samples) ** 2).mean()
    import math
    return 10 * math.log10(power + 1e-12)


def run_menu(screen, w, h):
    font = pygame.font.SysFont("dejavusansmono", 10)
    mode = "scan"  # or "ghost"
    band_idx = 0

    if not SDR_AVAILABLE:
        _message(screen, w, h, font,
                  ["No RTL-SDR dongle / pyrtlsdr detected.",
                   "Plug in an RTL-SDR USB dongle and retry.",
                   "(ESC to go back)"])
        _wait_for_escape()
        return

    sdr = RtlSdr()
    sdr.sample_rate = 2.048e6
    sdr.gain = "auto"

    history = []
    baseline = None
    clock = pygame.time.Clock()

    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    if event.key == pygame.K_TAB:
                        mode = "ghost" if mode == "scan" else "scan"
                    if event.key in (pygame.K_LEFT, pygame.K_a):
                        band_idx = (band_idx - 1) % len(BANDS)
                    if event.key in (pygame.K_RIGHT, pygame.K_d):
                        band_idx = (band_idx + 1) % len(BANDS)

            name, freq = BANDS[band_idx]
            dbm = _read_power_dbm(sdr, freq)
            history.append(dbm)
            if len(history) > w:
                history.pop(0)

            screen.fill(BLACK)
            title = font.render(f"SUB-GHZ [{mode.upper()}]  {name}", True, WHITE)
            screen.blit(title, (4, 2))

            if mode == "scan":
                for i, val in enumerate(history):
                    y = int(h - 20 - max(0, min(60, val + 60)))
                    pygame.draw.line(screen, RED, (i, h - 20), (i, y))
            else:  # ghost hunting
                if baseline is None and len(history) > 20:
                    baseline = sum(history[-20:]) / 20
                spike = baseline is not None and (dbm - baseline) > 8
                gauge_col = (255, 60, 60) if spike else (60, 160, 60)
                pygame.draw.rect(screen, gauge_col, (20, 60, w - 40, 30))
                label = "ANOMALY" if spike else "quiet"
                lbl = font.render(f"{label}  ({dbm:.1f} dBm)", True, WHITE)
                screen.blit(lbl, lbl.get_rect(center=(w // 2, 110)))

            hint = font.render("TAB: mode  <-/->: band  ESC: back", True, GRAY)
            screen.blit(hint, (4, h - 14))
            pygame.display.flip()
            clock.tick(15)
    finally:
        sdr.close()


def _message(screen, w, h, font, lines):
    screen.fill(BLACK)
    for i, line in enumerate(lines):
        t = font.render(line, True, WHITE)
        screen.blit(t, (10, 20 + i * 14))
    pygame.display.flip()


def _wait_for_escape():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
        time.sleep(0.05)
