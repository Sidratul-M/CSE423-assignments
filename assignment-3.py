from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math


SCREEN_HEIGHT = 500
SCREEN_WIDTH = 500

r = 10
shooter_x = SCREEN_WIDTH // 2
shooter_y = r
exit = False
#top buttons
restart_area = (30, SCREEN_HEIGHT - 50)
pause_play_area = (SCREEN_WIDTH/2, SCREEN_HEIGHT-50)
cross_area = (SCREEN_WIDTH-50, SCREEN_HEIGHT-50)
#variables
speed = 0.4
max_miss = 3
max_misfire = 3
misfire = 0
score = 0
game_over = False
pause = False


def draw_points(x, y, color, size):
    glColor3fv(color)
    glPointSize(size)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

################## midpoint Line #########################
def zone_conv_L(x1, y1, x2, y2):
    dx = x2-x1
    dy = y2-y1
    abs_dx = abs(dx)
    abs_dy = abs(dy)
    if (dx > 0 and dy > 0) and (abs_dx >= abs_dy):
        zone = 0
        return x1, y1, x2, y2, zone
    elif (dx > 0 and dy > 0) and (abs_dx < abs_dy):
        zone = 1
        return x1, y1, x2, y2, zone
    elif (dx < 0 and dy > 0) and (abs_dx < abs_dy):
        zone = 2
        return y1, -x1, y2, -x2, zone
    elif (dx < 0 and dy > 0) and (abs_dx >= abs_dy):
        zone = 3
        return -x1, y1, -x2, y2, zone
    elif (dx < 0 and dy < 0) and (abs_dx >= abs_dy):
        zone = 4
        return -x1, -y1, -x2, -y2, zone
    elif (dx < 0 and dy < 0) and (abs_dx < abs_dy):
        zone = 5
        return -y1, -x1, -y2, -x2, zone
    elif (dx > 0 and dy < 0) and (abs_dx < abs_dy):
        zone = 6
        return -y1, x1, -y2, x2, zone
    else:
        zone = 7
        return x1, -y1, x2, -y2, zone


def midpoint_L(x1, y1, x2, y2, color=(1, 1, 1)):
    x1, y1, x2, y2, zone = zone_conv_L(x1, y1, x2, y2)
    dx = x2 - x1
    dy = y2 - y1
    d = 2*dy - dx
    E = 2*dy
    NE = 2*(dy-dx)
    y = y1
    x = x1
    draw_points(x, y, color, 3)
    while (x <= x2):
        if (d > 0):
            d += NE
            x += 1
            y += 1
        else:
            d += E
            x += 1
        x_t, y_t = init_zone(x, y, zone)
        draw_points(x_t, y_t, color, 3)


def init_zone(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y
    else:
        print("Err")
        return x, y

#################|>#######################
def draw_Play(x, y):
    color = (1.0, 0.5, 0.0)
    
    midpoint_L(x - 10, y + 20, x - 10, y - 20,color)  # Left vertical line
    midpoint_L(x - 10, y + 20, x - 9, y - 20,color)  # Left vertical line
    midpoint_L(x - 10, y - 20, x + 20, y,color)       # Diagonal line
    midpoint_L(x + 20, y, x - 10, y + 20,color)       # Hypotenuse line

#################||#######################

def draw_Pause(x, y):
    color = (1.0, 0.5, 0.0)
    # midpoint_L(x - 10, y + 40, x - 10, y - 40)
    # midpoint_L(x + 10, y + 40, x + 10, y - 40)
    midpoint_L(238,465,239,430,color)  # Left 
    midpoint_L(257, 465, 260, 430,color)  # Right####################################e

#################<--#######################

def draw_restart(x, y):
    color = (0.0, 0.5, 1.0)
    midpoint_L(x, y, x+40, y, color)
    midpoint_L(x, y, x+20, y+20, color)
    midpoint_L(x, y, x+20, y-20, color)

#################X#######################

def draw_cross(x, y):
    color = (1.0, 0.0, 0.0)
    midpoint_L(x - 10, y + 10, x + 10, y - 10, color)
    midpoint_L(x - 10, y - 10, x + 10, y + 10, color)
###################################################################
###################################################################




#################initializing vars#######################
def restart():
    global game_over, score, pause, falling_circles, striker_circles, shooter_x, max_miss, misfire
    game_over = False
    score = 0
    pause = False
    shooter_x = SCREEN_WIDTH // 2
    max_miss = 3
    misfire = 0
    falling_circles.clear()
    striker_circles.clear()
    print("Starting Over")


#################Circle draw#######################
################## midpoint Circle #########################
    
def mpCircle_algorithm(r, c_x, c_y, color):
    d = 1 - r
    x = 0
    y = r

    while x < y:
        for i in range(8):
            x1, y1 = conv_Zone(x, y, i)
            draw_points(x1 + c_x, y1 + c_y, color, 3)

        if d < 0:  # E
            d += 2 * x + 3
            x += 1
        else:      # SE
            d += 2 * x - 2 * y + 5
            x += 1
            y -= 1


def conv_Zone(x, y, z):
    if z == 0:
        return x, y
    if z == 1:
        return y, x
    if z == 2:
        return -y, x
    if z == 3:
        return -x, y
    if z == 4:
        return -x, -y
    if z == 5:
        return -y, -x
    if z == 6:
        return y, -x
    if z == 7:
        return x, -y



falling_circles = []
striker_circles = []

################## striker & shooter #########################
def draw_shooter():
    mpCircle_algorithm(r, shooter_x, shooter_y, (1.0, 0.75, 0.0))


def draw_strikers():
    for i in striker_circles:
        mpCircle_algorithm(15, i[0], i[1], (1.0, 0.75, 0.0))


def update_strikers():
    global striker_circles, misfire, game_over, max_misfire
    for s in striker_circles[:]:
        s[1] += 30
        if s[1] > SCREEN_HEIGHT:
            striker_circles.remove(s)
            misfire += 1
            print("Misfire:", misfire)
            if misfire >= max_misfire:
                game_over = True


################## targets #########################
def generate_falling_circle():
    falling_circles.append([random.randint(r, SCREEN_WIDTH - r), random.randint(SCREEN_HEIGHT // 2, SCREEN_HEIGHT - r)])


# for c in range(0,3):
#     generate_falling_circle()


def draw_falling_circles():
    for i in falling_circles:
        mpCircle_algorithm(15, i[0], i[1], (1.0, 0.75, 0.0))


def update_falling_circles():
    global game_over, max_miss, shooter_x
    for c in falling_circles[:]:
        c[1] -= speed
        if c[1] < 0:
            falling_circles.remove(c)
            max_miss -= 1
            print("Chances:", max_miss)
            if max_miss == 0:
                game_over = True
                print("Game Over! Score:", score)
        elif abs(c[0] - shooter_x) < r * 2 and c[1] <= shooter_y + r * 2:
            game_over = True
            print("Game Over! Score:", score)


#Draw :3
def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    draw_shooter()
    draw_falling_circles()
    draw_strikers()
    draw_restart(restart_area[0], restart_area[1])
    draw_cross(cross_area[0], cross_area[1])
    if not pause:
        draw_Pause(pause_play_area[0], pause_play_area[1])
    else:
        draw_Play(pause_play_area[0], pause_play_area[1])
    glutSwapBuffers()

# |_|_|_|
def keyboardListener(key, x, y):
    global shooter_x, game_over
    if game_over:
        return
    
    elif key == b"a" and shooter_x - r > 0:
        shooter_x -= 30
        if shooter_x < r:
            shooter_x = r

    elif key == b"d" and shooter_x + r < SCREEN_WIDTH:
        shooter_x += 30


        if shooter_x > SCREEN_WIDTH - r:
            shooter_x = SCREEN_WIDTH - r

    elif key == b" " and not game_over:
        shoot()



#<)(||)---' #################################
def mouseListener(button, state, x, y):
    global pause, game_over, score, exit

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        y_transformed = SCREEN_HEIGHT - y
        if restart_area[0] <= x <= restart_area[0]+40 and y_transformed >= restart_area[1]-30 and y_transformed <= restart_area[1]+30:
            restart()
            print("Starting Over")


        elif pause_play_area[0]-10 <= x <= pause_play_area[0]+10 and y_transformed >= restart_area[1]-30 and y_transformed <= restart_area[1]+30:
            pause = not pause
            print("Game Paused" if pause else "Game Resumed")


        elif cross_area[0]-10 <= x <= cross_area[0]+10 and y_transformed >= cross_area[1]-10 and y_transformed <= cross_area[1]+10:
            print("Goodbye. Score:", score)
            exit = True


def shoot():
    global striker_circles, misfire, pause, game_over

    if not pause and not game_over:

        shot = [shooter_x, shooter_y + r]
        striker_circles.append(shot)


def update():
    global falling_circles, pause, game_over, score, misfire, max_misfire

    if not pause and not game_over:
        if len(falling_circles) < 3:
            generate_falling_circle()
        update_falling_circles()
        update_strikers()
        dhakka()

        if misfire >= max_misfire:
            if not game_over:
                print(f"Game Over! Score: {score}")
    
            game_over = True
            falling_circles.clear()


def dhakka():
    global score, striker_circles, falling_circles
    for s in striker_circles[:]:
        for c in falling_circles[:]:
            distance = math.sqrt((c[0] - s[0]) ** 2 + (c[1] - s[1]) ** 2)
            if distance < r * 2:
                striker_circles.remove(s)
                falling_circles.remove(c)
                score += 1
    
                print("Score:", score)
                break
    
    if exit:
        print("Goodbye. Score:", score)
        glutLeaveMainLoop()
    glutPostRedisplay()


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(SCREEN_WIDTH, SCREEN_HEIGHT)
glutCreateWindow(b"Shoot The Circles!")
glClearColor(0.0, 0.0, 0.0, 1.0)
gluOrtho2D(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)
glutDisplayFunc(draw)
glutIdleFunc(update)
glutKeyboardFunc(keyboardListener)
glutMouseFunc(mouseListener)
glutMainLoop()