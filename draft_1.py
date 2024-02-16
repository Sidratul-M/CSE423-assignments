from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
import time

# def blink_points():
#     global points
#     start_time = time.time()  # Record the start time
#     duration = 1.0  # Duration of transition in seconds
#     while time.time() - start_time < duration:  # While duration has not elapsed
#         t = (time.time() - start_time) / duration  # Calculate interpolation parameter (0 to 1)
#         for point in points:
#             if point.color == point.original_color:  # If the point's current color is its original color
#                 interpolated_color = interpolate_color(point.original_color, (0.0, 0.0, 0.0), t)
#             else:
#                 interpolated_color = interpolate_color((0.0, 0.0, 0.0), point.original_color, t)
#             point.color = interpolated_color


W_Width, W_Height = 500, 500

points = []  # List to store generated points
boundary_size = 180  # Size of the boundary region
point_speed = 0.10  # Speed of the points
point_radius = 2  # Radius of the points
speed_increment = 0.1  # Speed increment/decrement value
blink_interval = 100  # Blink interval in milliseconds
is_frozen = False  # Flag to indicate whether points are frozen
blink_flag = False  # Flag to indicate whether points are blinking


class Point:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.original_color = color  # Store the original color
        self.direction = random.choice([(1, 1), (-1, 1), (1, -1), (-1, -1)])




    def move(self):
        if not is_frozen:
            self.x += self.direction[0] * point_speed
            self.y += self.direction[1] * point_speed

            if self.x <= -boundary_size / 2 or self.x >= boundary_size / 2:
                self.direction = (-self.direction[0], self.direction[1])
            if self.y <= -boundary_size / 2 or self.y >= boundary_size / 2:
                self.direction = (self.direction[0], -self.direction[1])

    def draw(self):
        glColor3f(*self.color)
        glBegin(GL_POINTS)
        glVertex2f(self.x, self.y)
        glEnd()


# def generate_point(x, y):
#     global points
#     color = (random.random(), random.random(), random.random())
#     points.append(Point(x, y, color))

def generate_point(x, y):
    global points
    color = (random.random(), random.random(), random.random())  # Generate random color
    new_point = Point(x, y, color)
    points.append(new_point)


def mouseListener(button, state, x, y):
    global is_frozen
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        c_x, c_y = convert_coordinate(x, y)
        generate_point(c_x, c_y)
    elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN :
        i=0
        blink_points()
        # while i<20:
        #     blink_points()
        #     i+=1
    glutPostRedisplay()

import time

def blink_points():
    global points
    while True:  # Run indefinitely
        start_time = time.time()  # Record the start time for each loop
        duration = 1.0  # Duration of each transition in seconds
        while time.time() - start_time < duration:  # While duration has not elapsed
            t = (time.time() - start_time) / duration  # Calculate interpolation parameter (0 to 1)
            for point in points:
                if point.color == point.original_color:  # If the point's current color is its original color
                    interpolated_color = interpolate_color(point.original_color, (0.0, 0.0, 0.0), t)
                else:
                    interpolated_color = interpolate_color((0.0, 0.0, 0.0), point.original_color, t)
                point.color = interpolated_color
            display()  # Update display to show interpolated colors

def interpolate_color(color1, color2, t):
    # Interpolate between color1 and color2 using parameter t
    return (
        color1[0] * (1 - t) + color2[0] * t,
        color1[1] * (1 - t) + color2[1] * t,
        color1[2] * (1 - t) + color2[2] * t
    )


def keyboardListener(key, x, y):
    global point_speed, is_frozen
    if key == b'\x1b':  # Escape key
        is_frozen = not is_frozen
    elif key == b' ':  # Spacebar
        is_frozen = not is_frozen
    elif key == b'\x1b[A':  # Up arrow key
        point_speed += speed_increment
    elif key == b'\x1b[B':  # Down arrow key
        point_speed -= speed_increment
        if point_speed < 0:
            point_speed = 0
    glutPostRedisplay()

def specialKeyListener(key, x, y):
    global point_speed
    if is_frozen:
        return
    if key == GLUT_KEY_UP:
        point_speed *= 2  # Increase speed by multiplying by 2
        print("Speed Increased")
    elif key == GLUT_KEY_DOWN:
        point_speed /= 2  # Decrease speed by dividing by 2
        print("Speed Decreased")
    elif key == b' ':
        toggle_freeze()
        print("Freeze Toggled")

def animate(value):
    if not is_frozen:
        for point in points:
            point.move()
    glutPostRedisplay()
    glutTimerFunc(10, animate, 0)


def draw_axes():
    glLineWidth(2)
    glBegin(GL_LINES)
    glColor3f(1.0, 1.0, 1.0)  # White color for the boundary lines
    glVertex2f(-boundary_size / 2, -boundary_size / 2)
    glVertex2f(boundary_size / 2, -boundary_size / 2)

    glVertex2f(boundary_size / 2, -boundary_size / 2)
    glVertex2f(boundary_size / 2, boundary_size / 2)

    glVertex2f(boundary_size / 2, boundary_size / 2)
    glVertex2f(-boundary_size / 2, boundary_size / 2)

    glVertex2f(-boundary_size / 2, boundary_size / 2)
    glVertex2f(-boundary_size / 2, -boundary_size / 2)
    glEnd()

    # Draw dashed lines to mark the boundary of movement
    glEnable(GL_LINE_STIPPLE)
    glLineStipple(1, 0xAAAA)  # Dashed pattern
    glBegin(GL_LINE_LOOP)
    glColor3f(0.5, 0.5, 0.5)  # Gray color for the dashed lines
    glVertex2f(-boundary_size / 2, -boundary_size / 2)
    glVertex2f(boundary_size / 2, -boundary_size / 2)
    glVertex2f(boundary_size / 2, boundary_size / 2)
    glVertex2f(-boundary_size / 2, boundary_size / 2)
    glEnd()
    glDisable(GL_LINE_STIPPLE)


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 200, 0, 0, 0, 0, 1, 0)

    draw_axes()

    glPointSize(point_radius)
    glBegin(GL_POINTS)
    for point in points:
        glColor3f(*point.color)
        glVertex2f(point.x, point.y)
    glEnd()

    glutSwapBuffers()



def convert_coordinate(x, y):
    return x - (W_Width / 2), (W_Height / 2) - y


def init():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(104, 1, 1, 1000.0)
    glEnable(GL_DEPTH_TEST)


glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutCreateWindow(b"Amazing Box")

init()

glutDisplayFunc(display)
glutIdleFunc(lambda: glutPostRedisplay())
glutMouseFunc(mouseListener)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutTimerFunc(10, animate, 0)
 
glutMainLoop()
