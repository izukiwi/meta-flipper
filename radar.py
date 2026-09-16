import sys
import math
import threading
import time
import requests
import pygame

WIDTH, HEIGHT = 800, 800
CENTER = (WIDTH // 2, HEIGHT // 2)
MAX_DISTANCE = 10.0  # Distance maximale représentée (en mètres)
SCALE = (WIDTH // 2 - 50) / MAX_DISTANCE

COLOR_BG = (10, 20, 10)
COLOR_GRID = (0, 80, 0)
COLOR_TEXT = (0, 255, 100)
COLOR_SWEEP = (0, 255, 80)
COLOR_TARGET = (50, 255, 50)

detected_targets = []

def poll_api():
    global detected_targets
    while True:
        try:
            r = requests.get("http://127.0.0.1:8000/targets", timeout=1.0)
            if r.status_code == 200:
                detected_targets = r.json()
        except Exception:
            pass
        time.sleep(0.5)

threading.Thread(target=poll_api, daemon=True).start()

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Meta Radar Sonar")
clock = pygame.time.Clock()
font = pygame.font.SysFont("monospace", 14)

sweep_angle = 0.0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()

    screen.fill(COLOR_BG)

    # 1. Dessin des cercles de distance (2m, 5m, 8m, 10m)
    for dist in [2.0, 5.0, 8.0, 10.0]:
        r = int(dist * SCALE)
        pygame.draw.circle(screen, COLOR_GRID, CENTER, r, 1)
        lbl = font.render(f"{dist:.0f}m", True, COLOR_GRID)
        screen.blit(lbl, (CENTER[0] + 5, CENTER[1] - r - 15))

    # Axes orthogonaux
    pygame.draw.line(screen, COLOR_GRID, (CENTER[0], 40), (CENTER[0], HEIGHT - 40), 1)
    pygame.draw.line(screen, COLOR_GRID, (40, CENTER[1]), (WIDTH - 40, CENTER[1]), 1)

    # 2. Balayage radar
    sweep_angle = (sweep_angle + 2.0) % 360
    rad = math.radians(sweep_angle)
    sweep_x = CENTER[0] + (WIDTH // 2 - 50) * math.cos(rad)
    sweep_y = CENTER[1] + (WIDTH // 2 - 50) * math.sin(rad)
    pygame.draw.line(screen, COLOR_SWEEP, CENTER, (sweep_x, sweep_y), 2)

    # 3. Affichage des cibles Meta
    for t in detected_targets:
        dist = min(t["distance"], MAX_DISTANCE)
        angle_rad = math.radians(t["angle"])
        
        tx = int(CENTER[0] + dist * SCALE * math.cos(angle_rad))
        ty = int(CENTER[1] + dist * SCALE * math.sin(angle_rad))

        # Différence d'angle pour calculer la rémanence lumineuse
        angle_diff = (sweep_angle - t["angle"]) % 360
        if angle_diff < 90:
            alpha = int(255 * (1 - angle_diff / 90))
            # Dessin de l'écho
            pygame.draw.circle(screen, (0, alpha, 0), (tx, ty), 8)
            pygame.draw.circle(screen, COLOR_TARGET, (tx, ty), 3)

            # Texte d'information sous la cible
            txt = font.render(f"{t['name']} | {t['distance']:.1f}m", True, COLOR_TEXT)
            screen.blit(txt, (tx + 10, ty - 10))

    pygame.display.flip()
    clock.tick(60)