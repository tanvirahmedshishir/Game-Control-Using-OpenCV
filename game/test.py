import pygame, random, sys ,os,time
from pygame.locals import *
import cv2
import numpy as np
from time import sleep
import thread
import pyautogui
import math

pygame.init()

display_height = 600
display_width = 800

black = (0, 0, 0)
white = (255, 255, 255)

red = (200,0,0)
green = (0,200,0)
yellow = (200,200,0)
blue = (0,0,200)

bright_red = (255,0,0)
bright_green = (0,255,0)
bright_yellow = (255,255,0)
bright_blue = (0,0,255)
car_width = 55
zero=0
global topScore

if not os.path.exists("data/save.dat"):
    f=open("data/save.dat",'w')
    f.write(str(zero))
    f.close()
v=open("data/save.dat",'r')
topScore = int(v.readline())


gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Kuet road traffic challenge')
clock = pygame.time.Clock()

background = pygame.image.load("back.jpg")
gameover = pygame.image.load("gameover.png")
background = pygame.transform.scale(background, (800, 600))
pause=False
background_size = background.get_size()
background_rect = background.get_rect()
gameover_rect =gameover.get_rect()
screen = pygame.display.set_mode(background_size)
w, h = background_size
m = 0
n = 0
global choose
x1 = 0
y1 = -h

obsImg = pygame.image.load('b.png')
obsImg = pygame.transform.scale(obsImg, (50, 80))

RedCar = pygame.image.load('red.png')
RedCar = pygame.transform.scale(RedCar, (50, 85))

BlueCar = pygame.image.load('blue.png')
BlueCar = pygame.transform.scale(BlueCar, (50, 85))

GreenCar = pygame.image.load('green.png')
GreenCar = pygame.transform.scale(GreenCar, (50, 85))

pygame.mixer.music.load('car.wav')
gameOverSound = pygame.mixer.Sound('crash.wav')
laugh = pygame.mixer.Sound('laugh.wav')

def things_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Dodged: " + str(count), True, black)
    gameDisplay.blit(text, (0, 0))

def life_remaining(attempt):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Remaining Life: " + str(attempt), True, black)
    gameDisplay.blit(text, (0, 20))

def disp_highScore(topScore):
    font = pygame.font.SysFont(None, 25)
    text = font.render("High Score: " + str(topScore), True, black)
    gameDisplay.blit(text, (0, 40))

def car(x, y):
    if choose == 1:
        gameDisplay.blit(RedCar, (x, y))
    if choose == 2:
        gameDisplay.blit(BlueCar, (x, y))
    if choose == 3:
        gameDisplay.blit(GreenCar, (x, y))



def obs(x, y):
    gameDisplay.blit(obsImg, (x, y))


def things(thingx, thingy):
    gameDisplay.blit(obsImg, (thingx, thingy))


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def text_objects2(text, font):
    textSurface = font.render(text, True, red)
    return textSurface, textSurface.get_rect()
def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()
    global attempt
    attempt-=1
    if(attempt==0):
        laugh.play()
        attempt=3
        time.sleep(2)
        game_over()


    time.sleep(1)
    game_loop()

    gameOverSound.stop()
def unpause():
    global pause
    pause =False


def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            if action == "car1":
                global choose
                choose = 1
                game_loop()
            if action == "car2":
                choose = 2
                game_loop()
            if action == "car3":
                choose = 3
                game_loop()
            if action=="unpause":
                unpause()
            if action == "quit":
                pygame.quit()
                quit()
            if action == "gameIntro":
                game_intro()

    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",17)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)



def game_intro():
    global attempt
    attempt = 3
    intro = True

    while intro:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

        gameDisplay.fill(white)
        largeText = pygame.font.SysFont("comicsansms", 115)
        smallText = pygame.font.SysFont("comicsansms", 50)
        TextSurf, TextRect = text_objects("Choose Car", smallText)
        TextRect.center = ((display_width / 2), (display_height / 2))
        gameDisplay.blit(TextSurf, TextRect)

        button("Red car", 50, 450, 100, 50, red, bright_red, action = "car1")
        button("Blue car", 250, 450, 100, 50, blue, bright_blue, action = "car2" )
        button("Green car", 450, 450, 100, 50, green, bright_green, action="car3")
        button("Quit", 650, 450, 100, 50, yellow, bright_yellow, action = "quit")

        pygame.display.update()
        clock.tick(120)


def game_over():
    intro = True

    while intro:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        #gameDisplay.fill(white)
        screen.blit(gameover, gameover_rect)
        largeText = pygame.font.SysFont("comicsansms", 115)
        TextSurf, TextRect = text_objects2("Game     Over", largeText)
        TextRect.center = ((display_width / 2), (display_height / 2))
        gameDisplay.blit(TextSurf, TextRect)

        button("Play Again!", 150, 450, 100, 50, green, bright_green, action="gameIntro")
        button("Quit", 550, 450, 100, 50, red, bright_red, action="quit")

        pygame.display.update()
        clock.tick(120)

def paused():
    largeText = pygame.font.SysFont("comicsansms", 115)
    TextSurf, TextRect = text_objects("Paused", largeText)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)

    while pause:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()




        button("Continue", 150, 450, 100, 50, green, bright_green,action="unpause")
        button("Quit", 550, 450, 100, 50, red, bright_red, action="quit")

        pygame.display.update()
        clock.tick(120)

#'''
cap = cv2.VideoCapture(0)
cap.set(3,396)
cap.set(4,216)
def gamecontrol(moveLeft, moveRight, moveUp, moveDown):
    _, frame = cap.read()
    frame = cv2.blur(frame,(3,3))


    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    lower_blue = np.array([110,50,50])
    upper_blue = np.array([130,255,255])
    thresh = cv2.inRange(hsv,lower_blue, upper_blue)

    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    _,contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    max_area = 0
    best_cnt = None
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > max_area:
            max_area = area
            best_cnt = cnt

    M = cv2.moments(best_cnt)

    if(M['m00']>0 and max_area>100):
        cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
        cv2.circle(frame,(cx,cy),5,(0,0,255),-1)

        if(cx>190):
            moveRight = False
            moveLeft = True
        else:
            moveLeft = False
            moveRight = True
        if(cy>100):
            moveUp = False
            moveDown = True
        else:
            moveDown = False
            moveUp = True
    #else:
     #   pygame.mixer.music.stop()
      #  global pause
       # pause = True
        #paused()


    res = cv2.bitwise_and(frame,frame, mask= mask)
    res = (255-res)
    res=cv2.flip(res,1)
    cv2.imshow("res",res)


    return moveLeft, moveRight, moveUp, moveDown


def crash():
    global topScore
    if dodged > topScore:
        g = open("data/save.dat", 'w')
        g.write(str(dodged))
        g.close()
        topScore = dodged
    message_display('You Crashed')

    pygame.mixer.music.stop()




def game_loop():
    global pause
    x = (display_width * 0.45)
    y = (display_height * 0.85)
    moveLeft = moveRight = moveUp = moveDown = False
    x_change = 0
    y_change = 0
    thing_startx = random.randrange(0, display_width)
    thing_starty = -600
    thing_speed = 7
    global dodged
    dodged = 0




    gameExit = False

    while not gameExit:

        screen.blit(background, background_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    time.sleep(0.4)
                    game_intro()



            if event.type == pygame.KEYDOWN:
                #if event.key == pygame.K_p:


                if event.key == pygame.K_r:
                    f = open("data/save.dat", 'w')
                    f.write(str(zero))
                    f.close()
                    global topScore
                    topScore=0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP :
                    y_change = -5

                elif event.key == pygame.K_DOWN :
                    y_change = 5

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0


        moveLeft, moveRight, moveUp, moveDown = gamecontrol(moveLeft, moveRight, moveUp, moveDown)

        if moveLeft:
            x_change = -5
        elif moveRight:
            x_change = 5
        if moveUp:
            y_change = -5
        elif moveDown:
            y_change = 5





        x += x_change
        y += y_change

        pygame.mixer.music.play(-1, 0.0)
        global y1
        global n
        y1 += 5
        n += 5
        screen.blit(background, (m, n))
        screen.blit(background, (x1, y1))
        if n > h:
            n = -h
        if y1 > h:
            y1 = -h

        things(thing_startx, thing_starty)
        thing_starty += thing_speed
        car(x, y)
        things_dodged(dodged)
        life_remaining(attempt)
        disp_highScore(topScore)
        pygame.display.flip()
        pygame.display.update()

        if x > (display_width - car_width) or x < 0 or (y > display_height - car_width or y < 0):
            pygame.mixer.music.stop()
            gameOverSound.play()
            crash()

        if thing_starty > display_height:
            thing_starty = 0 - 70
            thing_startx = random.randrange(0, display_width-500)
            dodged += 1
            thing_speed += 1



        if y < thing_starty + 75:
            print('y crossover')

            if x > thing_startx and x < thing_startx + 50 or x + car_width > thing_startx and x + car_width < thing_startx + 50:
                print('x crossover')
                pygame.mixer.music.stop()
                gameOverSound.play()

                crash()





        pygame.display.update()
        clock.tick(120)

game_intro()
game_loop()
pygame.quit()
quit()
