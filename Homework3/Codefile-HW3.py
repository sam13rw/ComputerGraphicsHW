"""
Modified on Apr 2025
@author: lbg@dongseo.ac.kr
@modified: vsamueldavid18@gmail.com
"""

import pygame
from sys import exit
import numpy as np

width = 800
height = 600
pygame.init()
screen = pygame.display.set_mode((width, height), 0, 32)
pygame.display.set_caption("ImagePolylineMouseButton")

# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

pts = []
knots = []
count = 0
screen.fill(WHITE)
font= pygame.font.SysFont("consolas",14)

# https://kite.com/python/docs/pygame.Surface.blit
clock= pygame.time.Clock()

def printText(msg, color='WHITE', pos=(15,15)):
    textSurface = font.render(msg, True, pygame.Color(color), None)
    textRect = textSurface.get_rect()
    textRect.topleft = pos
    screen.blit(textSurface, textRect)

def drawPoint(pt, color='GREEN', thick=3):
    pygame.draw.circle(screen, color, pt, thick)

#for 2D
def ptline(pt0, pt1, alpha):
    return (1 - alpha) * pt0 + alpha * pt1

#HW2 implement drawLine with drawPoint
def drawLine(pt0, pt1, color = 'GREEN', thick = 3, ncircles = 1000):
    drawPoint(pt1, color, thick)
    if pt0 != pt1:
        for i in range(-1 * ncircles, 2 * (ncircles + 1)):
            pt_x = ptline(pt0[0], pt1[0], i / ncircles)
            pt_y = ptline(pt0[1], pt1[1], i / ncircles)
            drawPoint([int(pt_x), int(pt_y)], color, thick=2)

def drawPolylines(color='GREEN', thick=3):
    if count == 1:
        drawLine(pts[0], pts[0], color)
    elif count <= 3:
        for i in range(count - 1):
            drawLine(pts[i], pts[i + 1], color, ncircles=1000)
            if ((i - 1) % 3) == 0:
                drawLine(pts[i - 1], pts[i + 1], color, ncircles=1000)

def barycentricPoint(current_point, base_points):
    [t0, t1] = np.matmul(np.linalg.inv(base_points), current_point)
    return round(t0 ,3) , round(t1, 3), round(1 - t0 - t1, 3)

#Loop until the user clicks the close button.
done = False
pressed = 0
margin = 6
old_pressed = 0
old_button1 = 0

while not done:
    # This limits the while loop to a max of 10 times per second.
    # Leave this out and we will use all CPU we can.
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
    pygame.draw.circle(screen, RED, pt, 0)

    if old_pressed == -1 and pressed == 1 and old_button1 == 1 and button1 == 0 :
        pts.append(pt)
        count += 1
        if count <= 3:
            pygame.draw.rect(screen, BLUE, (pt[0]-margin, pt[1]-margin, 2*margin, 2*margin), 5)

    if len(pts)>=0:
        drawPolylines(GREEN, 1)

    pygame.draw.rect(screen, BLACK, (10, 10, 405, 125))
    printText("current point = (" + str(pt[0]) + "," + str(pt[1]) + ")", pos=(15, 15))

    if count != 0:
        pos = 35
        if count > 3:
            corner = 3
        else:
            corner = count
        for i in range(corner):
            printText("P" + str(i) + " = (" + str(pts[i][0]) + "," + str(pts[i][1]) + ")", pos = (15, pos))
            pos += 20
        if corner == 3:
            base_points = np.transpose([np.subtract(pts[0], pts[2]), np.subtract(pts[1], pts[2])])
            current_point = np.subtract(pt, pts[2]).tolist()
            t0, t1, t2 = barycentricPoint(current_point, base_points)
            printText("(t0, t1, t2) = (" + str(t0) + "," + str(t1) + "," + str(t2) + ")", pos = (15, pos))
            if t0 >= 0 and t1 >= 0 and t2 >= 0:
                printText("Current point is inside triangle", pos = (15, pos + 20))
            else:
                printText("Current point is outside triangle", pos=(15, pos + 20))


    # Go ahead and update the screen with what we've drawn.
    # This MUST happen after all the other drawing commands.
    pygame.display.update()
    old_button1 = button1
    old_pressed = pressed

pygame.quit()
