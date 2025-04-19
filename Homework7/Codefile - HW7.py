import pygame
import numpy as np

width, height = 800, 600
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Cubic B-spline Curve")
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

def bspline_basis(t):
    B0 = (1 - t)**3 / 6
    B1 = (3*t**3 - 6*t**2 + 4) / 6
    B2 = (-3*t**3 + 3*t**2 + 3*t + 1) / 6
    B3 = t**3 / 6
    return [B0, B1, B2, B3]

def bspline_point(P0, P1, P2, P3, t):
    B = bspline_basis(t)
    return B[0]*P0 + B[1]*P1 + B[2]*P2 + B[3]*P3

def draw_bspline_curve(points, steps=30):
    if len(points) < 4:
        return
    for i in range(len(points) - 3):
        P0 = np.array(points[i])
        P1 = np.array(points[i+1])
        P2 = np.array(points[i+2])
        P3 = np.array(points[i+3])
        for j in range(steps):
            t1 = j / steps
            t2 = (j + 1) / steps
            pt1 = bspline_point(P0, P1, P2, P3, t1)
            pt2 = bspline_point(P0, P1, P2, P3, t2)
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


        draw_bspline_curve(pts)

        pygame.draw.rect(screen, BLACK, (10, 10, 450, 80))
        printText("Click to add points. Cubic B-spline curve will be drawn.", pos=(15, 15))
        printText(f"Total control points: {len(pts)}", pos=(15, 40))

        pygame.display.flip()
        old_button1 = button1

    pygame.quit()

if __name__ == "__main__":
    main()
