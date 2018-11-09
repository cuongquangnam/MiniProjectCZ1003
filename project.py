import pygame, sys, time, math
from pygame.locals import *

from function import *
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
YELLOW  = (255, 255,   0)

# input boxes
validChars = "`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./"
shiftChars = '~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?'

map = pygame.image.load('ntumap(2).png')
ratio_scale = 1.3
initial_scale = 3309/900 # original width/scree width
food_list = [
    "B & D",
    "Chinese",
    "Fast food",
    "Indian",
    "Japanese",
    "Mala",
    "Mixed Rice",
    "Vegetarian",
    "Western",
    "Others"
]

def main():
    FPS = 120
    global screen, clock, mouse, shiftDown, width, height, space, backspace, max_rating, mouseClicked
    # all stage materials
    width = 900
    height = 636
    stage = 1
    mouse = pygame.mouse.get_pos()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption('NTU Food')


    # materials in stage 2
    # option part
    selected_box = [False]*len(food_list)
    box_of_choices = []
    num_of_choices = 0
    locked = False
    minBox = TextBox()
    maxBox = TextBox()
    dishBox = TextBox()
    pricerange = [0, 100]
    # rating
    max_rating, current_rating = 5, 0

    # stage 3
    rating_active = False
    price_active = False
    distance_active = False

    # stage 4
    left_image = 0
    top_image = 0
    user_location = (0,0)
    current_scale = 0
    place = ""
    hall_place = ""

    # start of loop
    while True:
        mouseClicked = False
        mouseClickedUp = False
        shiftDown = False
        backspace = False
        space = False
        pressed = pygame.key.get_pressed()
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
            # if event.type == pygame.KEYUP:
            #     if event.key == pygame.K_SPACE:
            #         space = False
            #     if event.key == pygame.K_BACKSPACE:
            #         backspace = False
            #     if event.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
            #         shiftDown = False
            if event.type == pygame.KEYDOWN:
                if minBox.active and not minBox.locked: minBox.add_chr(pygame.key.name(event.key))
                if maxBox.active and not maxBox.locked: maxBox.add_chr(pygame.key.name(event.key))
                if dishBox.active and not dishBox.locked: dishBox.add_chr(pygame.key.name(event.key))
                if event.key == K_SPACE:
                    space = True
                if event.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
                    shiftDown = True
                    if dishBox.active and not dishBox.locked: dishBox.add_chr(pygame.key.name(event.key))
                if event.key == pygame.K_BACKSPACE:
                    backspace = True

        # stage 1
        if stage == 1:
            screen.fill((0,167,157))
            cover = pygame.transform.scale(pygame.image.load("cover.jpg"), (900, 636))
            display_image(cover, 0, 0, width, height)
            drawTextCenter("Comic Sans MS", "NTU Food", YELLOW, None, 35, width//2, height//2, True)
            box2 = drawTextCenter("Gadugi", "GET START", (255,255,200), None, 35, width//2, height//1.4, True)
            if box2.collidepoint(mouse):
                display_image(cover, 0, 0, width, height)
                drawTextCenter("Comic Sans MS", "NTU Food", YELLOW, None, 35, width//2, height//2, True)
                drawTextCenter("Gadugi", "GET START", (255, 255, 200), None, 37, width//2, height//1.4, True)
                if mouseClickedUp:
                    stage = 2

        #stage 2
        if stage == 2:
            screen.fill(WHITE)

            # build boxes of options
            for i in range(len(food_list)):
                box_color = WHITE
                box_border = BLACK
                back_box = get_place(i) # postion of box i
                if selected_box[i]:
                    box_color = (255, 162, 100)
                    box_border = (200, 120, 0)
                    if mouseClicked and back_box.collidepoint(mouse):
                        selected_box[i] = not selected_box[i]
                        box_of_choices.remove(i)
                        num_of_choices -= 1
                else:
                    if back_box.collidepoint(mouse):
                        box_color = (153, 217, 234)
                        box_border = (0, 0, 180)
                        if num_of_choices < 3:
                            if mouseClicked:
                                selected_box[i] = not selected_box[i]
                                box_of_choices.append(i)
                                num_of_choices += 1
                        else:
                            drawTextTopLeft("Ebrima", "Maximum number of food reached!", 18, RED, None, width//20, height//5.9)
                drawOptions(i, box_color, box_border)

            # Your current choice:
            drawTextTopLeft("Corbel", "Your type of food: ", 30, BLACK, None, width//20, height//20)

            # box of selected choices
            name_of_choices = [food_list[i] for i in box_of_choices] # get in the input of the search function
            choices =  "   " + ", ".join(name_of_choices)
            font_choice2 = pygame.font.SysFont("Maiandra GD", 25)
            text_choice = font_choice2.render(choices, True, BLACK)
            # box_text_choice = text_choice.get_rect()
            box_of_choices_display = pygame.Rect(width//20, height//10, max(width//1.11, 360), height//15)
            pygame.draw.rect(screen, ORANGE, box_of_choices_display, 3)
            screen.blit(text_choice, box_of_choices_display)

            # budget
            drawTextTopLeft("Corbel", "Your budget:", 30, BLACK, None, width//20, height//1.7)

            # Minimum price
            drawTextTopLeft("Corbel", "Min ($)", 25, BLACK, None, width//15, height//1.53)
            minBox.rect = pygame.Rect(width//6, height//1.55, width//9, minBox.image.get_height())
            minBox.active = get_active(minBox.rect, minBox.active)
            if len(minBox.text) == 6:
                minBox.locked = True
                drawTextTopLeft("Corbel", "Too many characters!", 20, RED, None, width//3.5, height//1.53)
            else: minBox.locked = False
            if minBox.active:
                minBox.color = BLUE
                if backspace and len(minBox.text) > 1: minBox.text = minBox.text[:-1]
            else: minBox.color = BLUE1
            pygame.draw.rect(screen, minBox.color, minBox.rect, 2)
            screen.blit(minBox.image,  minBox.rect)

            # Maximum price
            drawTextTopLeft("Gadugi", "Max ($)", 25, BLACK, None, width//15, height//1.39)
            maxBox.rect = pygame.Rect(width//6, height//1.4, width//9, maxBox.image.get_height())
            maxBox.active = get_active(maxBox.rect, maxBox.active)
            if len(maxBox.text) == 6:
                maxBox.locked = True
                drawTextTopLeft("Gadugi", "Too many characters!", 20, RED, None, width//3.5, height//1.39)
            else: maxBox.locked = False
            if maxBox.active:
                maxBox.color = BLUE
                if backspace and len(maxBox.text) > 1: maxBox.text = maxBox.text[:-1]
            else: maxBox.color = BLUE1
            pygame.draw.rect(screen, maxBox.color, maxBox.rect, 2)
            screen.blit(maxBox.image,  maxBox.rect)

            # rating
            drawTextTopLeft("Gadugi", "Rating: " + str(current_rating), 30, BLACK, None, width//2, height//1.7)
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
            drawTextTopLeft("Gadugi", "Your dish:", 30, BLACK, None, width//20, height//2.1)
            dishBox.rect = pygame.Rect(width//5, height//2.1, width/1.34, dishBox.image.get_height())
            dishBox.active = get_active(dishBox.rect, dishBox.active)
            if dishBox.active:
                if backspace and len(dishBox.text) > 1: dishBox.text = dishBox.text[:-1]
                if space: dishBox.text += " "
                dishBox.color = BLUE
            else: dishBox.color = BLUE1
            pygame.draw.rect(screen, dishBox.color, dishBox.rect, 2)
            screen.blit(dishBox.image,  dishBox.rect)
            # submit button
            submit = drawTextCenter("Gadugi", "SUBMIT", BLACK, WHITE, 35, width//2, height//1.2, False)
            submit_box = drawBorderCenter(submit[2] + 10, submit[3] + 6, submit.center[0], submit.center[1], BLACK, 3)
            if submit_box.collidepoint(mouse):
                pygame.draw.rect(screen, (100, 100, 255), submit_box)
                pygame.draw.rect(screen, BLACK, submit_box, 3)
                drawTextCenter("Gadugi", "SUBMIT", WHITE, None, 35, width//2, height//1.2, False)
                if mouseClicked:
                    stage = 3
        # stage 3: return results to user
        # get input from stage 2: box_of_choices, minBox.text, maxBox.text, dishBox.text, current_rating
        if stage == 3:
            screen.fill(WHITE)
            result = []
            # FOOD
            list_of_choices = [food_list[i] for i in box_of_choices]
            name_of_choices = ", ".join(list_of_choices)
            drawTextTopLeft("Calibri", "Food: " + process_input(name_of_choices), 25, BLACK, None, width//50, height//30)
            # RATING
            drawTextTopLeft("Calibri", "Rating: " + str(current_rating), 25, BLACK, None, width//2, 3*height//30)
            # DISH
            drawTextTopLeft("Calibri", "Dish: " + process_input(str(dishBox.text)), 25, BLACK, None, width//50, 5*height//30)
            # LOCATION
            locate = drawTextTopLeft("Calibri", "Location: ", 25, BLACK, None, width//2, 5*height//30)
            # SORT BY
            main_sort = drawTextTopLeft("Calibri", "Sort by: ", 25, BLACK, None, width//2, height//30)
            rating_sort = drawTextTopLeft("Calibri", "Rating", 25, BLACK, None, main_sort.right + 5, height//30)
            dash1 = drawTextTopLeft("Calibri", "/", 25, BLACK, None, rating_sort.right + 5, height//30)
            price_sort = drawTextTopLeft("Calibri", "Price", 25, BLACK, None, dash1.right + 5, height//30)
            dash2 = drawTextTopLeft("Calibri", "/", 25, BLACK, None, price_sort.right + 5, height//30)
            distance_sort = drawTextTopLeft("Calibri", "Distance", 25, BLACK, None, dash2.right + 5, height//30)
            rating_active = get_active(rating_sort, rating_active)
            price_active = get_active(price_sort, price_active)
            distance_active = get_active(distance_sort, distance_active)
            if rating_active: drawTextTopLeft("Calibri", "Rating", 25, BLACK, BLUE1, main_sort.right + 5, height//30)
            if price_active: drawTextTopLeft("Calibri", "Price", 25, BLACK, BLUE1, dash1.right + 5, height//30)
            if distance_active:
                drawTextTopLeft("Calibri", "Distance", 25, BLACK, BLUE1, dash2.right + 5, height//30)
                if place == "":
                    drawTextTopLeft("Calibri", "You haven't choose your location", 25, RED, None, locate.right + 5, 5*height//30)
            if place != "": drawTextTopLeft("Calibri", place, 25, BLACK, None, locate.right + 5, 5*height//30)

            if box_of_choices == [] and minBox.text == " " and maxBox.text == " " and dishBox.text == " ":
                drawTextTopLeft("Calibri", "Price: " + displayValidPrice([None, None]), 25, BLACK, None, width//50, 3*height//30)
                drawNotFound()
            else:
                # PRICE
                price_range = validPrice(minBox.text, maxBox.text)
                drawTextTopLeft("Calibri", "Price: " + displayValidPrice(price_range), 25, BLACK, None, width//50, 3*height//30)
                if price_range == [None, None]:
                    drawNotFound()
                else:
                    result = searchfood(list_of_choices, price_range, current_rating, dishBox.text[1:], df)
                    if rating_active:
                        result = sort_by_rating(result)
                    if price_active:
                        result = sort_by_price(result)
                    if distance_active and place != "":
                        result = sort_by_location(process_place(place), result, infocan)
                    # result = sort_by_rating(result)
                    # print(box_of_choices, price_range, current_rating, dishBox.text[1:])
                    if result.shape[0] == 0:
                        drawNotFound()
                    else:
                        canteen_list = result.index.unique()
                        image_list = [infocan.loc[canteen]["Image"] for canteen in canteen_list]
                        drawCanteenBoxes(canteen_list, image_list, stage)

            stage = backNext(stage, 2, 4)

        # stage 4: map
        if stage == 4:
            list_of_boxes, list_of_names = generateMap()
            buttonZone = drawBorderCenter(height//15, height//1.42 - height//1.6 + height//15, width//1.065, (height//1.6 + height//1.42)/2, RED, 1)
            moveZone = drawBorderCenter(3*height/15, 3*height/15, width//1.065, height//1.12, RED, 1)
            confirmZone = drawBorderCenter(600, 46, 300, height - 14, RED, 1)
            screen.fill(WHITE)
            ratio = initial_scale * (ratio_scale ** current_scale)
            map_copy = pygame.transform.scale(map, (int(3309/ratio), int(2339/ratio)))
            left_image, top_image, image_width, image_height = display_image(map_copy, top_image, left_image, width, height)
            processed_mouse = processMouse(top_image, left_image, image_width, image_height, mouse)
            zoomIn = zoomButton(width//1.065, height//1.6, True)
            zoomOut = zoomButton(width//1.065, height//1.42, False)
            if (zoomIn or pressed[pygame.K_LEFTBRACKET]) and current_scale > -10:
                current_scale -= 1
                left_image, top_image, image_width, image_height = zoom(1, top_image, left_image, image_width, image_height)
                time.sleep(0.1)
            if (zoomOut or pressed[pygame.K_RIGHTBRACKET]) and current_scale < 0 :
                current_scale += 1
                left_image, top_image, image_width, image_height = zoom(-1, top_image, left_image, image_width, image_height)
                time.sleep(0.1)
            up, down, left, right = moveButtons()
            if pressed[pygame.K_UP] and (top_image <= 0) or up.collidepoint(mouse) and mouseClicked:
                top_image += 30
                time.sleep(0.08)
            if pressed[pygame.K_DOWN] and (top_image + image_height >= height) or down.collidepoint(mouse) and mouseClicked:
                top_image -= 30
                time.sleep(0.08)
            if pressed[pygame.K_LEFT] and (left_image <= 0) or left.collidepoint(mouse) and mouseClicked:
                left_image += 30
                time.sleep(0.08)
            if pressed[pygame.K_RIGHT] and (left_image + image_width >= width) or right.collidepoint(mouse) and mouseClicked:
                left_image -= 30
                time.sleep(0.08)

            if mouseClicked:
                if not buttonZone.collidepoint(mouse) and not moveZone.collidepoint(mouse) and not confirmZone.collidepoint(mouse):
                    user_location = str(processed_mouse)
                hall_place = ""
                hall_place = checkMap(list_of_boxes, list_of_names, hall_place, processed_mouse)
            else:
                checkMap(list_of_boxes, list_of_names, hall_place, processed_mouse)

            # return to stage 3 to sort by distance
            proceed = drawTextCenter("Gadugi", "Proceed ?", BLACK, WHITE, 25, 52, height - 14, False)
            if proceed.collidepoint(mouse):
                drawTextCenter("Gadugi", "Proceed ?", WHITE, (0, 100, 100), 25, 52, height - 14, False)
                if mouseClicked:
                    place = user_location
                    stage = 3
            left_location = proceed.right
            text = " Your location: " + user_location + " " + hall_place
            drawTextTopLeft("Gadugi", text, 25, BLACK, WHITE, left_location, height - 30)
        pygame.display.update()
        clock.tick(FPS)

# In case there are so many boxes with text in our interface, this function would work well
# def writeText(screen, text, text_color, background, font, x_center, y_center):
#     textSurface = font.render(text, True, text_color, background)
#     textRect = textSurface.get_rect()
#     textRect.center = (x_center, y_center)
#     screen.blit(textSurface, textRect)

def get_place(index):
    row = index//5
    col = index % 5
    minx = width//20
    miny = height//4.5
    box_width = max(100, width//6)
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
    rect1 = text1.get_rect()
    rect1.topleft = (x_pos, y_pos)
    screen.blit(text1, (x_pos, y_pos))
    return rect1

def drawTextTopRight(font, text, size, color, background, border, x_pos, y_pos):
    font1 = pygame.font.SysFont(font, size)
    text1 = font1.render(text, True, color, background)
    rect1 = text1.get_rect()
    rect1.topright = (x_pos, y_pos)
    screen.blit(text1, rect1)
    pygame.draw.rect(screen, border, rect1, 2)
    return rect1

def backNext(stage, b, n):
    new_stage = stage
    next = drawTextTopRight("Arial", " NEXT ", 20, BLACK, L_GRAY, BLACK, width, 0)
    if next.collidepoint(mouse) and mouseClicked:
        new_stage = n
    back = drawTextTopRight("Arial", " BACK ", 20, BLACK, L_GRAY, BLACK, next.left, 0)
    if back.collidepoint(mouse) and mouseClicked:
        new_stage = b
    return new_stage

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
    goldenstar = pygame.transform.scale(pygame.image.load("goldenstar.png"), (star_size, star_size))
    bluestar = pygame.transform.scale(pygame.image.load("bluestar.png"), (star_size, star_size))
    star = pygame.transform.scale(pygame.image.load("star.png"), (star_size, star_size))
    y_pos = height//1.5
    list_of_star = []
    for i in range(max_rating):
        x_pos = minx + i*(margin + star_size)
        screen.blit(star, (x_pos, y_pos))
        rect = pygame.Rect(x_pos, y_pos, star_size, star_size)
        list_of_star.append(rect)
    return list_of_star + [goldenstar, bluestar]

def drawTextCenter(font, text, color, background, size, x_center, y_center, bold1):
    font_text = pygame.font.SysFont(font, size, bold = bold1)
    textSrf = font_text.render(text, True, color, background)
    textbox = textSrf.get_rect()
    textbox.center = (x_center, y_center)
    screen.blit(textSrf, textbox)
    return textbox

def drawBorderCenter(rect_w, rect_h, x_center, y_center, color, border):
    rect = pygame.Rect(0, 0, rect_w, rect_h)
    rect.center = (x_center, y_center)
    pygame.draw.rect(screen, color, rect, border)
    return rect

def process_input(x):
    input1 = x
    if x == "" or x == " ":
        input1 = "Blank"
    return input1

def process_place(place):
    place1 = place.replace("(", "").replace(")", "").replace(",","")
    place2 = place1.split(" ")
    place3 = [float(a) for a in place2]
    return place3

def displayValidPrice(price_range):
    if price_range == [None, None]:
        return "No price range found"
    else:
        return "${} - ${}".format(price_range[0], price_range[1])

def validPrice(min1, max1):
    price_range = [0, 100]
    if (min1[1:].replace(".", "", 1).isdigit() or min1 == " ") and (max1[1:].replace(".", "", 1).isdigit() or max1 == " "):
        if min1 != " ": price_range[0] = float(min1[1:])
        if max1 != " ": price_range[1] = float(max1[1:])
        if price_range[0] <= price_range[1]: return price_range
    return [None, None]

def drawNotFound():
    not_found = pygame.image.load("notfound.png")
    not_found_box = not_found.get_rect()
    not_found_box.center = (width//2, height//1.8)
    screen.blit(not_found, not_found_box)

def drawCanteenBoxes(canteen_list, image_list, current_stage):
    def drawCanteenBox(x_pos, y_pos, canteen_list, image_list, index, current_stage):
        box_width, box_height = width//6, height//3.2
        box = drawBorderCenter(box_width, box_height, x_pos, y_pos, BLACK, 2)

        # image part
        font1 = "Calibri"
        image = pygame.image.load(image_list[index])
        value = min(int(box_width//1.2), int(box_height//2)) - 8
        ratio = image.get_width() / image.get_height()
        image = pygame.transform.scale(image, (int(value*ratio), value))
        image_box = image.get_rect()
        image_box.center = (x_pos, y_pos - box_height//5)
        screen.blit(image, image_box)

        # text part
        def get_name(raw):
            name = raw
            if raw == "Northspine Foodcourt":
                name = "North spine"
            if raw == "Koufu @ Southspine":
                name =  "South spine"
            return name

        drawTextCenter(font1, get_name(canteen_list[index]), (84, 100, 250), None, 25, x_pos, y_pos + box_height//5, True)
        clickMore = drawTextCenter(font1, "Click more", WHITE, None, 15, x_pos + box_width//3.8, y_pos + box_height//2.3, False)
        if box.collidepoint(mouse):
            pygame.draw.rect(screen, BLUE, box, 3)
            drawTextCenter(font1, "Click more", BLACK, None, 15, x_pos + box_width//3.8, y_pos + box_height//2.3, False)
        if clickMore.collidepoint(mouse):
            pygame.draw.line(screen, BLACK, (clickMore.left, clickMore.bottom + 0.1), (clickMore.right, clickMore.bottom + 0.1))
            if mouseClicked: # display a pop-up
                current_stage += 1

    num_of_boxes = len(canteen_list)
    down, up, space = 0, num_of_boxes, width//5.8
    if num_of_boxes > 5:
        down = num_of_boxes//2
        up = num_of_boxes - down
    # draw top boxes
    up2, down2 = (up-1)/2, (down-1)/2
    for i in range(up):
        x_pos = (i-up2)*space + width//2
        y_pos = height//2.5
        drawCanteenBox(x_pos, y_pos, canteen_list, image_list, i, current_stage)
    for j in range(down):
        x_pos = (j-down2)*space + width//2
        y_pos = height//1.3
        drawCanteenBox(x_pos, y_pos, canteen_list, image_list, j+up, current_stage)

def get_active(box, active):
    new_active = active
    if mouseClicked:
        if box.collidepoint(mouse):
            new_active = not new_active
        else:
            new_active = False
    return new_active

def generateMap():
    hall1 = pygame.Rect(420, 430, 45, 90)
    hall2 = pygame.Rect(410, 320, 75, 92)
    hall3 = pygame.Rect(430, 200, 35, 30)
    hall4 = pygame.Rect(350, 480, 43, 40)
    hall5 = pygame.Rect(395, 520, 45, 25)
    hall6 = pygame.Rect(480, 415, 50, 40)
    hall7 = pygame.Rect(90, 420, 45, 60)
    hall8 = pygame.Rect(495, 270, 58, 35)
    hall9 = pygame.Rect(555, 240, 60, 30)
    hall10 = pygame.Rect(617, 203, 40, 35)
    hall11 = pygame.Rect(665, 207, 45, 40)
    hall12 = pygame.Rect(395, 150, 40, 40)
    hall13 = pygame.Rect(436, 150, 40, 40)
    hall14 = pygame.Rect(475, 145, 45, 50)
    hall15 = pygame.Rect(527, 150, 65, 30)
    hall16 = pygame.Rect(390, 200, 35, 30)
    std_hostel = pygame.Rect(600, 160, 60, 30)
    pioneer = pygame.Rect(495, 525, 30, 30)
    cresent = pygame.Rect(470, 495, 25, 30)
    grad1 = pygame.Rect(705, 210, 25, 25)
    grad2 = pygame.Rect(665, 175, 30, 25)
    south = pygame.Rect(215, 380, 22, 70)
    north = pygame.Rect(253, 260, 80, 80)
    nie = pygame.Rect(220, 90, 140, 140)
    north_hill = pygame.Rect(665, 255, 45, 30)
    wave = pygame.Rect(583, 435, 60, 55)

    list_of_box = [hall1, hall2, hall3, hall4, hall5, hall6, hall7, hall8, hall9, hall10,
                    hall11, hall12, hall13, hall14, hall15, hall16, std_hostel, cresent, pioneer,
                    grad1, grad2, south, north, nie, north_hill, wave]
    list_of_name = ["Hall 1", "Hall 2", "Hall 3", "Hall 4", "Hall 5", "Hall 6", "Hall 7", "Hall 8", "Hall 9",
                    "Hall 10", "Hall 11", "Hall 12", "Hall 13", "Hall 14", "Hall 15", "Hall 16", "Student hostel",
                    "Pioneer Hall", "Cresent Hall", "Graduate 1", "Graduate 2", "South spine", "North spine", "NIE",
                    "North Hill", "The Wave"]
    return list_of_box, list_of_name

def checkMap(list1, list2, name, processed_mouse):
    name1 = name
    for box in list1:
        if box.collidepoint(processed_mouse):
            name1 = list2[list1.index(box)]
            drawTextTopLeft("Palatino Linotype", name1, 30, BLACK, WHITE, 0, 0)
            break
    return name1
def processMouse(top_image, left_image, image_width, image_height, mouse):
    x1 = round((mouse[0] - left_image)*900/image_width, 0)
    y1 = round((mouse[1] - top_image)*636/image_height, 0)
    return x1, y1

def display_image(image, top_image, left_image, width, height):
    screen_ratio = width/height
    true_width = image.get_width()
    true_height = image.get_height()
    image_ratio = true_width/true_height
    x_pos, y_pos = 0, 0
    image_width, image_height = width, height
    if width >= true_width or height >= true_height:
        if screen_ratio >= image_ratio:
            image_width = int(image_height * image_ratio)
            image1 = pygame.transform.scale(image, (image_width, image_height))
            x_pos = (width - height*image_ratio)//2
            screen.blit(image1, (x_pos, y_pos))
        else:
            image_height = int(image_width / image_ratio)
            image1 = pygame.transform.scale(image, (image_width, image_height))
            y_pos = (height - width/image_ratio)//2
            screen.blit(image1, (x_pos, y_pos))
    else:
        screen.blit(image, (left_image, top_image))
        image_width = true_width
        image_height = true_height
        x_pos = left_image
        y_pos = top_image

    return x_pos, y_pos, image_width, image_height

def zoom(zoom_num, top_image, left_image, image_width, image_height):
    x_center = width//2 - left_image
    y_center = height//2 - top_image
    ratio = ratio_scale if zoom_num == 1 else 1/ratio_scale
    new_x_center = x_center * ratio
    new_y_center = y_center * ratio
    image_width *= ratio
    image_height *= ratio
    new_left_image = width//2 - new_x_center
    new_top_image = height//2 - new_y_center
    return new_left_image, new_top_image, image_width, image_height

def zoomButton(x_center, y_center, bool):
    zoombox = pygame.Rect(0, 0, height//15, height//15)
    zoombox.center = (x_center, y_center)
    color = (130, 170, 250)
    if zoombox.collidepoint(mouse): color = (255, 220, 105)
    pygame.draw.ellipse(screen, color, zoombox)
    pygame.draw.line(screen, BLACK, (x_center - height//40, y_center), (x_center + height//40, y_center), 2)
    if bool:
        pygame.draw.line(screen, BLACK, (x_center, y_center - height//40), (x_center, y_center + height//40), 2)
    return zoombox.collidepoint(mouse) and mouseClicked

def moveButtons():
    color = (100, 240, 150)
    x_cen, y_cen, size = width//1.065, height//1.12, height//15
    dif1, dif2 = size, height//60
    # up
    up = pygame.Rect(0,0, size, size)
    up.center = (x_cen, y_cen - dif1)
    pygame.draw.ellipse(screen, color, up)
    pygame.draw.lines(screen, BLACK, False, ((x_cen - dif2, y_cen - dif1), (x_cen, y_cen - dif1 - dif2), (x_cen + dif2, y_cen - dif1)), 4)
    pygame.draw.line(screen, BLACK, (x_cen, y_cen - dif1 - dif2), (x_cen, y_cen - dif1 + dif2), 3)
    # down
    down = pygame.Rect(0,0, size, size)
    down.center = (x_cen, y_cen + dif1)
    if down.collidepoint(mouse): pygame.draw.ellipse(screen, (255, 220, 105), down)
    pygame.draw.ellipse(screen, color, down)
    pygame.draw.lines(screen, BLACK, False, ((x_cen - dif2, y_cen + dif1), (x_cen, y_cen + dif1 + dif2), (x_cen + dif2, y_cen + dif1)), 4)
    pygame.draw.line(screen, BLACK, (x_cen, y_cen + dif1 - dif2), (x_cen, y_cen + dif1 + dif2), 3)
    # left
    left = pygame.Rect(0,0, size, size)
    left.center = (x_cen - dif1, y_cen)
    if left.collidepoint(mouse): pygame.draw.ellipse(screen, (255, 220, 105), left)
    pygame.draw.ellipse(screen, color, left)
    pygame.draw.lines(screen, BLACK, False, ((x_cen - dif1, y_cen - dif2), (x_cen - dif1 - dif2, y_cen), (x_cen - dif1, y_cen + dif2)), 4)
    pygame.draw.line(screen, BLACK, (x_cen - dif1 - dif2, y_cen), (x_cen - dif1 + dif2, y_cen), 3)
    # right
    right = pygame.Rect(0,0, size, size)
    right.center = (x_cen + dif1, y_cen)
    if right.collidepoint(mouse): pygame.draw.ellipse(screen, (255, 220, 105), right)
    pygame.draw.ellipse(screen, color, right)
    pygame.draw.lines(screen, BLACK, False, ((x_cen + dif1, y_cen - dif2), (x_cen + dif1 + dif2,y_cen), (x_cen + dif1, y_cen + dif2)), 4)
    pygame.draw.line(screen, BLACK, (x_cen + dif1 - dif2, y_cen), (x_cen + dif1 + dif2, y_cen), 3)
    return up, down, left, right

if __name__ == '__main__':
    main()
