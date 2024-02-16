#task_1(Complete)
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys 

rain_direction=0
light=0
def draw_points(x, y):
    glPointSize(5) #pixel size. by default 1 thake
    glBegin(GL_POINTS)
    glColor3f(169, 50, 0)  # Set color to blue
    glVertex2f(x,y) #jekhane show korbe pixel
    glEnd()

def drawShapes(a,b,c,d):
    glBegin(GL_TRIANGLES)
    glColor3f(0.0, 1.50, 1.0) 
    glVertex2d(a, b)
    glColor3f(0.0, 1.0, 1.5) 
    glVertex2d(d, b)
    glColor3f(0.0, 1.0, 0.5) 
    glVertex2d(b, c)
    glEnd()


def drawLines(x1,x2,y1,y2):
    glLineWidth(3)
    glBegin(GL_LINES)
    glColor3f(10.75, 0.50, 3.0)
    glVertex2f(x1,y1)
    glVertex2f(x2,y2)
    glEnd()

def drawRains(a, b):
    global h,f, rain_direction
    w = b - a
    for h in range(1, 500, 15):
        f = a+ (a% 2)
        divisor = (h % 9) + 6
        if divisor != 0:
            print(h)

            for i in range(0, w , divisor):
                print(i,f)
                glLineWidth((h % 2)+1)
                glBegin(GL_LINES)
                glColor3f(0, 0, 3.0)
                glVertex2f(h+rain_direction, f)
                glVertex2f(h, f + (h%9)+5)
                glEnd()
                f += (h%9) + 11

            
def bkc():
    glClearColor(light,light,light)

def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    # bkc()
    glClearColor(light, light, light,0.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # glClearColor(0.0, 0.0, 0.0)
    glLoadIdentity()
    # glClearColor(0.0, 0.0, 0.0)
    iterate()
    glColor3f(0.0, 0.0, 0.0) #konokichur color set (RGB)
    #call the draw methods here
    # draw_points(250, 250)
    drawShapes(80,250,375,418) 
    drawLines(89,89,12,250)#####wall
    drawLines(411,411,12,250)#####wall
    drawLines(89,411,12,12)#####wall
    drawLines(110,175,150,150)#####door
    drawLines(110,110,12,150)#####door
    drawLines(175,175,12,150)#####door
    draw_points(125, 75)###door nob
    drawLines(320-40,320-40,100,200)#####win
    drawLines(320-40,400,100,100)#####win
    drawLines(320-40,400,200,200)#####win
    drawLines(400,400,100,200)#####win
    drawLines(338,338,100,200)#####win
    drawLines(340,340,100,200)#####win
    drawLines(280,400,149,149)#####win
    drawLines(280,400,151,151)#####win
    drawRains(252,500)
    glutSwapBuffers()





def specialKeyListener(key, x, y):
    global rain_direction,light
    if key == b'w':
        rain_direction -= 2
        print("W key pressed")
    elif key == b'q':
        rain_direction += 2
        print("Q key pressed")
    elif key == b'\x1b': 
        sys.exit()  
    elif key == GLUT_KEY_RIGHT:
        rain_direction += 2
        print("right")
    elif key == GLUT_KEY_LEFT:
        rain_direction -= 2
        print("left")
    elif key == b'd':
        light += 0.05
        print("Brighter")
    elif key == b'n':
        light-=0.05
        print("Darker")
    glutPostRedisplay()

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500)
glutInitWindowPosition(0, 0)
glutCreateWindow(b"OpenGL Coding Practice")
glutDisplayFunc(showScreen)
glutKeyboardFunc(specialKeyListener)  # Register keyboard callback function
glutSpecialFunc(specialKeyListener) 
glutMainLoop()