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
BLUE1   = (130, 180, 250)
ORANGE  = (240, 150,  50)
L_GRAY  = (230, 230, 230)

# input boxes
validChars = "`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./"
shiftChars = '~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?'

food_list = [
    "Bakery",
    "Beverage",
    "Chinese",
    "Dessert",
    "Fast food",
    "Halal",
    "Indian",
    "Mala",
    "Mixed Rice",
    "Vegetarian",
    "Western",
    "Others"
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
    global screen, clock, mouse, shiftDown, width, height, space, backspace, max_rating
    # all stage materials

    width = 900
    height = 648
    mouse = pygame.mouse.get_pos()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption('NTU Food')

    stage = 1

    # materials in stage 2
    # option part
    selected_box = [False]*len(food_list)
    box_of_choices = []
    num_of_choices = 0
    locked = False
    minBox = TextBox()
    maxBox = TextBox()
    dishBox = TextBox()
    # rating
    # rating
    max_rating = 5
    current_rating = 0
    # start of loop
    while True:
        mouseClicked = False
        mouseClickedUp = False
        shiftDown = False
        backspace = False
        space = False

        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # if event.type == MOUSEMOTION:
            #     mouse = event.pos
            if event.type == MOUSEBUTTONDOWN:
                mouseClicked = True
            if event.type == MOUSEBUTTONUP:
                mouseClickedUp = True
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                width, height = event.w, event.h
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    space = False
                if event.key == pygame.K_BACKSPACE:
                    backspace = False
                if event.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
                    shiftDown = False
            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    space = True
                if event.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
                    shiftDown = True
                    if dishBox.active and not dishBox.locked: dishBox.add_chr(pygame.key.name(event.key))
                if event.key == pygame.K_BACKSPACE:
                    backspace = True
                    # textBox.text = textBox.text[:-1]
                if minBox.active and not minBox.locked: minBox.add_chr(pygame.key.name(event.key))
                if maxBox.active and not maxBox.locked: maxBox.add_chr(pygame.key.name(event.key))
                if dishBox.active and not dishBox.locked: dishBox.add_chr(pygame.key.name(event.key))
        # stage 1
        if stage == 1:
            screen.fill(WHITE)
            submit("Candara", "Welcome to NTU Food", BLACK, None, 50, width//2, height//3)
            box2 = submit("Arial", "GET START", (255,200,0), (30, 50, 140), 60, width//2, height//1.5)
            if box2.collidepoint(mouse) and mouseClickedUp:
                screen.fill(WHITE)
                stage = 2

        #stage 2
        if stage == 2:
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
                        num_of_choices -= 1
                else:
                    if hover:
                        box_color = (153, 217, 234)
                        box_border = (0, 0, 180)
                        if num_of_choices < 3:
                            if mouseClicked:
                                selected_box[i] = not selected_box[i]
                                box_of_choices.append(i)
                                num_of_choices += 1
                        else:
                            drawTextTopLeft("Ebrima", "Maximum number of food reached!", 16, RED, None, width//20, height//5.2)
                drawOptions(i, box_color, box_border)

            # Your current choice:
            drawTextTopLeft("Corbel", "Your type of food: ", 30, BLACK, None, width//20, height//10)

            # box of selected choices
            name_of_choices = [food_list[i] for i in box_of_choices] # get in the input of the search function
            choices =  "   " + ", ".join(name_of_choices)
            font_choice2 = pygame.font.SysFont("Maiandra GD", 20)
            text_choice = font_choice2.render(choices, True, BLACK)
            # box_text_choice = text_choice.get_rect()
            box_of_choices_display = pygame.Rect(width//20, height//7, max(width//2.1, 360), height//19)
            pygame.draw.rect(screen, ORANGE, box_of_choices_display, 3)
            screen.blit(text_choice, box_of_choices_display)

            # vertical line
            pygame.draw.line(screen, BLACK, (max(width//1.8, 400), height//8), (max(width//1.8, 400), height//(8/5)))

            # budget
            drawTextTopLeft("Patalino Linotype", "Your budget:", 30, BLACK, None, width//1.7, height//10)

            # Minimum price
            drawTextTopLeft("Patalino Linotype", "Min ($)", 30, BLACK, None, width//1.7, height//6)
            minBox.rect = pygame.Rect(width//1.45, height//6.5, 100, minBox.image.get_height())
            if mouseClicked:
                if minBox.rect.collidepoint(mouse):
                    minBox.active = not minBox.active
                else:
                    minBox.active = False
            if len(minBox.text) == 6:
                minBox.locked = True
                drawTextTopLeft("Corbel", "Too many characters!", 15, RED, None, width//1.22, height//6)
            else: minBox.locked = False

            minBox.color = BLUE if minBox.active else BLUE1
            if backspace and len(minBox.text) > 1: minBox.text = minBox.text[:-1]
            pygame.draw.rect(screen, minBox.color, minBox.rect, 2)
            screen.blit(minBox.image,  minBox.rect)

            # Maximum price
            drawTextTopLeft("Patalino Linotype", "Max ($)", 30, BLACK, None, width//1.7, height//4.2)
            maxBox.rect = pygame.Rect(width//1.45, height//4.3, 100, maxBox.image.get_height())
            if mouseClicked:
                if maxBox.rect.collidepoint(mouse):
                    maxBox.active = not maxBox.active
                else:
                    maxBox.active = False
            if len(maxBox.text) == 6:
                maxBox.locked = True
                drawTextTopLeft("Corbel", "Too many characters!", 15, RED, None, width//1.22, height//6)
            else: maxBox.locked = False
            maxBox.color = BLUE if maxBox.active else BLUE1
            if backspace and len(maxBox.text) > 1: maxBox.text = maxBox.text[:-1]
            pygame.draw.rect(screen, maxBox.color, maxBox.rect, 2)
            screen.blit(maxBox.image,  maxBox.rect)

            # draw stars
            drawTextTopLeft("Patalino Linotype", "Rating: " + str(current_rating), 30, BLACK, None, width//1.7, height//2.7)
            list_of_star = drawRating(max_rating)
            for j in range(current_rating):
                screen.blit(list_of_star[-2], list_of_star[j])
            for i in range(len(list_of_star[:-2])):
                if list_of_star[i].collidepoint(mouse):
                    for j in range(1+i):
                        screen.blit(list_of_star[-1], list_of_star[j])

                    if mouseClicked:
                        current_rating = i+1
            # let they type their dish
            drawTextTopLeft("Corbel", "Your dish:", 30, BLACK, None, width//50, height//1.45)
            dishBox.rect = pygame.Rect(width//6, height//1.45, width/1.3, dishBox.image.get_height())
            if mouseClicked:
                if dishBox.rect.collidepoint(mouse):
                    dishBox.active = not dishBox.active
                else:
                    dishBox.active = False
            if dishBox.active:
                if backspace and len(dishBox.text) > 1: dishBox.text = dishBox.text[:-1]
                if space: dishBox.text += " "
                dishBox.color = BLUE
            else: dishBox.color = BLUE1


            pygame.draw.rect(screen, dishBox.color, dishBox.rect, 2)
            screen.blit(dishBox.image,  dishBox.rect)
            # submit button
            submit_button = submit("Gill Sans MT", "SUBMIT", (200, 50, 30), None, 60, width//2, height//1.2)
            submit_width, submit_height = submit_button[2] + width//50, submit_button[3] + 20
            submit_box = pygame.Rect(0,0, submit_width, submit_height)
            submit_box.center = (width//2, height//1.2)
            pygame.draw.rect(screen, BLACK, submit_box, 3)
            if submit_box.collidepoint(mouse):
                pygame.draw.rect(screen, (150, 255, 200), submit_box)
                if mouseClicked:
                    stage = 3
            submit("Gill Sans MT", "SUBMIT", (200, 50, 30), None, 60, width//2, height//1.2)

        # stage 3: return results to user
        # get input from stage 2: box_of_choices, minBox.text, maxBox.text, dishBox.text, current_rating
        if stage == 3:
            screen.fill(WHITE)
            # FOOD
            name_of_choices = ", ".join([food_list[i] for i in box_of_choices])
            drawTextTopLeft("Calibri", "Food: " + name_of_choices, 25, BLACK, None, width//50, height//30)
            # PRICE
            price_range = "$" + minBox.text[1:] + " - $" + maxBox.text[1:]
            drawTextTopLeft("Calibri", "Price: " + price_range, 25, BLACK, None, width//50, 3*height//30)
            # RATING
            drawTextTopLeft("Calibri", "Rating: " + str(current_rating), 25, BLACK, None, width//3, 3*height//30)


            back = submit("Arial", "BACK", BLACK, L_GRAY, 15, width//1.3, height//10)
            if back.collidepoint(mouse) and mouseClicked:
                stage = 2

        # stage4: map
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
    box_width = max(100, width//7)
    box_height = max(50, height//12)
    margin = min(15, width//50)
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
    box = get_place(index)      # find its proper place
    font1 = pygame.font.SysFont("Calibri",box.width//6)
    text = font1.render(name, True, BLACK, color)
    textbox = text.get_rect()
    textbox.center = (int(box[0] + box[2]//2), int(box[1] + box[3]//2))
    drawBoxOption(box, color, border)
    screen.blit(text, textbox)

def drawTextTopLeft(font, text, size, color, background, x_pos, y_pos):
    font1 = pygame.font.SysFont(font, size)
    text1 = font1.render(text, True, color, background)
    screen.blit(text1, (x_pos, y_pos))

class TextBox(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.text = " "
        self.font = pygame.font.SysFont("Calibri", 30)
        self.image = self.font.render("", True, [0, 0, 0])
        self.rect = self.image.get_rect()
        self.active = False
        self.locked = False
        self.color = BLUE1

    def add_chr(self, char):
        global shiftDown
        if self.active:
            if char in validChars and not shiftDown:
                self.text += char
            elif char in validChars and shiftDown:
                self.text += shiftChars[validChars.index(char)]
            elif char == " ":
                self.text += " "
        self.image = self.font.render(self.text, True, [0, 0, 0])

def drawRating(max_rating):
    minx = width//1.7
    margin = width//50
    star_size = width//20
    goldenstar = pygame.image.load("goldenstar.png")
    bluestar = pygame.image.load("bluestar.png")
    star = pygame.image.load("star.png")
    goldenstar = pygame.transform.scale(goldenstar, (star_size, star_size))
    bluestar = pygame.transform.scale(bluestar, (star_size, star_size))
    star = pygame.transform.scale(star, (star_size, star_size))
    y_pos = height//2.3
    list_of_star = []
    for i in range(max_rating):
        x_pos = minx + i*(margin + star_size)
        screen.blit(star, (x_pos, y_pos))
        rect = pygame.Rect(x_pos, y_pos, star_size, star_size)
        list_of_star.append(rect)
    return list_of_star + [goldenstar, bluestar]

def submit(font, text, color, background, size, x_center, y_center):
    font_text = pygame.font.SysFont(font, size)
    textSrf = font_text.render(text, True, color, background)
    textbox = textSrf.get_rect()
    textbox.center = (x_center, y_center)
    screen.blit(textSrf, textbox)
    return textbox

def process_input():
    pass
main()
