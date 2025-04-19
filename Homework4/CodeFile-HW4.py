import pygame
from sys import exit
import numpy as np

width = 800
height = 600
pygame.init()
screen = pygame.display.set_mode((width, height), 0, 32)
pygame.display.set_caption("Lagrange Interpolation")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pts = []
count = 0
screen.fill(WHITE)
font = pygame.font.SysFont("consolas", 14)
clock = pygame.time.Clock()

def printText(msg, color='WHITE', pos=(15,15)):
    textSurface = font.render(msg, True, pygame.Color(color), None)
    textRect = textSurface.get_rect()
    textRect.topleft = pos
    screen.blit(textSurface, textRect)

def drawPoint(pt, color='GREEN', thick=3):
    pygame.draw.circle(screen, color, pt, thick)

def lagrange_interpolation(x_vals, y_vals, x):
    total = 0
    n = len(x_vals)
    for i in range(n):
        xi, yi = x_vals[i], y_vals[i]
        term = yi
        for j in range(n):
            if i != j:
                xj = x_vals[j]
                term *= (x - xj) / (xi - xj)
        total += term
    return total

def draw_lagrange_curve(points, color='BLUE', step=1):
    if len(points) < 2:
        return
    x_vals = [p[0] for p in points]
    y_vals = [p[1] for p in points]
    
    prev_point = None
    for x in range(min(x_vals), max(x_vals), step):
        try:
            y = lagrange_interpolation(x_vals, y_vals, x)
            current_point = (x, int(y))
            if prev_point:
                pygame.draw.line(screen, pygame.Color(color), prev_point, current_point, 2)
            prev_point = current_point
        except ZeroDivisionError:
            pass

done = False
pressed = 0
old_pressed = 0
old_button1 = 0
margin = 6

while not done:
    time_passed = clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            pressed = -1
        elif event.type == pygame.MOUSEBUTTONUP:
            pressed = 1
        elif event.type == pygame.QUIT:
            done = True
        else:
            pressed = 0

    button1, button2, button3 = pygame.mouse.get_pressed()
    x, y = pygame.mouse.get_pos()
    pt = [x, y]

    if old_pressed == -1 and pressed == 1 and old_button1 == 1 and button1 == 0:
        pts.append(pt)
        count += 1
        pygame.draw.rect(screen, BLUE, (pt[0]-margin, pt[1]-margin, 2*margin, 2*margin), 5)

    screen.fill(WHITE)

    for p in pts:
        drawPoint(p, 'GREEN', 4)

    draw_lagrange_curve(pts, 'RED')

    pygame.draw.rect(screen, BLACK, (10, 10, 405, 125))
    printText("current point = (" + str(pt[0]) + "," + str(pt[1]) + ")", pos=(15, 15))

    pos = 35
    for i in range(len(pts)):
        printText(f"P{i} = ({pts[i][0]},{pts[i][1]})", pos=(15, pos))
        pos += 20

    pygame.display.update()
    old_button1 = button1
    old_pressed = pressed

pygame.quit()
