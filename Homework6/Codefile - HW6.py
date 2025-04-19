import pygame
import numpy as np

width, height = 800, 600
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Smooth Hermite Curve Through All Points")
font = pygame.font.SysFont("consolas", 14)
clock = pygame.time.Clock()


WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

pts = []

def printText(msg, color='WHITE', pos=(15, 15)):
    textSurface = font.render(msg, True, pygame.Color(color), None)
    screen.blit(textSurface, textSurface.get_rect(topleft=pos))

def drawPoint(pt, color='BLUE', thick=3):
    pygame.draw.circle(screen, pygame.Color(color), pt, thick)

def hermite_curve(t, P0, P1, T0, T1):
    h00 = 2 * t**3 - 3 * t**2 + 1
    h10 = t**3 - 2 * t**2 + t
    h01 = -2 * t**3 + 3 * t**2
    h11 = t**3 - t**2
    return h00 * P0 + h10 * T0 + h01 * P1 + h11 * T1

def estimate_tangents(points):
    n = len(points)
    tangents = []
    for i in range(n):
        if i == 0:
            t = 0.5 * (np.array(points[1]) - np.array(points[0]))
        elif i == n - 1:
            t = 0.5 * (np.array(points[-1]) - np.array(points[-2]))
        else:
            t = 0.5 * (np.array(points[i + 1]) - np.array(points[i - 1]))
        tangents.append(t)
    return tangents

def draw_smooth_hermite_curve(points, steps=30):
    if len(points) < 2:
        return
    tangents = estimate_tangents(points)
    for i in range(len(points) - 1):
        P0 = np.array(points[i])
        P1 = np.array(points[i + 1])
        T0 = tangents[i]
        T1 = tangents[i + 1]
        for j in range(steps):
            t1 = j / steps
            t2 = (j + 1) / steps
            pt1 = hermite_curve(t1, P0, P1, T0, T1)
            pt2 = hermite_curve(t2, P0, P1, T0, T1)
            pygame.draw.line(screen, RED, pt1, pt2, 2)

def main():
    global pts
    running = True
    screen.fill(WHITE)
    old_button1 = 0

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        button1, _, _ = pygame.mouse.get_pressed()
        x, y = pygame.mouse.get_pos()
        pt = [x, y]
        if old_button1 == 1 and button1 == 0:
            pts.append(pt)

        screen.fill(WHITE)
        for p in pts:
            drawPoint(p, 'BLUE', 4)
        if len(pts) >= 2:
            draw_smooth_hermite_curve(pts)
          
        pygame.draw.rect(screen, BLACK, (10, 10, 420, 80))
        printText("Click to add points. A Hermite curve will pass through them.", pos=(15, 15))
        printText(f"Total points: {len(pts)}", pos=(15, 40))

        pygame.display.flip()
        old_button1 = button1

    pygame.quit()

if __name__ == "__main__":
    main()
