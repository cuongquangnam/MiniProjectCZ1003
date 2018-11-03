# please read the comments
# if you find sth that weird, you can fix it with a double #, like this:
# this is flase ->
## this is false
import pygame, sys, time
from pygame.locals import *

pygame.init()

# color
WHITE   = (255, 255, 255)
BLACK   = (  0,   0,   0)
RED     = (255,   0,   0)
GREEN   = (  0, 255,   0)
BLUE    = (  0,   0, 255)

food_list = [
    "yasuo",
    "vayne",
    "annie",
    "galio",
    "kayle",
    "rakan",
    "xayah"
]
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
    FPS = 60
    global screen, clock, mouse, width, height
    # all stage materials
    width = 900
    height = 648
    mouse = pygame.mouse.get_pos()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption('NTU F&B')
    stage = 1

    # materials in stage 2
    selected_box = [False]*len(food_list)
    box_of_choices = []
    num_of_choices = 0
    locked = False
    while True:
        mouseClicked = False

        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # if event.type == MOUSEMOTION:
            #     mouse = event.pos
            if event.type == MOUSEBUTTONDOWN:
                mouseClicked = True
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                width, height = event.w, event.h

        if stage == 1:
            # box 1
            screen.fill(WHITE)
            font1 = pygame.font.SysFont("Candara", 50)
            text1 = font1.render("Welcome to NTU F&B", True, BLACK)
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
                stage = 2

        if stage == 2: # let them choose
            screen.fill(WHITE)

            # build boxes of options
            for i in range(len(food_list)):
                box_color = WHITE
                box_border = BLACK
                back_box = get_place(i)
                hover = back_box.collidepoint(mouse)
                if selected_box[i]:
                    box_color = (255, 162, 100)
                    box_border = (200, 120, 0)
                    if mouseClicked and hover:
                        selected_box[i] = not selected_box[i]
                        box_of_choices.remove(i)
                else:
                    if hover:
                        box_color = (153, 217, 234)
                        box_border = (0, 0, 180)
                        if mouseClicked:
                            selected_box[i] = not selected_box[i]
                            box_of_choices.append(i)
                drawOptions(i, box_color, box_border)

            # Your current choice:
            font_choice1 = pygame.font.SysFont("Corbel", 30)
            choice_intro = font_choice1.render("Your current choice: ", True, BLACK)
            screen.blit(choice_intro, (width//20, height//10))

            # box of selected choices
            name_of_choices = [food_list[i] for i in box_of_choices]
            choices =  "   " + ", ".join(name_of_choices)
            font_choice2 = pygame.font.SysFont("Maiandra GD", 25)
            text_choice = font_choice2.render(choices, True, BLACK)
            #box_text_choice = text_choice.get_rect()
            box_of_choices_display = pygame.Rect(width//20, height//7, width//2.5, height//20)

            pygame.draw.rect(screen, BLUE, box_of_choices_display, 3)
            screen.blit(text_choice, box_of_choices_display)

        if stage == 4:
            map = pygame.image.load('ntumap(2).png')
            map = pygame.transform.scale(map, (width, height))
            screen.blit(map, (0,0))

            # a small button to back to stage 1
            button1 = pygame.Rect(width-30, 0, 30, 20)
            pygame.draw.rect(screen, RED, button1)
            if button1.collidepoint(mouse) and mouseClicked:
                stage = 1


        pygame.display.update()
        clock.tick(FPS)

# In case there are so many boxes with text in our interface, this function would work well
# def writeText(screen, text, text_color, background, font, x_center, y_center):
#     textSurface = font.render(text, True, text_color, background)
#     textRect = textSurface.get_rect()
#     textRect.center = (x_center, y_center)
#     screen.blit(textSurface, textRect)

def get_place(index):
    row = index//3
    col = index % 3
    minx = width//20
    miny = height//4
    box_width = min(100, width//8)
    box_height = min(60, height//10)
    margin = min(20, width//40)
    x_pos = minx + col*(box_width + margin)
    y_pos = miny + row*(box_height + margin)
    back_box = pygame.Rect(x_pos, y_pos, box_width, box_height)
    return back_box

def drawBoxOption(box, color, border):
    x, y, width1, height1 = box
    radius = min(width, height)//50
    drawRoundedRectangle(border, x, y, width1, height1, radius)
    drawRoundedRectangle(color, x+2, y+2, width1-4, height1-4, radius-2)

def drawRoundedRectangle(color, x, y, width, height, radius):
    diameter = 2*radius
    pygame.draw.rect(screen, color, (x+radius, y, width - diameter, radius))
    pygame.draw.rect(screen, color, (x, y + radius, width, height - diameter))
    pygame.draw.rect(screen, color, (x+radius, y + height - radius, width - diameter, radius))
    pygame.draw.ellipse(screen, color, (x, y, diameter, diameter))                       # top-left quarter circle
    pygame.draw.ellipse(screen, color, (x + width - diameter, y, diameter, diameter))   # top-right quarter circle
    pygame.draw.ellipse(screen, color, (x, y + height - diameter, diameter, diameter))  # bot-left quarter circle
    pygame.draw.ellipse(screen, color, (x + width - diameter, y + height - diameter, diameter, diameter))

def drawOptions(index, color, border): # draw the box with its text in the middle
    name = food_list[index]
    font1 = pygame.font.SysFont("Calibri", 30)
    text = font1.render(name, True, BLACK, color)
    textbox = text.get_rect()
    box = get_place(index)      # find its proper place
    textbox.center = (int(box[0] + box[2]//2), int(box[1] + box[3]//2))
    drawBoxOption(box, color, border)
    screen.blit(text, textbox)

class optionBox(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.text = text
        self.selected = selected
        self.box_color = box_color
        self.box_border = box_border


main()
