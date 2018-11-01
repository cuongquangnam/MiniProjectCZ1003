# please read the comments
# if you find sth that weird, you can fix it with a double #, like this:
# this is flase -> 
## this is false
import pygame, sys
from pygame.locals import *

pygame.init()



# stage 1: hello user
# stage 2: ask user what they want to eat


# stage 3: show the result of searching
# in stage 3, user may want to search again (reason may be they misclicked, or just to choose another food)
# so case 1: we need a BACK button to return to stage 2
#    case 2: keep the main functions of stage 2, but display it on the screen of stage 3


# stage 4: if user request to see the map, show them what we've got
# in stage 4, they may want to zoom the map, drag the map to their proper position to observe,
# so we need to calculate the mouse position and its relation to the current map
# which may be different in scale and position, it needs a little bit of math (xd).
# we also need a BACK button, ZOOM IN, ZOOM OUT, drag the map by mouse, by KEYS, or by DIRECTION buttons
# to manipulate the scale and position of the map
# ADD-ON feature: when moving the mouse around the map, the pop-up appears, showing where the mouse is

def main():
    width = 900
    height = 648
    FPS = 60

    global screen, clock, mouse
    mouse = pygame.mouse.get_pos()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption('NTU F&B')
    stage = 1
    mouseClicked = False

    while True:
        if stage == 1:
            # box 1
            font1 = pygame.font.SysFont("Arial", 50)
            text1 = font1.render("Welcome to NTU F&B", True, (255,255,255))
            textbox1 = text1.get_rect()
            textbox1.center = (width//2, height//3)
            screen.blit(text1, textbox1)
            # box 2
            font2 = pygame.font.SysFont("Arial", 60)
            text2 = font2.render("GET STARTED", True, (255, 200, 0), (30, 50, 140))
            textbox2 = text2.get_rect()
            textbox2.center = (width//2, height//1.5)
            screen.blit(text2, textbox2)
            if textbox2.collidepoint(mouse) and mouseClicked:
                stage += 1
        if stage == 2:
            map = pygame.image.load('ntumap(2).png')
            map = pygame.transform.scale(map, (width, height))
            screen.blit(map, (0,0))

        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # if event.type == MOUSEMOTION:
            #     mouse = event.pos
            if event.type == MOUSEBUTTONUP:
                mouseClicked = True
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                width, height = event.w, event.h
        pygame.display.update()
        clock.tick(FPS)

def start(): # hello user
    start_font1 = pygame.font.SysFont('Helvetica', 60)
    box1 = writeText(screen, "Welcome to NTU F&B", (255,255,255), None, start_font1, width//2, height//3)

# In case there are so many boxes with text in our interface, this function would work well
# def writeText(screen, text, text_color, background, font, x_center, y_center):
#     textSurface = font.render(text, True, text_color, background)
#     textRect = textSurface.get_rect()
#     textRect.center = (x_center, y_center)
#     screen.blit(textSurface, textRect)


# ask user what they want to eat
#

main()
