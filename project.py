import sys
import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

class Button:
    def __init__(self, label, x, y, width, height, callback):
        self.label = label
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.callback = callback

    def draw(self):
        glColor3f(1.0, 1.0, 1.0)
        draw_rectangle(self.x, self.y, self.width, self.height, (0, 0, 0))
        glColor3f(1.0, 1.0, 1.0)
        draw_text(self.x + 10, self.y + self.height // 2, self.label)

    def is_clicked(self, click_x, click_y):
        return (
            self.x <= click_x <= self.x + self.width
            and self.y <= click_y <= self.y + self.height
        )

# Global vars
ball_x = 400
ball_y = 50
ball_radius = 10
ball_dx = 2
ball_dy = 2
#Lives 
life_count = 3

paddle_x = 350
paddle_y = 20
paddle_width = 100
paddle_height = 20

window_width = 800
window_height = 600

num_blocks_x = 10
num_blocks_y = 6
block_width = window_width // num_blocks_x
block_height = 30

blocks = [[1 for a in range(num_blocks_x)] for b in range(num_blocks_y)]

paddle_colors = [
    (0.0, 1.0, 0.0),  # Green
    (1.0, 0.0, 0.0),  # Red
    (0.0, 0.0, 1.0),  # Blue
    (1.0, 1.0, 0.0),  # Yellow
]

current_paddle_color = random.choice(paddle_colors)

game_over = False
is_paused = False
score = 0

pause_button = Button("Pause", window_width - 80, 20, 60, 20, lambda: toggle_pause())
restart_button = Button("Restart", window_width - 80, 50, 60, 20, lambda: restart_game())
exit_button = Button("Exit", window_width - 80, 80, 60, 20, lambda: exit_game())


buttons = [pause_button, restart_button, exit_button]

def init():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow(b"Rainbow Brick Buster")
    glutDisplayFunc(draw)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse)
    glutTimerFunc(16, update, 0)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    gluOrtho2D(0, window_width, 0, window_height)

def draw_circle(x, y, radius):
    segments = 100
    angle_increment = 2.0 * math.pi / segments

    glBegin(GL_POINTS)

    for i in range(segments + 1):
        angle = i * angle_increment
        dx = radius * math.cos(angle)
        dy = radius * math.sin(angle)
        glVertex2f(x + dx, y + dy)

    glEnd()

######################################################## BLOCKS ##############################################
def draw_rectangle(x, y, width, height, color):
    glColor3f(*color)
    glPointSize(2.0)

    glBegin(GL_POINTS)

    ################### lines(using the MP line algo)#######################
    # top line 
    MP_Line(x, y, x + width, y)
    #right line 
    MP_Line(x + width, y, x + width, y + height)
    # bottom line 
    MP_Line(x + width, y + height, x, y + height)
    # left line
    MP_Line(x, y + height, x, y)


    ############### rounded edges(using the MP circle algo)###################
    MP_Circle(x, y + height / 2, height / 2)
    MP_Circle(x + width, y + height / 2, height / 2)

    glEnd()

def MP_Line(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    x, y = x1, y1
    glVertex2f(x, y)

    if abs(dx) > abs(dy):
        steps = abs(dx)
    else:
        steps = abs(dy)

    x_increment = dx / float(steps)
    y_increment = dy / float(steps)

    for _ in range(int(steps)):
        x += x_increment
        y += y_increment
        glVertex2f(round(x), round(y))

def MP_Circle(cx, cy, radius):
    x = radius
    y = 0
    P = 1 - radius

    while x > y:
        glVertex2f(x + cx, y + cy)
        glVertex2f(y + cx, x + cy)
        glVertex2f(-x + cx, y + cy)
        glVertex2f(-y + cx, x + cy)
        glVertex2f(-x + cx, -y + cy)
        glVertex2f(-y + cx, -x + cy)
        glVertex2f(x + cx, -y + cy)
        glVertex2f(y + cx, -x + cy)

        y += 1

        if P <= 0:
            P = P + 2 * y + 1
        else:
            x -= 1
            P = P + 2 * y - 2 * x + 1

        if x < y:
            break

        glVertex2f(x + cx, y + cy)
        glVertex2f(y + cx, x + cy)
        glVertex2f(-x + cx, y + cy)
        glVertex2f(-y + cx, x + cy)
        glVertex2f(-x + cx, -y + cy)
        glVertex2f(-y + cx, -x + cy)
        glVertex2f(x + cx, -y + cy)
        glVertex2f(y + cx, -x + cy)

def draw_blocks():
    for i in range(num_blocks_y):
        for j in range(num_blocks_x):
            if blocks[i][j]:
                if i == 0 or i == 5 or j == 0 or j == 9 or (1 < i < 4 and 3 <= j <= 6):
                    draw_rectangle(j * block_width, window_height - (i + 1) * block_height, block_width, block_height,
                                   (random.uniform(0,1), random.uniform(0,1), random.uniform(0,1)))
                else:
                    draw_rectangle(j * block_width, window_height - (i + 1) * block_height, block_width, block_height,
                                   (random.uniform(0,1), random.uniform(0,1), random.uniform(0,1)))
                    
########################################## Writings(fixed on screen) #############################################
def draw_text(x, y, text):
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

def draw_score():
    glColor3f(1.0, 1.0, 1.0)
    draw_text(window_width - 780, window_height - 570, f"Score: {score}")

def draw_lives():
    glColor3f(1.0, 1.0, 1.0)
    draw_text(window_width - 780, window_height - 592, f"Lives left: {life_count}")


def draw_buttons():
    for button in buttons:
        button.draw()

def mouse(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        for btn in buttons:
            if btn.is_clicked(x, window_height - y):
                btn.callback()

def draw():
    global game_over

    glClear(GL_COLOR_BUFFER_BIT)

    # Draw the ball
    # Set ball color based on life_count
    if life_count == 3:
        glColor3f(0.0, 1.0, 0.0)  # Green
    elif life_count == 2:
        glColor3f(1.0, 1.0, 0.0)  # Yellow
    elif life_count == 1:
        glColor3f(1.0, 0.0, 0.0)  # Red

    draw_circle(ball_x, ball_y, ball_radius)

    # Draw the paddle
    global current_paddle_color
    draw_rectangle(paddle_x, paddle_y, paddle_width, paddle_height, current_paddle_color)

    # Draw the blocks
    draw_blocks()

    # Draw the score
    draw_score()

    #Draw the lives counter
    draw_lives() 

    # Draw the buttons
    draw_buttons()

    if game_over:
        glColor3f(1.0, 0.0, 0.0)
        draw_text(window_width // 2 - 50, window_height // 2, "Game Over!")
        draw_text(window_width // 2 - 50, window_height // 2.5, f"Your Score: {score}")
        glutSwapBuffers()
        return
    glutSwapBuffers()


def update(value):
    global ball_x, ball_y, ball_dx, ball_dy, game_over, score, life_count

    if game_over:
        return
    if not is_paused:
        # Update ball position based on the current score
        if score > 2 and score <= 6:
            ball_x += ball_dx + ball_dx 
            ball_y += ball_dy + ball_dy 
        elif 6 < score <= 14:
            ball_x += ball_dx + ball_dx * 2
            ball_y += ball_dy + ball_dy * 2
        elif 14 < score <= 30:
            ball_x += ball_dx + ball_dx * 3
            ball_y += ball_dy + ball_dy * 3
        elif 30 < score <= 120:
            ball_x += ball_dx + ball_dx * 4
            ball_y += ball_dy + ball_dy * 4


        # Add more ranges as needed
        else:
            ball_x += ball_dx
            ball_y += ball_dy

        # Check for collisions with walls
        if ball_x + ball_radius > window_width or ball_x - ball_radius < 0:
            ball_dx *= -1

        if ball_y + ball_radius > window_height:
            game_over = True
            ball_dy *= -1

        if ball_y - ball_radius < 0:
            ball_dy *= -1

        # Check for collision with the paddle
        if (
            ball_x >= paddle_x
            and ball_x <= paddle_x + paddle_width
            and ball_y - ball_radius <= paddle_y + paddle_height
        ):
            ball_dy *= -1
            change_paddle_color()

        # Check for collision with blocks
        hit_block_y = (window_height - ball_y) // block_height
        hit_block_x = ball_x // block_width
        if (
            hit_block_y >= 0
            and hit_block_y < num_blocks_y
            and hit_block_x >= 0
            and hit_block_x < num_blocks_x
            and blocks[hit_block_y][hit_block_x]
        ):
            ball_dy *= -1
            blocks[hit_block_y][hit_block_x] = 0
            score += 2

        # Check for game over condition
        if ball_y - ball_radius < 0:
            life_count -=1
            if life_count == 0:
                game_over = True

    glutPostRedisplay()
    glutTimerFunc(16, update, 0)


def change_paddle_color():
    global current_paddle_color
    current_paddle_color = random.choice(paddle_colors)

def generate_random_points():
    glPushMatrix()
    glTranslatef(0, 0, 0)
    glColor3f(1.0, 1.0, 1.0)
    for _ in range(10):
        x = random.randint(0, window_width // 2)
        y = random.randint(window_height // 2, window_height)
        draw_circle(x, y, 3)
    glPopMatrix()

def exit_game():
    glutLeaveMainLoop()


def toggle_pause():
    global is_paused
    is_paused = not is_paused

def restart_game():
    global game_over, score, ball_x, ball_y, ball_dx, ball_dy, is_paused,life_count,num_blocks_x, num_blocks_y,block_width, block_height, blocks
    game_over = False
    score = 0
    ball_x = 400
    ball_y = 50
    ball_dx = 2
    ball_dy = 2
    life_count = 3
    num_blocks_x = 10
    num_blocks_y = 6
    block_width = window_width // num_blocks_x
    block_height = 30
    blocks = [[1 for a in range(num_blocks_x)] for b in range(num_blocks_y)]
    is_paused = False
    glutPostRedisplay()
    glutTimerFunc(16, update, 0)

def keyboard(key, x, y):
    global paddle_x, is_paused

    if key == b'q':
        glutLeaveMainLoop()
    elif key == b'a' and paddle_x > 0:
        paddle_x -= 20
    elif key == b'd' and paddle_x + paddle_width < window_width:
        paddle_x += 20
    elif key == b'p':
        is_paused = not is_paused

if __name__ == "__main__":
    init()
    glutMainLoop()