import sys
import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

#screen size
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600


DIAMOND_SIZE = 20
CATCHER_SIZE = 90

#var
catcher_x = SCREEN_WIDTH // 2 - CATCHER_SIZE // 2
catcher_y = 20  #catcher_y constant
score = 0
diamond_speed = 0.5
game_over = False
paused = False
diamond_x = random.randint(0, SCREEN_WIDTH - DIAMOND_SIZE)
diamond_y = 600
diamond_color = (random.random(), random.random(), random.random())

#<>
def draw_diamond():
    global diamond_color
    glColor3f(*diamond_color)
    glBegin(GL_POINTS)
    draw_line((diamond_x, diamond_y + DIAMOND_SIZE // 2), (diamond_x - DIAMOND_SIZE // 2, diamond_y))
    draw_line((diamond_x - DIAMOND_SIZE // 2, diamond_y), (diamond_x, diamond_y - DIAMOND_SIZE // 2))
    draw_line((diamond_x, diamond_y - DIAMOND_SIZE // 2), (diamond_x + DIAMOND_SIZE // 2, diamond_y))
    draw_line((diamond_x + DIAMOND_SIZE // 2, diamond_y), (diamond_x, diamond_y + DIAMOND_SIZE // 2))
    glEnd()
    print(diamond_speed,99)

#|===|
def draw_catcher():
    global catcher_x, catcher_y
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_POINTS)
    top_y = catcher_y + CATCHER_SIZE // 5
    bottom_y = catcher_y - CATCHER_SIZE // 5
    left_x = catcher_x - CATCHER_SIZE // 2
    right_x = catcher_x + CATCHER_SIZE // 2
    if game_over:
        glColor3f(1.0, 0.0, 0.0)
    else:
        glColor3f(1.0, 1.0, 1.0)
    draw_line((left_x, top_y), (right_x, top_y))
    draw_line((left_x + 10, bottom_y), (right_x - 10, bottom_y))
    draw_line((left_x, top_y), (left_x + 10, bottom_y))
    draw_line((right_x, top_y), (right_x - 10, bottom_y))
    glEnd()

#w points
def draw_line(start, end):
    x1, y1 = start
    x2, y2 = end
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy
    while True:
        glVertex2f(x1, y1)
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy

#Key_B
def special_keys(key, x, y):
    global catcher_x
    if not game_over and not paused:
        if key == GLUT_KEY_LEFT:
            if catcher_x - CATCHER_SIZE / 2 > 0:
                catcher_x -= 10
        elif key == GLUT_KEY_RIGHT:
            if catcher_x + CATCHER_SIZE / 2 < SCREEN_WIDTH:
                catcher_x += 10

#<> pos change/animate
def update_diamond(_):
    global diamond_y, diamond_x, score, diamond_speed, game_over,diamond_color

    if not game_over and not paused:
        diamond_y -= diamond_speed
        # print(diamond_x,diamond_y)

        # Check collision
        
        if has_collided(diamond_x, diamond_y, DIAMOND_SIZE, DIAMOND_SIZE, catcher_x, catcher_y, CATCHER_SIZE, CATCHER_SIZE):
            score += 1
            diamond_y = 600
            diamond_x = random.randint(0, SCREEN_WIDTH - DIAMOND_SIZE)
            diamond_speed += 0.5
            diamond_color = (random.random(), random.random(), random.random())
            print("Score:", score)

        if diamond_y <= 0:
            game_over = True

    glutTimerFunc(30, update_diamond, 0)
    glutPostRedisplay()

#Check collision algo
def has_collided(x1, y1, w1, h1, x2, y2, w2, h2):
    return x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2-50 + h2 and y1 + h1 > y2-50


#DRAW :3

    #Ab
def draw_text(x, y, text):
    glColor3f(1.0, 1.0, 1.0)
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

    #:(
def draw_game_over():
    glColor3f(1.0, 0.0, 0.0)
    draw_text(SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2, "Game Over")
    draw_text(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 30, "Score: " + str(score))
    
    #....
def draw_score():
    glColor3f(1.0, 1.0, 1.0)
    draw_text(10, SCREEN_HEIGHT - 30, "Score: " + str(score))

#DRAW game things
def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    draw_diamond()
    draw_catcher()
    draw_buttons()
    draw_score()

    if game_over:
        draw_game_over()

    glutSwapBuffers()


#<)(||)---'
def mouse(button, state, x, y):
    global game_over, score, diamond_speed, paused,diamond_y,diamond_x,diamond_color
    y = SCREEN_HEIGHT - y

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if 15 <= x <= 50 and 550 <= y <= 595:
            score = 0
            diamond_speed = 0.5
            print(diamond_speed)
            game_over = False
            paused = False
            diamond_y = 600
            diamond_x = random.randint(0, SCREEN_WIDTH - DIAMOND_SIZE)
            diamond_color = (random.random(), random.random(), random.random())
            glutTimerFunc(50, update_diamond, 0)
        elif 270 <= x <= 295 and  550<= y <= 595:
            paused = not paused
            print("Game", "Paused" if paused else "Resumed")
        elif 555 <= x <= 585 and 550<= y <= 595:
            print("Goodbye")
            glutLeaveMainLoop()

#<---
def draw_right_arrow_button():
    glColor3f(0.0, 0.8, 0.8)
    glBegin(GL_POINTS)
    pointy = (20, 570)
    bottom = (35, 550)
    top = (35, 590)
    middie = (50, 570)
    draw_line(pointy, bottom)
    draw_line(pointy, top)
    draw_line(pointy, middie)
    glEnd()


#<| or ||
def draw_play_pause_button():
    if paused:
        glColor3f(1.0, 0.5, 0.0)
        glBegin(GL_POINTS)
        top_left = (280, 590)
        top_right = (290, 590)
        bottom_left = (280, 550)
        bottom_right = (290, 550)
        draw_line(top_left, bottom_left)
        draw_line(top_right, bottom_right)
        glEnd()
    else:
        glColor3f(1.0, 0.5, 0.0)
        glBegin(GL_POINTS)
        top_vertex = (280, 570)
        bottom_left_vertex = (280, 550)
        bottom_right_vertex = (290, 560)
        draw_line(top_vertex, bottom_left_vertex)
        draw_line(bottom_left_vertex, bottom_right_vertex)
        draw_line(bottom_right_vertex, top_vertex)
        glEnd()


#X
def draw_cross_button():
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_POINTS)
    top_left = (580, 570)
    top_right = (560, 570)
    bottom_left = (580, 550)
    bottom_right = (560, 550)
    draw_line(top_left, bottom_right)
    draw_line(top_right, bottom_left)
    glEnd()

#oooo
def draw_buttons():
    draw_right_arrow_button()
    draw_play_pause_button()
    draw_cross_button()


def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)
    glMatrixMode(GL_MODELVIEW)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(SCREEN_WIDTH, SCREEN_HEIGHT)
    glutCreateWindow(b"Catch the Diamonds!")
    glutDisplayFunc(draw)
    glutSpecialFunc(special_keys)
    glutMouseFunc(mouse)
    init()
    glutTimerFunc(0, update_diamond, 0)
    glutMainLoop()

#func call
if __name__ == "__main__":
    main()

