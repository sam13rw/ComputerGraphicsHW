import pygame
import numpy as np

width, height = 800, 600
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Cubic Bezier")
font = pygame.font.SysFont("consolas", 14)
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

pts = []

def printText(msg, color='WHITE', pos=(15, 15)):
    textSurface = font.render(msg, True, pygame.Color(color), None)
    screen.blit(textSurface, textSurface.get_rect(topleft=pos))

def drawPoint(pt, color='BLUE', thick=3):
    pygame.draw.circle(screen, pygame.Color(color), pt, thick)

def cubic_bezier(t, P0, P1, P2, P3):
    return (
        (1 - t)**3 * np.array(P0) +
        3 * (1 - t)**2 * t * np.array(P1) +
        3 * (1 - t) * t**2 * np.array(P2) +
        t**3 * np.array(P3)
    )

def get_bezier_points_from_catmull_rom(p0, p1, p2, p3, alpha=0.5):

    d1 = np.linalg.norm(np.array(p1) - np.array(p0))
    d2 = np.linalg.norm(np.array(p2) - np.array(p1))
    d3 = np.linalg.norm(np.array(p3) - np.array(p2))

    if d1 + d2 == 0 or d2 + d3 == 0:
        return p1, p2  # Avoid divide-by-zero

    a1 = (2 * d1 + d2) * d2 / (3 * (d1 + d2)) if (d1 + d2) != 0 else 0
    a2 = (2 * d3 + d2) * d2 / (3 * (d3 + d2)) if (d3 + d2) != 0 else 0

    ctrl1 = np.array(p1) + a1 * (np.array(p2) - np.array(p0)) / d2
    ctrl2 = np.array(p2) - a2 * (np.array(p3) - np.array(p1)) / d2

    return ctrl1.tolist(), ctrl2.tolist()

def draw_smooth_bezier_through_points(points, steps=30):
    n = len(points)
    if n < 2:
        return

    # Duplicate endpoints to maintain tension at ends
    full = [points[0]] + points + [points[-1]]

    for i in range(1, len(points) - 1):
        p0, p1, p2, p3 = full[i - 1], full[i], full[i + 1], full[i + 2]
        ctrl1, ctrl2 = get_bezier_points_from_catmull_rom(p0, p1, p2, p3)
        for j in range(steps):
            t1 = j / steps
            t2 = (j + 1) / steps
            pt1 = cubic_bezier(t1, p1, ctrl1, ctrl2, p2)
            pt2 = cubic_bezier(t2, p1, ctrl1, ctrl2, p2)
            pygame.draw.line(screen, RED, pt1, pt2, 2)

def main():
    global pts
    running = True
    screen.fill(WHITE)
    margin = 6
    old_pressed = 0
    old_button1 = 0

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        button1, _, _ = pygame.mouse.get_pressed()
        x, y = pygame.mouse.get_pos()
        pt = [x, y]

        pressed = 0
        if old_button1 == 1 and button1 == 0:
            pts.append(pt)

        screen.fill(WHITE)

        for p in pts:
            drawPoint(p, 'BLUE', 4)

        if len(pts) >= 4:
            draw_smooth_bezier_through_points(pts)

        pygame.draw.rect(screen, BLACK, (10, 10, 420, 80))
        printText("Click to add points.", pos=(15, 15))
        printText(f"Total points: {len(pts)}", pos=(15, 40))

        pygame.display.flip()
        old_button1 = button1

    pygame.quit()

if __name__ == "__main__":
    main()
